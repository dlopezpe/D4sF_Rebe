# Generated by Django 3.0.7 on 2020-08-11 14:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('imgprocess', '0002_imagenpro_fechas'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagenpro',
            name='finifin',
            field=models.CharField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
    ]
