# Generated by Django 3.0.7 on 2020-06-24 11:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_userprofile_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='enterprise_id',
            field=models.UUIDField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
