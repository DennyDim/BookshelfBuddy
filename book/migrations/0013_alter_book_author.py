# Generated by Django 5.0.2 on 2024-04-09 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0012_alter_country_options_alter_author_country'),
        ('book', '0012_remove_book_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='author.author'),
        ),
    ]
