from django.http import HttpResponse
from django.views.decorators.cache import patch_cache_control


# pylint: disable=unused-argument
def ping(request):
    response = HttpResponse('pong', status=200)
    patch_cache_control(response, **{
        'must-revalidate': True,
        'no-cache': True,
        'no-store': True,
        'private': True,
    })
    return response
