from django.conf import settings
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

import datetime

# Create your models here.


class Book(models.Model):

    CURRENT_YEAR = datetime.date.today().year
    MIN_LEN_BOOK_DESCRIPTION = 100

    cover_image = models.ImageField(
        upload_to="static/images/",
        default='static/images/book_cover_no_img.jpg',
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
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(CURRENT_YEAR)
        ]
    )

    # add category and cover image

    category = models.ManyToManyField(
        'category.Category',
        blank=False,
        default="Not set yet"
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
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        editable=False,
        null=True,
    )
    @property
    def get_added_by(self):
        if self.added_by is None:
            return "Anonymous"
        return self.added_by.username

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        if not self.added_by:
            self.added_by = kwargs.pop('user', None)

        super(Book, self).save(*args, **kwargs)


