from rest_framework import serializers

from projects.serializers.category_ser import CategorySerializer
from projects.serializers.tag_ser import TagSerializer
from .models import Category, Tag, Project



class ProjectListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'details',
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
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'details',
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
        ]


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = [
            'title',
            'details',
            'total_target',
            'total_donated',
            'start_time',
            'end_time',
            'category',
            'tag_ids',
            'is_cancelled',
        ]

    def validate(self, attrs):
        start_time = attrs.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = attrs.get('end_time', getattr(self.instance, 'end_time', None))

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError("end_time must be later than start_time.")

        return attrs

    def create(self, validated_data):
        tags = validated_data.pop('tag_ids', [])
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None

        if user is None:
            raise serializers.ValidationError(
                "Authenticated user is required to create a project."
            )

        project = Project.objects.create(owner=user, **validated_data)
        project.tags.set(tags)
        return project

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        return instance