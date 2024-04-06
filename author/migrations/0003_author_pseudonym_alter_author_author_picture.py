# Generated by Django 5.0.2 on 2024-04-05 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0002_author_author_picture_author_authors_bio_author_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='pseudonym',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='author_picture',
            field=models.ImageField(default='images/no_profile_pic.jpg', upload_to='authors_pictures'),
        ),
    ]
