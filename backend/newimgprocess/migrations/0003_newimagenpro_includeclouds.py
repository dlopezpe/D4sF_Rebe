# Generated by Django 3.0.7 on 2021-06-09 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newimgprocess', '0002_newimagenpro_id_parcelas'),
    ]

    operations = [
        migrations.AddField(
            model_name='newimagenpro',
            name='includeClouds',
            field=models.BooleanField(default=False),
        ),
    ]
