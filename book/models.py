from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.db import models

import datetime

from bookie.models import Bookie


class Book(models.Model):
    CURRENT_YEAR = datetime.date.today().year
    MIN_YEAR_ADDED_VALUE = 1000

    MAX_LEN_BOOK_TITLE = 100
    MAX_LEN_AUTHOR_NAME = 100

    MIN_LEN_BOOK_DESCRIPTION = 100
    MAX_LEN_BOOK_DESCRIPTION = 1_000

    MAX_SERIES_NAME_LENGTH = 100
    MIN_VALUE_FOR_NUMBER_SERIES = 1

    SUPER_USER_EMAIL = 'denny@gmail.com'
    SUPERUSER_PK = 14

    cover_image = models.ImageField(
        upload_to='cover_images',
        default='no_cover.jpg',
    )

    title = models.CharField(
        max_length=MAX_LEN_BOOK_TITLE,
        blank=False,
        null=True,
    )

    author = models.ForeignKey(
        'author.Author',
        on_delete=models.CASCADE,
        max_length=MAX_LEN_AUTHOR_NAME,
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

    genres = models.ManyToManyField(
        'Genre.Genre',
        blank=False,
        help_text=f"If you can`t find the Genre you need,\n"
                  f"please contact the administrator at {SUPER_USER_EMAIL}."
    )

    description = models.TextField(
        max_length=MAX_LEN_BOOK_DESCRIPTION,
        blank=False,
        null=True,
        help_text=f"Describe the book in at least {MIN_LEN_BOOK_DESCRIPTION} characters.",
        validators=[
            MinLengthValidator(MIN_LEN_BOOK_DESCRIPTION),
            MaxLengthValidator(MAX_LEN_BOOK_DESCRIPTION)
        ]
    )

    name_of_series = models.CharField(
        max_length=MAX_SERIES_NAME_LENGTH,
        blank=True,
        null=True,
        verbose_name="Name of Series",
        help_text='Add name of series only if there are pre/sequels to the book.\n'
                  'Keep in mind this field is case-sensitive.'
    )

    series_number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Series number",
        validators=([
            MinValueValidator(MIN_VALUE_FOR_NUMBER_SERIES)
        ]),
        help_text="Required only if the book belongs to series."
    )

    added_by = models.ForeignKey(
        'bookie.Bookie',
        on_delete=models.SET_NULL,
        null=True,
    )

    added_on_date = models.DateField(
        blank=True,
        null=True,
    )

    last_edited_on_date = models.DateField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def overall_rating(self):
        total_reviews = self.book_reviews.all()
        if total_reviews:
            total_rating = sum(rat.rating for rat in total_reviews)
            result = total_rating / len(total_reviews)
            return result
        return 0

    @property
    def required_age(self):
        age = 0
        for genre in self.genres.all():
            if genre.age_restriction and genre.age_restriction > age:
                age = genre.age_restriction

        return age


class SortByAddedOnDate(SimpleListFilter):
    title = "Added on"
    parameter_name = 'added_on_date'

    def lookups(self, request, model_admin):
        return (
            ('newly_added', "Newest Books"),
            ('old_books', 'Oldest Books')
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        elif self.value() == "newly_added":
            return queryset.order_by("-added_on_date")
        elif self.value() == "old_books":
            return queryset.order_by("added_on_date")


class FilterBookEditedOnDate(SimpleListFilter):
    title = "Edit date"
    parameter_name = 'last_edited_on_date'

    def lookups(self, request, model_admin):
        return (
            ('newly_edited', "Newest edits"),
            ('first_edited', 'Oldest edits')
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        elif self.value() == "newly_edited":
            return queryset.order_by("-last_edited_on_date")
        elif self.value() == "first_edited":
            return queryset.order_by("last_edited_on_date")


class BookAdmin(admin.ModelAdmin):
    list_display = ('added_on_date', 'title',)
    list_filter = (SortByAddedOnDate, FilterBookEditedOnDate)
    search_fields = ('title', 'author__name')
