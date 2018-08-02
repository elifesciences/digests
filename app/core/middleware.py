from logging import getLogger
from typing import Callable

from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse

LOGGER = getLogger(__name__)


def _set_can_modify(request: HttpRequest, state: bool) -> HttpRequest:
    request.META[settings.KONG_MODIFICATION_HEADER] = state
    return request


def _set_authenticated(request: HttpRequest, state: bool) -> HttpRequest:
    request.META[settings.KONG_AUTH_HEADER] = state
    return request


def kong_authentication(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    def middleware(request: HttpRequest):
        authenticated = False
        can_modify = False

        groups_header = request.META.get(settings.CONSUMER_GROUPS_HEADER, None)

        if groups_header:
            groups = [group.strip() for group in groups_header.split(',')]

            LOGGER.debug('user groups: %s', groups)
            if 'view-unpublished-content' in groups:
                authenticated = True
            else:
                LOGGER.debug('setting request as not authenticated')

            if 'edit-digests' in groups:
                can_modify = True
            else:
                LOGGER.debug('setting request as user cannot modify digests')

        request = _set_authenticated(_set_can_modify(request, can_modify), authenticated)

        return get_response(request)

    return middleware
