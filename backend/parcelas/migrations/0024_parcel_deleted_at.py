# Generated by Django 3.0.7 on 2023-12-13 08:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('parcelas', '0023_parcel_is_lyc'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='deleted_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]