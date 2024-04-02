# Generated by Django 5.0.2 on 2024-04-02 11:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='author_picture',
            field=models.ImageField(default='images/no_profile_pic.jpg', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='author',
            name='authors_bio',
            field=models.TextField(default='Born in', help_text='A brief description of the author. Use at least 40 characters.', max_length=1000, validators=[django.core.validators.MinLengthValidator(40)]),
        ),
        migrations.AddField(
            model_name='author',
            name='name',
            field=models.CharField(error_messages={'unique': 'Author with this name already exists.'}, max_length=100, null=True, unique=True, verbose_name='Author name'),
        ),
        migrations.AddField(
            model_name='author',
            name='year_born',
            field=models.PositiveIntegerField(default=1000, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(2024)], verbose_name='Author`s birth year'),
        ),
    ]
