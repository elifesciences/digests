import json
import os
from typing import Any, Dict

from django.conf import settings
from elife_api_validator import SCHEMA_DIRECTORY
from jsonschema import validate as validate_json
from jsonschema import ValidationError
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from digests.exceptions import validation_error_handler
from digests.models import Digest
from digests.pagination import DigestPagination
from digests.serializers import DigestSerializer


def get_schema(schema_name: str) -> Dict:
    with open(os.path.join(SCHEMA_DIRECTORY, schema_name)) as schema:
        val = json.loads(schema.read())
        return val


class DigestViewSet(viewsets.ModelViewSet):
    model = Digest
    queryset = Digest.objects.all()
    serializer_class = DigestSerializer
    pagination_class = DigestPagination

    content_type = settings.DIGESTS_CONTENT_TYPE
    schema_name = 'digest.v1.json'

    def _create_response(self, data: Dict[str, Any]) -> Response:
        return Response(data, content_type=self.content_type)

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            validate_json(request.data, schema=get_schema(self.schema_name))
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
        return self._create_response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self._create_response(serializer.data)
