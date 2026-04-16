from django.urls import path
from .views import (
    CategoryListAPIView,
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
    ProjectsByCategoryAPIView,
    LatestProjectsAPIView,
    SimilarProjectsAPIView,
    cancel_project,
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),

    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/latest/', LatestProjectsAPIView.as_view(), name='latest-projects'),
    path('projects/category/<int:category_id>/', ProjectsByCategoryAPIView.as_view(), name='projects-by-category'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('projects/<int:project_id>/similar/', SimilarProjectsAPIView.as_view(), name='similar-projects'),
    path('projects/<int:pk>/cancel/', cancel_project, name='cancel-project'),
]