# Generated by Django 3.0.7 on 2020-06-24 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_userprofile_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='usuario',
        ),
    ]