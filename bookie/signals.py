
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import bookie.models
from bookie.models import BookieProfile, Bookie
from django.db.models.signals import m2m_changed


@receiver(post_save, sender=Bookie)
def create_profile(sender, instance, created, **kwargs):
    if created:
        BookieProfile.objects.create(user=instance, pk=instance.pk)

@receiver(post_delete, sender=Bookie)
def delete_the_associated_profile(sender, instance, **kwargs):
    try:
        instance.profile.delete()

    except BookieProfile.DoesNotExist:
        pass

