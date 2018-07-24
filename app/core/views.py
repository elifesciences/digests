from django.http import HttpResponse


# pylint: disable=unused-argument
def ping(request):
    return HttpResponse('pong', status=200)
