# Generated by Django 5.0.2 on 2024-04-09 23:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0014_remove_author_total_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='people_who_like_this_author',
            field=models.ManyToManyField(blank=True, related_name='likes_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
