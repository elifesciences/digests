from django.urls import include, path
from .views import ping


URLPATTERNS = [
    path('ping', ping),
    path('', include('digests.urls')),
]

# pylint: disable=invalid-name
urlpatterns = URLPATTERNS
