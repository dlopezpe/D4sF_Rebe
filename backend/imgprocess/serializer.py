from .models import ImagenPro
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.db import models as gis_models

from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class ImagenProSerializer(serializers.ModelSerializer):
    urlSentinel = serializers.ListField(child=serializers.CharField(), required = False)
    fechas = serializers.ListField(child=serializers.CharField(), required = False)
    id_parcelas = serializers.ListField(child=serializers.CharField(), required = False)
    imagen = serializers.CharField(required = False, allow_blank=True)
    finifin = serializers.CharField(required = False, allow_blank=True)
    xlsxFile = serializers.CharField(required = False, allow_blank=True)
    fechaElegida = serializers.CharField(required = False, allow_blank=True)
    alias = serializers.CharField(required = False, allow_blank=True)
    parcela = serializers.CharField(required = False, allow_blank=True)
    capa = serializers.CharField(required = False, allow_blank=True)
    enterprise_id = serializers.CharField(required = False, allow_blank=True)
    
    tipo = serializers.IntegerField(required = False)
    polygon = serializers.ListField(child=serializers.ListField(), required = False)
    checkDellOtros = serializers.BooleanField(required=False)
    esCooperative = serializers.BooleanField(required=False)
    class Meta:
        model = ImagenPro
        fields = '__all__'