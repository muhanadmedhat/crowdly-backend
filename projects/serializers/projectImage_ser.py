from rest_framework import serializers
from ..models.projectImage_model import ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'image_url', 'order']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None