# Generated by Django 5.2 on 2025-07-23 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0008_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='distance',
            field=models.FloatField(blank=True, default=0.0),
        ),
    ]
