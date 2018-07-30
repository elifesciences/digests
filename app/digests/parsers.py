from django.conf import settings
from rest_framework.parsers import JSONParser


class DigestsParser(JSONParser):
    media_type = settings.DIGEST_CONTENT_TYPE
