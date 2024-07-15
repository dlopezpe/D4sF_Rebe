# Generated by Django 3.0.6 on 2020-05-29 08:37

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.polygon
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcelas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parcel',
            name='point',
        ),
        migrations.AddField(
            model_name='parcel',
            name='polygon',
            field=django.contrib.gis.db.models.fields.PolygonField(default=django.contrib.gis.geos.polygon.Polygon(((0, 0), (0, 10), (10, 10), (0, 10), (0, 0)), ((4, 4), (4, 6), (6, 6), (6, 4), (4, 4))), srid=4326),
        ),
    ]