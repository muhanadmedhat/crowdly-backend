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
    path('<int:id>/images/', projectImageUpload_views.ProjectImageView.as_view()),
    path('<int:id>/images/<int:img_id>/', projectImageUpload_views.ProjectImageDeleteView.as_view()),
    path('', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('latest/', LatestProjectsAPIView.as_view(), name='latest-projects'),
    path('category/<int:category_id>/', ProjectsByCategoryAPIView.as_view(), name='projects-by-category'),
    path('<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('<int:project_id>/similar/', SimilarProjectsAPIView.as_view(), name='similar-projects'),
    path('<int:pk>/cancel/', cancel_project, name='cancel-project'),
]
