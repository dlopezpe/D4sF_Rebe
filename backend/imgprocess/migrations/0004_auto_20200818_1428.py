# Generated by Django 3.0.7 on 2020-08-18 12:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('imgprocess', '0003_imagenpro_finifin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagenpro',
            old_name='imagen',
            new_name='jsonFile',
        ),
        migrations.AddField(
            model_name='imagenpro',
            name='xlsxFile',
            field=models.CharField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
    ]
