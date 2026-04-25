from rest_framework.pagination import CursorPagination, Response
import os

class CustomCursorPagination(CursorPagination):
    page_size = 12
    ordering = 'id'

    def _replace_host(self, link):
        if not link:
            return link
        api_host = os.getenv('API_GATEWAY_URL', '')
        if api_host:
            from urllib.parse import urlparse, urlunparse
            parsed = urlparse(link)
            gateway = urlparse(api_host)
            link = urlunparse(parsed._replace(scheme=gateway.scheme, netloc=gateway.netloc))
        return link

    def paginate_queryset(self, queryset, request, view=None):
        self.count = queryset.count()
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'next': self._replace_host(self.get_next_link()),
            'previous': self._replace_host(self.get_previous_link()),
            'count': self.count,
            'results': data
        })
