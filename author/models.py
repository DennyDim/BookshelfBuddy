
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models

import datetime



class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"



class Author(models.Model):

    MIN_AUTHOR_BIO_CHARS = 40
    MIN_YEAR_BORN = 1_000
    CURRENT_YEAR = datetime.datetime.today().year

    name = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=False,
        verbose_name="Author name",
    )

    pseudonym = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    year_born = models.PositiveIntegerField(
        blank=False,
        null=False,
        default=CURRENT_YEAR,
        verbose_name="Author`s birth year",
        validators=[
            MinValueValidator(MIN_YEAR_BORN),
            MaxValueValidator(CURRENT_YEAR)
        ]
    )

    country = models.ForeignKey(
        
        'author.Country',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )

    author_picture = models.ImageField(
        upload_to="authors_pictures",
        default='no_profile.png',
    )

    authors_bio = models.TextField(
        max_length=1_000,
        help_text=f"Use at least {MIN_AUTHOR_BIO_CHARS} characters.",
        validators=[
            MinLengthValidator(MIN_AUTHOR_BIO_CHARS),
        ])

    people_who_like_this_author = models.ManyToManyField(
        'bookie.Bookie',
        related_name='author_likes',
        blank=True
    )

    @property
    def get_name(self):
        if self.pseudonym:
            return f"{self.name}({self.pseudonym})"
        else:
            return self.name

    def __str__(self):
        return self.get_name

    def get_book_categories(self):
        
        all_categories = {}
        for book in self.book_set.all():
            for c in book.genres.all():
                if c not in all_categories:
                    all_categories[c] = 0
                all_categories[c] += 1

        return sorted(all_categories, key=lambda x: all_categories.get(x), reverse=True)



