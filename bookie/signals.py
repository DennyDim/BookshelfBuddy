
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import bookie.models
from bookie.models import BookieProfile, Bookie
from django.db.models.signals import m2m_changed


@receiver(post_save, sender=Bookie)
def create_profile(sender, instance, created, **kwargs):
    if created:
        BookieProfile.objects.create(user=instance)



@receiver(post_delete, sender=BookieProfile)
def delete_the_associated_user(sender, instance, **kwargs):
    try:
        instance.user.delete()

    except Bookie.DoesNotExist:
        pass

