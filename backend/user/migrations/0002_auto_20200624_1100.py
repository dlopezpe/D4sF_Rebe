# Generated by Django 3.0.7 on 2020-06-24 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_enterpriseadmin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_systemadmin',
            field=models.BooleanField(default=False),
        ),
    ]