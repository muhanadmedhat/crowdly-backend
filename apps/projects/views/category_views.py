from rest_framework import generics, permissions
from ..models.category_model import Category
from ..models.project_model import Project
from ..serializers.project_ser import ProjectSerializer
from ..serializers.category_ser import CategorySerializer

class CategoryListCreateView(generics.ListCreateAPIView): # GET /categories/  POST /categories/
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]  # only admin can create
        return [permissions.AllowAny()]


class CategoryProjectsView(generics.ListAPIView): # GET /categories/<id>/projects/
    serializer_class = ProjectSerializer

    def get_queryset(self):
        category_id = self.kwargs['id']
        return Project.objects.filter(category__id=category_id)