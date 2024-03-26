from django.conf import settings
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

import datetime

# Create your models here.


class Book(models.Model):

    DEFAULT_BOOK_COVER = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPa8pabMznsqT-GWDJccgg3uLBcnSwOpIXrA&usqp=CAU"

    CURRENT_YEAR = datetime.date.today().year
    MIN_LEN_BOOK_DESCRIPTION = 100

    MIN_YEAR_ADDED_VALUE = 1000
    SUPER_USER_EMAIL = 'denny@gmail.com'

    cover_image = models.URLField(
        default=DEFAULT_BOOK_COVER,
        blank=True,
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
        help_text= f"If the book you are trying to add was published before {MIN_YEAR_ADDED_VALUE},\n"
                   f"please contact the administrator at {SUPER_USER_EMAIL}.",

        validators=[
            MinValueValidator(MIN_YEAR_ADDED_VALUE),
            MaxValueValidator(CURRENT_YEAR)
        ]

    )

    # add category and cover image

    categories = models.ManyToManyField(
        'book.Category',
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
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        editable=False,
        null=True,
    )

    def save(self, *args, **kwargs):

        if not self.added_by:
            self.added_by = kwargs.pop('user', None)

        if not self.pk:
            super().save(*args, **kwargs)

            return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author}"



class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )

    age_restriction = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=None,
        validators=[
            MaxValueValidator(50),
        ]
    )

    books = models.ManyToManyField(
        Book,
        related_name='books_in_category',

    )

    @property
    def get_age_restriction(self):
        if self.age_restriction:
            return f"({self.age_restriction})"
        else:
            return ''

    def get_book_count(self):
        return self.book_set.count()

    def __str__(self):
        return f"{self.name}{self.get_age_restriction}\nBooks: {self.get_book_count()}"

