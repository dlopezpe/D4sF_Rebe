# Generated by Django 3.0.7 on 2020-07-17 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcelas', '0005_auto_20200717_1247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parcel',
            old_name='enterprise_id',
            new_name='enterprise',
        ),
    ]
