# Generated by Django 5.0.2 on 2024-04-02 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookie', '0008_alter_bookieprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookieprofile',
            name='username',
        ),
        migrations.AddField(
            model_name='bookieprofile',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
