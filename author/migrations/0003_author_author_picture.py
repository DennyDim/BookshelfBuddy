# Generated by Django 5.0.2 on 2024-03-23 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0002_alter_author_year_born'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='author_picture',
            field=models.ImageField(default='images/no_profile_pic.jpg', upload_to='images/'),
        ),
    ]
