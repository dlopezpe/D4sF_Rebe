# Generated by Django 3.0.7 on 2020-09-24 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgprocess', '0009_imagenpro_enterprise_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagenpro',
            name='capa',
            field=models.CharField(default='NDVI', max_length=254),
            preserve_default=False,
        ),
    ]
