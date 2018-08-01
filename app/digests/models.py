from django.db import models
from django.contrib.postgres.fields import JSONField


DIGEST_ID_FORMAT = r'^[A-Za-z0-9\-._]+$'

PREVIEW = 'preview'
PUBLISHED = 'published'

DIGEST_STAGES = (
    (PREVIEW, 'preview'),
    (PUBLISHED, 'published'),
)


class Digest(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    content = JSONField()
    image = JSONField()
    impactStatement = models.TextField(blank=True, null=True)
    published = models.DateTimeField(null=True)
    relatedContent = JSONField()
    stage = models.CharField(max_length=25, choices=DIGEST_STAGES, default=PREVIEW)
    subjects = JSONField(null=True)
    title = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return f'{self.id}: {self.title}'
