from django.db import models
from django.contrib.postgres.fields import JSONField

DIGEST_ID_FORMAT = r'^[A-Za-z0-9\-._]+$'


class Digest(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    content = JSONField()
    image = JSONField()
    impactStatement = models.TextField(blank=True, null=True)
    published = models.DateTimeField()
    relatedContent = JSONField()
    subjects = JSONField(null=True)
    title = models.CharField(max_length=255)
    updated = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.id}: {self.title}'
