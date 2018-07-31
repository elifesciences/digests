from rest_framework import serializers

from digests.models import Digest


class CreateDigestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Digest
        fields = (
            'id',
            'title',
            'impactStatement',
            'stage',
            'published',
            'updated',
            'image',
            'subjects',
            'content',
            'relatedContent',
        )


class DigestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Digest
        read_only_fields = ('id',)
        fields = (
            'id',
            'title',
            'impactStatement',
            'stage',
            'published',
            'updated',
            'image',
            'subjects',
            'content',
            'relatedContent',
        )
