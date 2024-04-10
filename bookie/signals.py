
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from bookie.models import BookieProfile, Bookie


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

