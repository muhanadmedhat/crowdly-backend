from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardPagination(PageNumberPagination):
    page_size = 12                     # default
    page_size_query_param = 'page_size' # e.g. ?page_size=6
    max_page_size = 100                # hard cap

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # total items
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
# if you want to disable pagination for a specific view, set pagination_class = None in that view.
    
