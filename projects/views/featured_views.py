from rest_framework import generics, permissions
from ..models.project_model import Project
from ..serializers.project_ser import ProjectSerializer


class FeaturedProjectsView(generics.ListAPIView):  # GET /projects/featured/
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Project.objects.filter(
            is_featured=True,
            status='running'
        ).order_by('-created_at')[:5]
