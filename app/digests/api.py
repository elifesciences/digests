from typing import Any, Dict

from django.conf import settings

from jsonschema import validate as validate_json
from jsonschema import ValidationError
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from digests.exceptions import validation_error_handler
from digests.models import Digest
from digests.pagination import DigestPagination
from digests.serializers import DigestSerializer
from digests.utils import get_schema, get_schema_name


class DigestViewSet(viewsets.ModelViewSet):
    model = Digest
    queryset = Digest.objects.all()
    serializer_class = DigestSerializer
    pagination_class = DigestPagination

    content_type = settings.DIGEST_CONTENT_TYPE
    list_content_type = settings.DIGESTS_CONTENT_TYPE

    def _create_response(self, data: Dict[str, Any]) -> Response:
        return Response(data, content_type=self.content_type)

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            schema = get_schema(get_schema_name(request.content_type))

            # validating entire `json` against the externally defined schema
            validate_json(request.data, schema=schema)

            # validating the actual table fields as using the rules defined in the `Digest` model
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except ValidationError as err:
            err.code = status.HTTP_400_BAD_REQUEST
            return validation_error_handler(err)

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, content_type=self.list_content_type)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, content_type=self.content_type)
