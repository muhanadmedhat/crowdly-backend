from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import Project, Category
from .serializers import (
    CategorySerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectCreateUpdateSerializer,
)
from .permissions import IsOwnerOrReadOnly


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Project.objects.select_related(
            'owner', 'category'
        ).prefetch_related('tags').all()

        category_id = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        sort = self.request.query_params.get('sort')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(details__icontains=search) |
                Q(tags_name_icontains=search) |
                Q(category_name_icontains=search)
            ).distinct()

        # sort examples:
        # ?sort=latest
        # ?sort=oldest
        # ?sort=target_asc
        # ?sort=target_desc
        if sort == 'latest':
            queryset = queryset.order_by('-created_at')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'target_asc':
            queryset = queryset.order_by('total_target')
        elif sort == 'target_desc':
            queryset = queryset.order_by('-total_target')

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateUpdateSerializer
        return ProjectListSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.select_related(
        'owner', 'category'
    ).prefetch_related('tags').all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectCreateUpdateSerializer
        return ProjectDetailSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]

    def get_serializer_context(self):
        return {'request': self.request}


class ProjectsByCategoryAPIView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Project.objects.select_related(
            'owner', 'category'
        ).prefetch_related('tags').filter(category_id=category_id)


class LatestProjectsAPIView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Project.objects.select_related(
            'owner', 'category'
        ).prefetch_related('tags').order_by('-created_at')[:5]


class SimilarProjectsAPIView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        project_id = self.kwargs['project_id']

        try:
            current_project = Project.objects.prefetch_related('tags').get(id=project_id)
        except Project.DoesNotExist:
            return Project.objects.none()

        tag_ids = current_project.tags.values_list('id', flat=True)

        queryset = Project.objects.select_related(
            'owner', 'category'
        ).prefetch_related('tags').filter(
            category=current_project.category
        ).exclude(
            id=current_project.id
        )

        if tag_ids:
            queryset = queryset.filter(tags__in=tag_ids).distinct()

        return queryset[:5]


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cancel_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(
            {'detail': 'Project not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if project.owner != request.user:
        return Response(
            {'detail': 'You do not have permission to cancel this project.'},
            status=status.HTTP_403_FORBIDDEN
        )

    if project.is_cancelled:
        return Response(
            {'detail': 'Project is already cancelled.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    project.is_cancelled = True
    project.save()

    return Response(
        {'detail': 'Project cancelled successfully.'},
        status=status.HTTP_200_OK
    )