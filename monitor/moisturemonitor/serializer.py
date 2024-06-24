from rest_framework import serializers
from moisturemonitor.models import MoistureMonitor

class MoistureMonitorModelserializer(serializers.ModelSerializer):
    class Meta:
        model = MoistureMonitor
        fields = (
            'id',
            'parcel',
            'name',

            # Naranja
            'pix_naranja_total',
            'pix_naranja_porcent',
            'pix_naranja_area_porcent',

            # Amarillo
            'pix_amarillo_total',
            'pix_amarillo_porcent',
            'pix_amarillo_area_porcent',

            # Verde
            'pix_verde_total',
            'pix_verde_porcent',
            'pix_verde_area_porcent',

            # Azul Claro
            'pix_azul_claro_total',
            'pix_azul_claro_porcent',
            'pix_azul_claro_area_porcent',

            # Azul medio
            'pix_azul_medio_total',
            'pix_azul_medio_porcent',
            'pix_azul_medio_area_porcent',

            # Azul oscuro
            'pix_azul_oscuro_total',
            'pix_azul_oscuro_porcent',
            'pix_azul_oscuro_area_porcent',

            #NUBES

            'nubes_porcent',

            'image',
            'nubesImage',
            'trueColorImage',
            'date'
        )

class MoistureMonitorSerializer(serializers.Serializer):

    parcel = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)

    # Naranja
    pix_naranja_total = serializers.FloatField(required=False)
    pix_naranja_porcent = serializers.FloatField(required=False)
    pix_naranja_area_porcent = serializers.FloatField(required=False)

    # Amarillo
    pix_amarillo_total = serializers.FloatField(required=False)
    pix_amarillo_porcent = serializers.FloatField(required=False)
    pix_amarillo_area_porcent = serializers.FloatField(required=False)

    # Verde
    pix_verde_total = serializers.FloatField(required=False)
    pix_verde_porcent = serializers.FloatField(required=False)
    pix_verde_area_porcent = serializers.FloatField(required=False)

    # Azul Claro
    pix_azul_claro_total = serializers.FloatField(required=False)
    pix_azul_claro_porcent = serializers.FloatField(required=False)
    pix_azul_claro_area_porcent = serializers.FloatField(required=False)

    # Azul medio
    pix_azul_medio_total = serializers.FloatField(required=False)
    pix_azul_medio_porcent = serializers.FloatField(required=False)
    pix_azul_medio_area_porcent = serializers.FloatField(required=False)

    # Azul oscuro
    pix_azul_oscuro_total = serializers.FloatField(required=False)
    pix_azul_oscuro_porcent = serializers.FloatField(required=False)
    pix_azul_oscuro_area_porcent = serializers.FloatField(required=False)

    #NUBES

    nubes_porcent = serializers.FloatField(required=False)

    image = serializers.CharField(required=False)
    nubesImage = serializers.CharField(required=False)
    trueColorImage = serializers.CharField(required=False)
    date =  serializers.DateTimeField(required=False)


    def validate(self, data):
        return data

    def create(self, data):
        document = MoistureMonitor.objects.create(**data)
        return document