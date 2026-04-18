from rest_framework import generics, permissions
from ..models.project_model import Project
from ..models.projectImage_model import ProjectImage
from ..serializers.projectImage_ser import ProjectImageSerializer

class ProjectImageView(generics.ListCreateAPIView): # POST, GET -> /projects/<id>/images/
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectImageSerializer

    def get_queryset(self):
        return ProjectImage.objects.filter(project__id=self.kwargs['id'])

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['id'])
        serializer.save(project=project)

class ProjectImageDeleteView(generics.DestroyAPIView): # DELETE /projects/<id>/images/<img_id>/
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectImage.objects.filter(
            project__id=self.kwargs['id'],
            project__creator=self.request.user  # only the creator can delete
        )
    
    def get_object(self):
        return self.get_queryset().get(id=self.kwargs['img_id'])