from django.urls import path, include
from rest_framework.routers import DefaultRouter
from admin_panel.views import (
    ProjectReportListView,
    ProjectReportActionView,
    CommentReportListView,
    CommentReportActionView,
    ReplyReportListView,
    ReplyReportActionView,
    CategoryViewSet,
)

# Router for viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

app_name = 'admin_panel'

urlpatterns = [
    # Category management
    path('', include(router.urls)),
    
    # Project reports
    path('reports/projects/', ProjectReportListView.as_view(), name='project-reports-list'),
    path('reports/projects/<int:report_id>/', ProjectReportActionView.as_view(), name='project-reports-action'),
    
    # Comment reports
    path('reports/comments/', CommentReportListView.as_view(), name='comment-reports-list'),
    path('reports/comments/<int:report_id>/', CommentReportActionView.as_view(), name='comment-reports-action'),
    
    # Reply reports
    path('reports/replies/', ReplyReportListView.as_view(), name='reply-reports-list'),
    path('reports/replies/<int:report_id>/', ReplyReportActionView.as_view(), name='reply-reports-action'),
]
