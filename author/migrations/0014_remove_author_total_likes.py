# Generated by Django 5.0.2 on 2024-04-09 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0013_author_total_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='total_likes',
        ),
    ]
