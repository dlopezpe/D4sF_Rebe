from .models import Campanas, Siembras, Producciones
from rest_framework import serializers


class CampanasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campanas
        fields = '__all__'


class SiembrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Siembras
        fields = '__all__'


class ProduccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producciones
        fields = '__all__'
