from django.db import models

from book.models import Book
from bookie.models import Bookie

# Create your models here.


class ReviewAndRating(models.Model):

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='book_reviews'
    )

    user = models.ForeignKey(
        Bookie,
        on_delete=models.SET_NULL,
        null=True,
    )

    review = models.TextField(
        max_length=100,
        blank=True
    )

    rating = models.FloatField(
    )

    has_voted = models.BooleanField(
        default=False,
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.save()

    def __str__(self):
        return self.review


