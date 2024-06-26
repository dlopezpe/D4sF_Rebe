# Generated by Django 3.0.7 on 2020-07-20 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enterprises', '0005_remove_enterprise_hectares_used'),
        ('parcelas', '0009_auto_20200720_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parcel',
            name='enterprise_id',
        ),
        migrations.AddField(
            model_name='parcel',
            name='enterprise',
            field=models.ForeignKey(default='e20af9fa-892c-4099-9a5f-002e759d2948', on_delete=django.db.models.deletion.CASCADE, related_name='parcels', to='enterprises.Enterprise'),
            preserve_default=False,
        ),
    ]
