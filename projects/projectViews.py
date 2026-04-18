from django.db.models import Q, Count, Avg
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import Project, Category
from .projectSerializers import (
    CategorySerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectCreateUpdateSerializer,
)
from .permissions import IsOwnerOrReadOnly


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Project.objects.select_related(
            'owner', 'category'
        ).prefetch_related('tags', 'images').all()

        category_id = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        sort = self.request.query_params.get('sort')
        status_filter = self.request.query_params.get('status')
        is_featured = self.request.query_params.get('is_featured')
        total_target = self.request.query_params.get('max_goal')
        average_rating = self.request.query_params.get('min_rating')
        


        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(details__icontains=search) |
                Q(tags__name__icontains=search) |
                Q(category__name__icontains=search)
            ).distinct()

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if is_featured is not None:
            is_featured_normalized = is_featured.strip().lower()
            if is_featured_normalized in ['true', '1', 'yes']:
                queryset = queryset.filter(is_featured=True)
            elif is_featured_normalized in ['false', '0', 'no']:
                queryset = queryset.filter(is_featured=False)

        if total_target:
            try:
                total_target_value = float(total_target)
                queryset = queryset.filter(total_target__lte=total_target_value)
            except ValueError:
                pass  # Ignore invalid total_target values

        if average_rating:
            try:
                average_rating_value = float(average_rating)
                queryset = queryset.annotate(avg_rating=Avg('rating__score')).filter(avg_rating__gte=average_rating_value)
            except ValueError:
                pass  # Ignore invalid average_rating values

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

        queryset = queryset.annotate(
            average_rating=Avg('rating__score'),
            rating_count=Count('rating')
        )

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
    ).prefetch_related('tags', 'images').annotate(
        average_rating=Avg('rating__score'),
        rating_count=Count('rating')
    ).all()

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
        ).prefetch_related('tags', 'images').filter(
            category_id=category_id
        ).annotate(
            average_rating=Avg('rating__score'),
            rating_count=Count('rating')
        )


class LatestProjectsAPIView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Project.objects.select_related(
            'owner', 'category'
        ).prefetch_related('tags', 'images').filter(
            status='running',
            is_cancelled=False
        ).annotate(
            average_rating=Avg('rating__score'),
            rating_count=Count('rating')
        ).order_by('-created_at')[:5]


<<<<<<< Updated upstream
from rest_framework.views import APIView
from rest_framework.response import Response
=======
class MyProjectsAPIView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.select_related(
            'owner', 'category'
        ).prefetch_related('tags').filter(
            owner=self.request.user
        ).order_by('-created_at')


class SimilarProjectsAPIView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.AllowAny]
>>>>>>> Stashed changes

class SimilarProjectsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, project_id):
        try:
            current_project = Project.objects.prefetch_related('tags', 'images').get(id=project_id)
        except Project.DoesNotExist:
            return Response([])

        tags = current_project.tags.values_list('id', flat=True)

        queryset = Project.objects.select_related(
            'owner', 'category'
        ).prefetch_related('tags', 'images').filter(
            category=current_project.category
        ).exclude(
            id=current_project.id
        ).annotate(
            average_rating=Avg('rating__score'),
            rating_count=Count('rating')
        )

        if tags:
            queryset = queryset.filter(tags__in=tags).distinct()

<<<<<<< Updated upstream
        queryset = queryset.order_by('-is_featured', 'id')[:5]
        serializer = ProjectListSerializer(queryset, many=True)
        return Response(serializer.data)
=======
        return queryset.order_by('id')

>>>>>>> Stashed changes

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
    project.status = 'cancelled'
    project.save()

    return Response(
        {'detail': 'Project cancelled successfully.'},
        status=status.HTTP_200_OK
    )