# Generated by Django 5.0.2 on 2024-04-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_alter_book_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(blank=True, default='static/images/no_cover.jpg', null=True, upload_to='book/cover_images'),
        ),
    ]
