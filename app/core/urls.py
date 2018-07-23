from django.urls import path
from .views import ping


URLPATTERNS = [
    path('ping', ping),
]

urlpatterns = URLPATTERNS
