# Generated by Django 5.0.2 on 2024-04-04 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_reviewandrating_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewandrating',
            name='type',
            field=models.CharField(choices=[('positive', 'Positive'), ('negative', 'Negative'), ('neutral', 'Neutral')], default='Neutral', max_length=10),
        ),
    ]
