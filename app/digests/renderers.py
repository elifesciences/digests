from django.conf import settings
from rest_framework.renderers import JSONRenderer


class DigestRenderer(JSONRenderer):
    media_type = settings.DIGEST_CONTENT_TYPE


class DigestsRenderer(JSONRenderer):
    media_type = settings.DIGESTS_CONTENT_TYPE
