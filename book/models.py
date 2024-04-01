import os

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

import datetime

from django.contrib.auth import models as auth_models


# Create your models here.
def custom_upload_to(instance, filename):
    base_filenmae, file_extension = os.path.splitext(filename)

    unique_filename = f"{base_filenmae}_{instance.pk}{file_extension}"

    return os.path.join('images', unique_filename)


class Book(models.Model):
    DEFAULT_BOOK_COVER = 'static/images/no_cover.jpg'

    CURRENT_YEAR = datetime.date.today().year
    MIN_LEN_BOOK_DESCRIPTION = 100

    MIN_YEAR_ADDED_VALUE = 1000
    SUPER_USER_EMAIL = 'denny@gmail.com'

    cover_image = models.ImageField(
        upload_to='cover_images',
        default='no_cover.jpg',
    )

    title = models.CharField(
        unique=True,
        max_length=100,
        blank=False,
        null=False,
    )

    author = models.ForeignKey(
        'author.Author',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )

    year_published = models.PositiveIntegerField(
        blank=False,
        null=False,
        default=CURRENT_YEAR,
        help_text=f"If the book you are trying to add was published before {MIN_YEAR_ADDED_VALUE},\n"
                  f"please contact the administrator at {SUPER_USER_EMAIL}.",

        validators=[
            MinValueValidator(MIN_YEAR_ADDED_VALUE),
            MaxValueValidator(CURRENT_YEAR)
        ]

    )

    # add category and cover image

    categories = models.ManyToManyField(
        'category.Category',
        blank=False,
        help_text=f"If you can`t find the category you need,\n"
                  f"please contact the administrator at {SUPER_USER_EMAIL}."
    )

    description = models.TextField(
        max_length=1_000,
        blank=False,
        null=True,
        help_text=f"Describe the book in at least {MIN_LEN_BOOK_DESCRIPTION} characters.",
        validators=[
            MinLengthValidator(MIN_LEN_BOOK_DESCRIPTION),
        ]
    )

    added_by = models.ForeignKey(
        'bookie.Bookie',
        on_delete=models.SET_NULL,
        editable=False,
        null=True,
    )

    def save(self, *args, **kwargs):

        if not self.added_by:
            self.added_by = kwargs.pop('user', None)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def overall_rating(self):
        total_reviews = self.book_reviews.all()
        if total_reviews:
            total_rating = sum(rat.rating for rat in total_reviews)
            return total_rating / len(total_reviews)
        return 0
