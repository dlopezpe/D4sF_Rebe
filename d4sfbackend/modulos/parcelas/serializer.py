from .models import Parcel
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.db import models as gis_models

from rest_framework_jwt.settings import api_settings

from django.utils import timezone

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class ParcelSerializer(GeoFeatureModelSerializer):
        requires_context = False
        description = serializers.CharField(required = False, allow_blank=True)
        user_created = serializers.CharField(required = False, allow_blank=True)
        user_updated = serializers.CharField(required = False, allow_blank=True)
        class Meta:
            model = Parcel
            geo_field = "polygon"
            fields = (
                'id', 
                'name', 
                'description', 
                'area', 
                'enterprise', 
                'date_updated', 
                'user_created', 
                'user_updated', 
                'sentinel_instance', 
                'id_importado', 
                'id_productor_importado', 
                'productor_importado',
                'id_variedad_importado', 
                'variedad_importado', 
                'sigpac_importado', 
                'polygon_init', 
                'area_calc', 
                'area_porc', 
                'id_sufijo', 
                'is_LYC'
            )

        def __init__(self, *args, **kwargs):
            # buscar correo Desarrollo parcelas confirmado - Agraz.
            kwargs['partial'] = True
            super(ParcelSerializer, self).__init__(*args, **kwargs)
            self.fields["name"].error_messages["required"] = u"El Nombre es un campo requerido"
            self.fields["name"].error_messages["blank"] = u"El Nombre no puede estar en blanco"

class ParcelSerializerFilter(GeoFeatureModelSerializer):
    class Meta:
            model = Parcel
            geo_field = "polygon"
            fields = ('id', 'name', 'description', 'area', 'enterprise_id', 'sentinel_instance')

class ParcelSerializerArea(GeoFeatureModelSerializer):
    class Meta:
            model = Parcel
            geo_field = "polygon"
            fields = ('id', 'name', 'description', 'area', 'enterprise_id', 'sentinel_instance')
    
    def get_count(self, obj):
        return obj.Parcel.count()

class ParcelSerializerFilterNoSentInstance(GeoFeatureModelSerializer):
    class Meta:
            model = Parcel
            geo_field = "polygon"
            fields = ('id', 'name', 'description', 'area', 'enterprise', 'sentinel_instance')