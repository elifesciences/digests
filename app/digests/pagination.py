from django.conf import settings

from rest_framework import pagination
from rest_framework.response import Response


class DigestPagination(pagination.PageNumberPagination):

    page_query_param = 'page'
    page_size = 20
    page_size_query_param = 'per-page'
    content_type = settings.DIGESTS_CONTENT_TYPE

    def get_paginated_response(self, data):
        return Response(
            {
                'total': self.page.paginator.count,
                'items': data
            },
            content_type=self.content_type
        )
