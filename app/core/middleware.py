from logging import getLogger
from typing import Callable

from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse

LOGGER = getLogger(__name__)


def _set_can_modify(request: HttpRequest, state: bool) -> HttpRequest:
    request.META[settings.AUTHORIZATION_MODIFICATION_HEADER] = state
    return request


def _set_can_preview(request: HttpRequest, state: bool) -> HttpRequest:
    request.META[settings.AUTHORIZATION_PREVIEW_HEADER] = state
    return request


def kong_authentication(get_response: Callable[[HttpRequest], HttpResponse]) \
        -> Callable[[HttpRequest], HttpResponse]:
    def middleware(request: HttpRequest):
        can_preview = False
        can_modify = False

        groups_header = request.META.get(settings.CONSUMER_GROUPS_HEADER, None)

        if groups_header:
            groups = [group.strip() for group in groups_header.split(',')]

            LOGGER.debug('user groups: %s', groups)
            if 'view-unpublished-content' in groups:
                can_preview = True
            else:
                LOGGER.debug('setting request as user cannot view unpublished content/cannot preview')

            if 'edit-digests' in groups:
                can_modify = True
            else:
                LOGGER.debug('setting request as user cannot modify digests')

        request = _set_can_preview(_set_can_modify(request, can_modify), can_preview)

        return get_response(request)

    return middleware
