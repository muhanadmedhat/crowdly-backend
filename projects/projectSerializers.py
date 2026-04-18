from rest_framework import serializers
from django.db.models import Avg

from projects.serializers.category_ser import CategorySerializer
from projects.serializers.tag_ser import TagSerializer
from .models import Category, Tag, Project



class ProjectListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        annotated_value = getattr(obj, 'average_rating', None)
        if annotated_value is not None:
            return float(annotated_value)
        return obj.rating_set.aggregate(avg=Avg('score'))['avg']

    def get_rating_count(self, obj):
        annotated_value = getattr(obj, 'rating_count', None)
        if annotated_value is not None:
            return int(annotated_value)
        return obj.rating_set.count()

    def get_cover_image(self, obj):
        first_image = obj.images.order_by('id').first()
        if not first_image:
            return None

        request = self.context.get('request')
        if request is None:
            return first_image.image.url
        return request.build_absolute_uri(first_image.image.url)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'details',
            'status',
            'is_featured',
            'total_target',
            'total_donated',
            'start_time',
            'end_time',
            'is_cancelled',
            'created_at',
            'updated_at',
            'owner',
            'category',
            'tags',
            'average_rating',
            'rating_count',
            'cover_image',
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        annotated_value = getattr(obj, 'average_rating', None)
        if annotated_value is not None:
            return float(annotated_value)
        return obj.rating_set.aggregate(avg=Avg('score'))['avg']

    def get_rating_count(self, obj):
        annotated_value = getattr(obj, 'rating_count', None)
        if annotated_value is not None:
            return int(annotated_value)
        return obj.rating_set.count()

    def get_cover_image(self, obj):
        first_image = obj.images.order_by('id').first()
        if not first_image:
            return None

        request = self.context.get('request')
        if request is None:
            return first_image.image.url
        return request.build_absolute_uri(first_image.image.url)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'details',
            'status',
            'is_featured',
            'total_target',
            'total_donated',
            'start_time',
            'end_time',
            'is_cancelled',
            'created_at',
            'updated_at',
            'owner',
            'category',
            'tags',
            'average_rating',
            'rating_count',
            'cover_image',
        ]


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'details',
            'status',
            'is_featured',
            'total_target',
            'total_donated',
            'start_time',
            'end_time',
            'category',
            'tags',
            'is_cancelled',
        ]
        read_only_fields = ['id','is_featured']

    def validate(self, attrs):
        start_time = attrs.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = attrs.get('end_time', getattr(self.instance, 'end_time', None))

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError("end_time must be later than start_time.")

        return attrs

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None

        if validated_data.get('status') == 'cancelled':
            validated_data['is_cancelled'] = True

        if validated_data.get('is_cancelled'):
            validated_data['status'] = 'cancelled'

        if user is None:
            raise serializers.ValidationError(
                "Authenticated user is required to create a project."
            )

        project = Project.objects.create(owner=user, **validated_data)
        project.tags.set(tags)
        return project

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)

        if validated_data.get('status') == 'cancelled':
            validated_data['is_cancelled'] = True

        if validated_data.get('is_cancelled') is True:
            validated_data['status'] = 'cancelled'

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        return instance