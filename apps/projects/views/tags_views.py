from rest_framework import generics, permissions
from ..models.tag_model import Tag
from ..serializers.tag_ser import TagSerializer

class TagListCreateView(generics.ListCreateAPIView): # GET /tags/  POST /tags/
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]