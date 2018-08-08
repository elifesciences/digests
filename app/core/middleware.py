from logging import getLogger
from typing import Callable

from django.conf import settings
from django.http.request import HttpRequest as Request
from django.http.response import HttpResponse as Response
from django.views.decorators.cache import patch_cache_control

LOGGER = getLogger(__name__)


def _set_can_modify(request: Request, state: bool) -> Request:
    request.META[settings.AUTHORIZATION_MODIFICATION_HEADER] = state
    return request


def _set_can_preview(request: Request, state: bool) -> Request:
    request.META[settings.AUTHORIZATION_PREVIEW_HEADER] = state
    return request


def kong_authentication(get_response: Callable[[Request], Response]) \
        -> Callable[[Request], Response]:
    def middleware(request: Request):
        can_preview = False
        can_modify = False

        groups_header = request.META.get(settings.CONSUMER_GROUPS_HEADER, None)

        if groups_header:
            groups = [group.strip() for group in groups_header.split(',')]

            LOGGER.debug('user groups: %s', groups)
            if 'view-unpublished-content' in groups:
                can_preview = True
            else:
                LOGGER.debug('setting request as user cannot view '
                             'unpublished content/cannot preview')

            if 'edit-digests' in groups:
                can_modify = True
            else:
                LOGGER.debug('setting request as user cannot modify digests')

        request = _set_can_preview(_set_can_modify(request, can_modify), can_preview)

        return get_response(request)

    return middleware


def downstream_caching(get_response: Callable[[Request], Response]) \
        -> Callable[[Request], Response]:
    def middleware(request: Request):
        public_headers = {
            'public': True,
            'max-age': 60 * 5,
            'stale-while-revalidate': 60 * 5,
            'stale-if-error': (60 * 60) * 24,
        }

        private_headers = {
            'private': True,
            'max-age': 0,
            'must-revalidate': True,
        }

        response = get_response(request)

        if request.META.get(settings.AUTHORIZATION_PREVIEW_HEADER, False):
            cache_headers = private_headers
        else:
            cache_headers = public_headers

        patch_cache_control(response, **cache_headers)

        return response

    return middleware
