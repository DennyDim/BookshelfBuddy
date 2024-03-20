
from django.db.models.signals import post_save
from django.dispatch import receiver

from bookie.models import BookieProfile, Bookie


@receiver(post_save, sender=Bookie)
def create_profile(sender, instance, created, **kwargs):
    if created:
        BookieProfile.objects.create(user=instance)
        instance.bookieprofile.save()
