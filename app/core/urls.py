from django.urls import path
from .views import ping


URLPATTERNS = [
    path('ping', ping),
]

# pylint: disable=C0103
urlpatterns = URLPATTERNS
