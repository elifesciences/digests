from django.http import HttpResponse


# pylint: disable=W0613
def ping(request):
    return HttpResponse('pong', status=200)
