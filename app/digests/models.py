from logging import getLogger

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from elife_bus_sdk import get_publisher
from elife_bus_sdk.events import Event


LOGGER = getLogger(__name__)

event_publisher = get_publisher(config=settings.ELIFE_BUS)

DIGEST_ID_FORMAT = r'^[A-Za-z0-9\-._]+$'

PREVIEW = 'preview'
PUBLISHED = 'published'

DIGEST_STAGES = (
    (PREVIEW, 'preview'),
    (PUBLISHED, 'published'),
)


class Digest(models.Model):
    id = models.CharField(primary_key=True, db_index=True, max_length=255)
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


@receiver(post_save, sender=Digest)
def send_event(sender, instance, created, **kwargs):
    try:
        # could add a `DigestEvent` to `elife_bus_sdk`
        # to replace the `Event` here, though functionality will not change.
        event_publisher.publish(Event(id=instance.id))
    except (AttributeError, RuntimeError):
        LOGGER.exception(f'Failed to send event for Digest {instance.id}')
