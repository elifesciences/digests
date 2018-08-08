from collections import ChainMap
from logging import getLogger
from typing import Any, Dict

from django.conf import settings
from django.db import transaction

from django_filters.rest_framework import DjangoFilterBackend
from jsonschema import validate as validate_json
from jsonschema import ValidationError
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from digests.events import DigestEvent
from digests.exceptions import validation_error_handler
from digests.models import Digest, PUBLISHED
from digests.pagination import DigestPagination
from digests.serializers import CreateDigestSerializer, DigestSerializer
from digests.utils import get_schema, get_schema_name
from elife_bus_sdk import get_publisher


LOGGER = getLogger(__name__)

event_publisher = get_publisher(config=settings.ELIFE_BUS)


class DigestViewSet(viewsets.ModelViewSet):
    model = Digest
    queryset = Digest.objects.all()
    serializer_class = DigestSerializer
    pagination_class = DigestPagination
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('stage',)
    instance = None

    content_type = settings.DIGEST_CONTENT_TYPE
    list_content_type = settings.DIGESTS_CONTENT_TYPE

    def _can_modify(self) -> bool:
        return self.request.META.get(settings.AUTHORIZATION_MODIFICATION_HEADER, False)

    def _create_response(self, data: Dict[str, Any]) -> Response:
        return Response(data, content_type=self.content_type)

    def _can_preview(self) -> bool:
        return self.request.META.get(settings.AUTHORIZATION_PREVIEW_HEADER, False)

    @staticmethod
    def _publish_event(instance: Digest) -> None:
        try:
            # could add a `DigestEvent` to `elife_bus_sdk`
            # to replace the `Event` here, though functionality will not change.
            LOGGER.info('_publish_event call for %s' % instance.id)
            event_publisher.publish(DigestEvent(id=instance.id))
        except (AttributeError, RuntimeError):
            LOGGER.exception(f'Failed to publish event for digest {instance.id}')

    @staticmethod
    def _validate_against_schema(request: Request, data: Dict) -> None:
        schema = get_schema(get_schema_name(request.content_type))
        validate_json(data, schema=schema)

    def get_queryset(self):
        if self._can_preview():
            return Digest.objects.all()
        else:
            return Digest.objects.filter(stage=PUBLISHED)

    def create(self, request: Request, *args, **kwargs) -> Response:
        if not self._can_modify() or not self._can_preview():
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            self._validate_against_schema(request, data=request.data)
            with transaction.atomic():
                # validating the actual table fields as using the rules defined in the `Digest` model
                serializer = CreateDigestSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()

                transaction.on_commit(lambda: self._publish_event(instance))

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
        if not self._can_modify() or not self._can_preview():
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            partial = kwargs.pop('partial', False)

            with transaction.atomic():
                self.instance = self.get_object()

                if partial:
                    # validatation for `PATCH` request
                    existing_instance = self.get_serializer(self.instance)
                    new_data = dict(ChainMap(request.data, existing_instance.data))
                else:
                    # validation for `PUT` request
                    new_data = request.data

                self._validate_against_schema(request, data=new_data)

                # validating the actual table fields as using the rules defined in the `Digest` model
                serializer = self.get_serializer(self.instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                transaction.on_commit(lambda: self._publish_event(self.instance))

            return Response(serializer.data)

        except ValidationError as err:
            err.code = status.HTTP_400_BAD_REQUEST
            return validation_error_handler(err)
