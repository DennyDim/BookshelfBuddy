from django.utils import timezone

import time

from django.db import models

from book.models import Book
from bookie.models import Bookie

# Create your models here.


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
