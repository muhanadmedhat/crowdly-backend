from rest_framework import serializers
from .category_ser import CategorySerializer
from .tag_ser import TagSerializer
from ..models.project_model import Project


class ProjectSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True) # nested serializer is like .populate in mongoose
    tags     = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'goal_amount', 'current_amount', 'status', 'category', 'tags']