# Generated by Django 3.0.7 on 2020-09-07 15:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('imgprocess', '0008_imagenpro_polygon'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagenpro',
            name='enterprise_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]