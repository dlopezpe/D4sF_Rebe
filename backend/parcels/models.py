from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Polygon


# Create your models here.

class Parcel(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    # point = gis_models.PolygonField(default=Point(0, 0), blank=True)