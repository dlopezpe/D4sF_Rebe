from .models import Parcel
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class ParcelSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parcel
        geo_field = "polygon"
        fields = ('id', 'name', 'description')