# Generated by Django 4.0.4 on 2022-04-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moisturemonitor', '0002_moisturemonitor_trueColorImage'),
    ]

    operations = [
        migrations.AddField(
            model_name='moisturemonitor',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
