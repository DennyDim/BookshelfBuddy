from django.contrib import admin
from django.contrib.admin import SimpleListFilter

import time

from django.db import models

from book.models import Book
from bookie.models import Bookie


class ReviewAndRating(models.Model):

    TYPE_CHOICES = (
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    )

    book = models.ForeignKey(
        'book.Book',
        on_delete=models.CASCADE,
        related_name='book_reviews',
        null=True,
    )

    user = models.ForeignKey(
        Bookie,
        on_delete=models.SET_NULL,
        null=True,
    )

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='Neutral'
    )

    review = models.TextField(
        blank=True,
        null=True
    )

    rating = models.FloatField(
        null=True,
    )

    has_voted = models.BooleanField(
        default=False,
        )

    date_added = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.pk:
            self.date_added = time.time()

        self.book.save()

    def __str__(self):
        return self.review


class FilterByRating(SimpleListFilter):
    title = "Rating"
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return (
            ("high_rated", "Highest Ratings"),
            ("low_rated", "Lowest Ratings")
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        elif self.value() == "high_rated":
            return queryset.filter(rating__gt=0).order_by("-rating")

        elif self.value() == "low_rated":
            return queryset.filter(rating__gt=0).order_by("rating")


class ReviewAndRatingAdmin(admin.ModelAdmin):
    list_display = ('rating', "date_added", "user", "book", "rating")
    list_filter = (FilterByRating, )
    search_fields = ("user", "book")
