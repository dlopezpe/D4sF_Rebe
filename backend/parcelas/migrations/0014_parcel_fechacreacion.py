# Generated by Django 3.0.7 on 2020-08-10 07:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('parcelas', '0013_auto_20200807_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]