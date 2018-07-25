from typing import Any, Dict

from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response

from digests.models import Digest
from digests.pagination import DigestPagination
from digests.serializers import DigestSerializer


class DigestViewSet(viewsets.ModelViewSet):
    model = Digest
    queryset = Digest.objects.all()
    serializer_class = DigestSerializer
    pagination_class = DigestPagination

    content_type = settings.DIGESTS_CONTENT_TYPE

    def _create_response(self, data: Dict[str, Any]) -> Response:
        return Response(data, content_type=self.content_type)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return self._create_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self._create_response(serializer.data)
