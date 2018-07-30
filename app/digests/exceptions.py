import logging
from typing import List

from django.conf import settings
from rest_framework.response import Response

LOGGER = logging.getLogger(__name__)


def format_error_path(path: List[str]) -> str:
    return '.'.join([str(item) for item in path])


def generate_error_string(message: str, path: List[str]) -> str:
    equals_str = ''
    if len(path):
        equals_str = ' = '

    return '{0}{1}{2}'.format(format_error_path(path), equals_str, message)


def validation_error_handler(exception: Exception) -> Response:
    err_msg = generate_error_string(message=exception.message, path=exception.path)
    LOGGER.exception(err_msg)
    return Response(
        {'title': err_msg},
        status=exception.code,
        content_type=settings.ERROR_CONTENT_TYPE
    )
