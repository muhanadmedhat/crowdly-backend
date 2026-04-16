from django.urls import path

from .views import category_views, tags_views, featured_views
from .views import projectImageUpload_views
from .projectViews import (
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
    ProjectsByCategoryAPIView,
    LatestProjectsAPIView,
    SimilarProjectsAPIView,
    cancel_project,
)

urlpatterns = [
    path('categories/', category_views.CategoryListCreateView.as_view()),
    path('categories/<int:id>/projects/', category_views.CategoryProjectsView.as_view()),
    path('tags/', tags_views.TagListCreateView.as_view()),
    path('featured/', featured_views.FeaturedProjectsView.as_view()),
    path('projects/<int:id>/images/', projectImageUpload_views.ProjectImageUploadView.as_view()),
    path('projects/<int:id>/images/<int:img_id>/', projectImageUpload_views.ProjectImageDeleteView.as_view()),
    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/latest/', LatestProjectsAPIView.as_view(), name='latest-projects'),
    path('projects/category/<int:category_id>/', ProjectsByCategoryAPIView.as_view(), name='projects-by-category'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('projects/<int:project_id>/similar/', SimilarProjectsAPIView.as_view(), name='similar-projects'),
    path('projects/<int:pk>/cancel/', cancel_project, name='cancel-project'),
]
