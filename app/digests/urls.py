from django.urls import path, include

from rest_framework import routers

from digests.api import DigestViewSet


router_v1 = routers.DefaultRouter(trailing_slash=False)
router_v1.register('digests', DigestViewSet, base_name='digests')


urlpatterns = [
    path('', include((router_v1.urls, 'api_v1'))),
]
