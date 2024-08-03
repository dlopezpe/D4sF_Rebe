from .models import NewImagenPro
from rest_framework import serializers

from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class NewImagenProSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=False, allow_blank=True)
    jsonFile = serializers.CharField(required=False, allow_blank=True)
    xlsxFile = serializers.CharField(required=False, allow_blank=True)
    capa = serializers.CharField(required=False, allow_blank=True)
    fechaInicio = serializers.CharField(required=False, allow_blank=True)
    fechaFin = serializers.CharField(required=False, allow_blank=True)
    enterprise_id = serializers.CharField(required=False, allow_blank=True)
    esCooperative = serializers.BooleanField(required=False)
    user_created = serializers.CharField(required=False, allow_blank=True)
    created = serializers.CharField(required=False, allow_blank=True)
    id_parcelas = serializers.ListField(child=serializers.CharField(), required=False, read_only=False)
    includeClouds = serializers.BooleanField(required=False)
    esUnificado = serializers.BooleanField(required=False)
    parcelas_fallidas = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = NewImagenPro
        fields = '__all__'

class NewImagenProModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewImagenPro
        fields = '__all__'