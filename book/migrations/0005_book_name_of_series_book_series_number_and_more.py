# Generated by Django 5.0.2 on 2024-04-06 13:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_deletedbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='name_of_series',
            field=models.CharField(blank=True, help_text='Add name of series only if there are pre/sequels to the book.\nKeep in mind this field is case-sensitive.', max_length=100, null=True, verbose_name='Name of Series'),
        ),
        migrations.AddField(
            model_name='book',
            name='series_number',
            field=models.IntegerField(blank=True, help_text='Required only if the book belongs to series.', null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Series number'),
        ),
        migrations.DeleteModel(
            name='DeletedBook',
        ),
    ]