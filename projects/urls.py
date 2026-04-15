from django.urls import path

from .views import category_views, tags_views
from .views import projectImageUpload_views

urlpatterns = [
    path('categories/', category_views.CategoryListCreateView.as_view()),
    path('categories/<int:id>/projects/', category_views.CategoryProjectsView.as_view()),
    path('tags/', tags_views.TagListCreateView.as_view()),
    path('projects/<int:id>/images/', projectImageUpload_views.ProjectImageUploadView.as_view()),
    path('projects/<int:id>/images/<int:img_id>/', projectImageUpload_views.ProjectImageDeleteView.as_view()),
]