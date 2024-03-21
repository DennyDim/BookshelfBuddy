from django.core import validators
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

    #   from here we get username, age and email

    user = models.OneToOneField(
        Bookie,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    profile_picture = models.ImageField(
        default='static/images/no_profile_pic.png',
        upload_to='static/images/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        max_length=250,
        default="Tell something about yourself in 250 characters or less."
    )

    books_i_want_to_read = models.ManyToManyField(
        "book.Book",
        related_name="books_wanted_by_users",
        blank=True,
    )

    books_ive_read = models.ManyToManyField(
        "book.Book",
        related_name="books_read_by_users",
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username.capitalize()}'s Profile"
