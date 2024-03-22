
from django.db.models.signals import post_save
from django.dispatch import receiver

from bookie.models import BookieProfile, Bookie

from django.db.models.signals import m2m_changed


@receiver(post_save, sender=Bookie)
def create_profile(sender, instance, created, **kwargs):
    if created:
        BookieProfile.objects.create(user=instance)
        instance.bookieprofile.save()


@receiver(m2m_changed, sender=BookieProfile.books_i_want_to_read.through)
def update_want_to_read_library(sender, instance, action, **kwargs):
    if action == 'post_add':
        library = sender.bookieprofile.books_i_want_to_read.all()
        library.append(instance)


@receiver(m2m_changed, sender=BookieProfile.books_ive_read.through)
def update_have_read_library(sender, instance, action, **kwargs):
    if action == 'post_add':
        library = sender.bookieprofile.books_ive_read.all()
        library.append(instance)