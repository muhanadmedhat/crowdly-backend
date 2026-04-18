from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from django.db.models import Q
from interactions.models import ProjectReport, CommentReport, ReplyReport
from interactions.serializers import (
    ProjectReportSerializer,
    CommentReportSerializer,
    ReplyReportSerializer,
)
from projects.models import Category
from admin_panel.permissions import IsAdminUser
from admin_panel.serializers import (
    ReportActionSerializer,
    CategorySerializer,
)


class AdminPagination(PageNumberPagination):
    """Pagination for admin endpoints"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProjectReportListView(APIView):
    """
    Admin endpoint to list all project reports.
    
    GET: List project reports with filtering by status
    Query params:
    - status: 'pending', 'reviewed', 'approved', 'rejected'
    - search: search by project title or reporter username
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            # Get filter parameters
            status_filter = request.query_params.get('status', 'pending')
            search_query = request.query_params.get('search', '')
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))

            # Build query
            queryset = ProjectReport.objects.select_related(
                'project', 'reporter', 'project__owner'
            ).all()

            # Filter by status
            if status_filter in ['pending', 'reviewed', 'approved', 'rejected']:
                queryset = queryset.filter(status=status_filter)

            # Search filter
            if search_query:
                queryset = queryset.filter(
                    Q(project__title__icontains=search_query) |
                    Q(reporter__username__icontains=search_query)
                )

            # Order by most recent
            queryset = queryset.order_by('-created_at')

            # Paginate
            start = (page - 1) * page_size
            end = start + page_size
            total_count = queryset.count()

            serializer = ProjectReportSerializer(queryset[start:end], many=True)

            return Response({
                'count': total_count,
                'page': page,
                'page_size': page_size,
                'results': serializer.data,
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectReportActionView(APIView):
    """
    Admin endpoint to take action on a specific project report.
    
    PATCH: Update report status and add admin notes
    Body:
    {
        "action": "approve" or "reject",
        "admin_notes": "Optional notes about the action"
    }
    """
    permission_classes = [IsAdminUser]

    def patch(self, request, report_id):
        try:
            report = ProjectReport.objects.get(id=report_id)
            
            # Validate action
            serializer = ReportActionSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            action_taken = serializer.validated_data['action']
            admin_notes = serializer.validated_data.get('admin_notes', '')

            # Update report
            if action_taken == 'approve':
                report.status = 'reviewed'
            elif action_taken == 'reject':
                report.status = 'rejected'

            report.admin_notes = admin_notes
            report.save()

            response_serializer = ProjectReportSerializer(report)
            return Response(
                {
                    'message': f'Report {action_taken} successfully',
                    'report': response_serializer.data
                },
                status=status.HTTP_200_OK
            )

        except ProjectReport.DoesNotExist:
            return Response(
                {'error': 'Report not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommentReportListView(APIView):
    """
    Admin endpoint to list all comment reports.
    
    GET: List comment reports
    Query params:
    - status: 'pending', 'reviewed', 'approved', 'rejected'
    - search: search by comment text or reporter username
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            status_filter = request.query_params.get('status', 'pending')
            search_query = request.query_params.get('search', '')
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))

            queryset = CommentReport.objects.select_related(
                'comment', 'reporter', 'comment__author', 'comment__project'
            ).all()

            if status_filter in ['pending', 'reviewed', 'approved', 'rejected']:
                queryset = queryset.filter(status=status_filter)

            if search_query:
                queryset = queryset.filter(
                    Q(comment__text__icontains=search_query) |
                    Q(reporter__username__icontains=search_query)
                )

            queryset = queryset.order_by('-created_at')

            start = (page - 1) * page_size
            end = start + page_size
            total_count = queryset.count()

            serializer = CommentReportSerializer(queryset[start:end], many=True)

            return Response({
                'count': total_count,
                'page': page,
                'page_size': page_size,
                'results': serializer.data,
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommentReportActionView(APIView):
    """
    Admin endpoint to take action on a specific comment report.
    
    PATCH: Update report status and add admin notes
    """
    permission_classes = [IsAdminUser]

    def patch(self, request, report_id):
        try:
            report = CommentReport.objects.get(id=report_id)
            
            serializer = ReportActionSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            action_taken = serializer.validated_data['action']
            admin_notes = serializer.validated_data.get('admin_notes', '')

            if action_taken == 'approve':
                report.status = 'reviewed'
            elif action_taken == 'reject':
                report.status = 'rejected'

            report.admin_notes = admin_notes
            report.save()

            response_serializer = CommentReportSerializer(report)
            return Response(
                {
                    'message': f'Report {action_taken} successfully',
                    'report': response_serializer.data
                },
                status=status.HTTP_200_OK
            )

        except CommentReport.DoesNotExist:
            return Response(
                {'error': 'Report not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReplyReportListView(APIView):
    """
    Admin endpoint to list all reply reports.
    
    GET: List reply reports
    Query params:
    - status: 'pending', 'reviewed', 'approved', 'rejected'
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            status_filter = request.query_params.get('status', 'pending')
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))

            queryset = ReplyReport.objects.select_related(
                'reply', 'reporter', 'reply__author'
            ).all()

            if status_filter in ['pending', 'reviewed', 'approved', 'rejected']:
                queryset = queryset.filter(status=status_filter)

            queryset = queryset.order_by('-created_at')

            start = (page - 1) * page_size
            end = start + page_size
            total_count = queryset.count()

            serializer = ReplyReportSerializer(queryset[start:end], many=True)

            return Response({
                'count': total_count,
                'page': page,
                'page_size': page_size,
                'results': serializer.data,
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReplyReportActionView(APIView):
    """
    Admin endpoint to take action on a specific reply report.
    
    PATCH: Update report status and add admin notes
    """
    permission_classes = [IsAdminUser]

    def patch(self, request, report_id):
        try:
            report = ReplyReport.objects.get(id=report_id)
            
            serializer = ReportActionSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            action_taken = serializer.validated_data['action']
            admin_notes = serializer.validated_data.get('admin_notes', '')

            if action_taken == 'approve':
                report.status = 'reviewed'
            elif action_taken == 'reject':
                report.status = 'rejected'

            report.admin_notes = admin_notes
            report.save()

            response_serializer = ReplyReportSerializer(report)
            return Response(
                {
                    'message': f'Report {action_taken} successfully',
                    'report': response_serializer.data
                },
                status=status.HTTP_200_OK
            )

        except ReplyReport.DoesNotExist:
            return Response(
                {'error': 'Report not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryViewSet(ModelViewSet):
    """
    Admin endpoint for category management (CRUD).
    
    - GET /admin-panel/categories/ - List all categories
    - POST /admin-panel/categories/ - Create new category
    - GET /admin-panel/categories/{id}/ - Get category detail
    - PUT /admin-panel/categories/{id}/ - Update category
    - DELETE /admin-panel/categories/{id}/ - Delete category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    pagination_class = AdminPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'id']
    ordering = ['name']

    def get_queryset(self):
        """Get categories with project count"""
        return Category.objects.all()

    def perform_create(self, serializer):
        """Create new category"""
        serializer.save()

    def perform_update(self, serializer):
        """Update category"""
        serializer.save()
