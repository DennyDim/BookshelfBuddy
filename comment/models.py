
from django.db import models

# Create your models here.

class Comment(models.Model):


    text = models.TextField(
        max_length=1_000,
        blank=False,
    )

    commented_by = models.ForeignKey(
        'bookie.Bookie',
        on_delete=models.CASCADE,
        null=True,
        editable=False,
    )

    book = models.ForeignKey(
        'book.Book',
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True,
        blank=True
    )
