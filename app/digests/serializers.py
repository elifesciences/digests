from rest_framework import serializers

from digests.models import Digest


class DigestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Digest
        fields = (
            'id',
            'title',
            'impactStatement',
            'published',
            'updated',
            'image',
            'subjects',
            'content',
            'relatedContent',
        )
