from collections import ChainMap
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

    @staticmethod
    def _validate_against_schema(request: Request, data: Dict) -> None:
        schema = get_schema(get_schema_name(request.content_type))
        validate_json(data, schema=schema)

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            self._validate_against_schema(request, data=request.data)

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

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()

            if partial:
                existing_instance = self.get_serializer(instance)

                self._validate_against_schema(request, data=dict(ChainMap(request.data, existing_instance.data)))

            # validating the actual table fields as using the rules defined in the `Digest` model
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        except ValidationError as err:
            err.code = status.HTTP_400_BAD_REQUEST
            return validation_error_handler(err)
