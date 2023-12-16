from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'page_size': len(self.page.object_list),
            'total_page_count': self.page.paginator.num_pages,
            'total_count': self.page.paginator.count,
            'results': data
        })
