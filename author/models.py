
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models

import datetime

# Create your models here.



class Author(models.Model):

    MIN_AUTHOR_BIO_CHARS = 40

    CURRENT_YEAR = datetime.datetime.today().year

    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Author name",
        error_messages={"unique": "Author with this name already exists."}
    )

    year_born = models.PositiveIntegerField(
        blank=False,
        null=False,
        default=1_000,
        verbose_name="Author`s birth year",
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(CURRENT_YEAR)
        ]
    )

    author_picture = models.ImageField(
        upload_to="images/",
        default='images/no_profile_pic.jpg',
    )

    authors_bio = models.TextField(
        max_length=1_000,
        blank=False,
        null=False,
        help_text=f"A brief description of the author. Use at least {MIN_AUTHOR_BIO_CHARS} characters.",
        validators=[
            MinLengthValidator(MIN_AUTHOR_BIO_CHARS),
        ]

    )

    def get_book_titles(self) -> list:
        return [book.title for book in self.book_set.all()]

    def get_book_categories(self):
        all_categories = {}
        for book in self.book_set.all():
            for c in book.category.all():
                if c not in all_categories:
                    all_categories[c] = 0
                all_categories[c] += 1

        return sorted(all_categories, key=lambda x: all_categories.get(x), reverse=True)

    def __str__(self):
        return self.name
