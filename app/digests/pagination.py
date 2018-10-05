from django.conf import settings

from rest_framework import pagination
from rest_framework.response import Response

from digests.exceptions import PaginationError


class DigestPagination(pagination.PageNumberPagination):

    page_query_param = 'page'
    page_size = 20
    max_page_size = 100
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

    @staticmethod
    def validate_parameters(page_parameter, per_page_parameter):
        if page_parameter is not None:
            try:
                page = int(page_parameter)
            except ValueError as err:
                raise PaginationError(f'`page` parameter is invalid') from err

            if not page >= 1:
                raise PaginationError(f'`page` parameter is too small')

        if per_page_parameter is not None:
            try:
                per_page = int(per_page_parameter)
            except ValueError as err:
                raise PaginationError(f'`per-page` parameter is invalid') from err

            if not per_page >= 1:
                raise PaginationError(f'`per-page` parameter is too small')
            if not per_page <= DigestPagination.max_page_size:
                raise PaginationError(f'`per-page` parameter is too large')
