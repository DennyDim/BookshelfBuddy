# Generated by Django 5.0.2 on 2024-03-23 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_alter_book_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.URLField(blank=True, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPa8pabMznsqT-GWDJccgg3uLBcnSwOpIXrA&usqp=CAU'),
        ),
    ]