# Generated by Django 3.0.6 on 2020-05-27 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_auto_20200527_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='description',
        ),
    ]