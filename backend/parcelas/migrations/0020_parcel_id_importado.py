# Generated by Django 3.0.7 on 2022-03-30 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcelas', '0019_parcel_sentinel_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='id_importado',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
