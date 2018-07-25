from rest_framework import viewsets

from digests.models import Digest
from digests.serializers import DigestSerializer


class DigestViewSet(viewsets.ModelViewSet):
    model = Digest
    queryset = Digest.objects.all()
    serializer_class = DigestSerializer
