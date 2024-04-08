# Generated by Django 5.0.2 on 2024-04-07 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookie', '0009_remove_bookieprofile_username_bookieprofile_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookieprofile',
            name='date_joined',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bookie',
            name='email',
            field=models.EmailField(max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='bookieprofile',
            name='bio',
            field=models.TextField(blank=True, help_text='Share something about yourself.', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='bookieprofile',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]