# Generated by Django 3.0.7 on 2020-07-17 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcelas', '0004_parcel_enterprise_id'),
        ('enterprises', '0003_enterprise_sentinel_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprise',
            name='hectares_used',
            field=models.ManyToManyField(to='parcelas.Parcel'),
        ),
    ]
