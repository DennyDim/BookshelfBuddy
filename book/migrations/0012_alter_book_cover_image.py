# Generated by Django 5.0.2 on 2024-04-01 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_alter_book_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(default='no_cover.jpg', upload_to='cover_images'),
        ),
    ]
