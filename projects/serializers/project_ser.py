from rest_framework import serializers
from .category_ser import CategorySerializer
from .tag_ser import TagSerializer
from ..models.project_model import Project


class ProjectSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True) # nested serializer is like .populate in mongoose
    tags     = TagSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'details', 'total_target', 'total_donated', 'status', 'category', 'tags', 'average_rating', 'rating_count', 'cover_image']

    def get_cover_image(self, obj):
        first_image = obj.images.order_by('id').first()
        return first_image.image.url if first_image else None