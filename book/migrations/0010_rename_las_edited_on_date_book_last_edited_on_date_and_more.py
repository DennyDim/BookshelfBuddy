# Generated by Django 5.0.2 on 2024-04-07 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_book_added_on_date_book_las_edited_on_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='las_edited_on_date',
            new_name='last_edited_on_date',
        ),
        migrations.DeleteModel(
            name='BookRequestFromUserModel',
        ),
    ]
