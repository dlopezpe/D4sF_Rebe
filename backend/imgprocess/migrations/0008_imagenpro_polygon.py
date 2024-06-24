# Generated by Django 3.0.7 on 2020-08-21 08:20

import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('imgprocess', '0007_auto_20200820_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagenpro',
            name='polygon',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=8), default='{}', size=8),
            preserve_default=False,
        ),
    ]
