from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.


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

    @property
    def get_age_restriction(self):
        if self.age_restriction:
            return f" ({self.age_restriction})"
        else:
            return ''

    def __str__(self):
        return f"{self.name}{self.get_age_restriction}"