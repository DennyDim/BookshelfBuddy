
from django.db import models


from django.contrib.auth import models as auth_models

# Create your models here.


class Bookie(auth_models.AbstractUser):

    age = (
        models.PositiveIntegerField(
            blank=False,
            null=False,
            default=18,
        )
    )

    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        error_messages={"unique": "Another bookie is already using that email."},
    )

    def __str__(self):
        return self.username


class BookieProfile(models.Model):

    DEFAULT_USER_IMAGE = "https://www.pngitem.com/pimgs/m/22-223978_transparent-no-avatar-png-pyrenees-png-download.png"

    #   from here we get username, age and email

    user = models.OneToOneField(
        'bookie.Bookie',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile"
    )

    email = models.EmailField(blank=True, null=True)

    profile_picture = models.URLField(
        blank=True,
        default=DEFAULT_USER_IMAGE,
    )

    bio = models.TextField(
        blank=True,
        max_length=250,
        default="Share something about yourself in 250 characters or less."
    )
    want_to_read = models.ManyToManyField(
        'book.Book',
        blank=True,
        default=None,
        related_name='want_to_read',
    )

    have_read = models.ManyToManyField(
        'book.Book',
        blank=True,
        default=None,
        related_name="have_read"
    )

    def __str__(self):
        return f"{self.user.username.capitalize()}'s Profile"

    def save(self, *args, **kwargs):
        self.email = self.user.email
        super(BookieProfile, self).save(*args, **kwargs)




