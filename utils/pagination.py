from rest_framework.pagination import CursorPagination, Response

class CustomCursorPagination(CursorPagination):
    page_size = 12
    ordering = 'id'

    def paginate_queryset(self, queryset, request, view=None):
        # Capture the count before the queryset is sliced for the page
        self.count = queryset.count()
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        # Add 'count' to the default response dictionary
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.count,  # Injected count
            'results': data
        })