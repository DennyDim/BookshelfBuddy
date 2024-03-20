from django.conf import settings
from django.db import models

# Create your models here.

class Comment(models.Model):

    commented_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
    )

    text = models.TextField(
        max_length=1_000,
        blank=False,
    )

    book = models.ForeignKey(
        'book.Book',
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True,
        blank=True
    )
