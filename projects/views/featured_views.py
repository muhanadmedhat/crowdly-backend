from rest_framework import generics, permissions
from ..models.project_model import Project
from ..projectSerializers import ProjectListSerializer


class FeaturedProjectsView(generics.ListAPIView):  # GET /projects/featured/
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Project.objects.filter(
            is_featured=True,
            status='running'
        ).order_by('-created_at')[:5]
