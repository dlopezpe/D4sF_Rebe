from rest_framework import serializers
from ndvimonitor.models import NdviMonitor

class NdviMonitorModelserializer(serializers.ModelSerializer):
    class Meta:
        model = NdviMonitor
        fields = (
            'id',
            'parcel',
            'name',

            # AZULES
            'pix_azul_total',
            'pix_azul_total_porcent',

            'pix_azul_altos_total',
            'pix_azul_altos_porcent',
            'pix_azul_altos_area_porcent',

            'pix_azul_medios_total',
            'pix_azul_medios_porcent',
            'pix_azul_medios_area_porcent',

            'pix_azul_bajos_total',
            'pix_azul_bajos_porcent',
            'pix_azul_bajos_area_porcent',

            #AMARILLOS

            'pix_amarillo_total',
            'pix_amarillo_total_porcent',

            'pix_amarillo_altos_total',
            'pix_amarillo_altos_porcent',
            'pix_amarillo_altos_area_porcent',

            'pix_amarillo_medios_total',
            'pix_amarillo_medios_porcent',
            'pix_amarillo_medios_area_porcent',

            'pix_amarillo_bajos_total',
            'pix_amarillo_bajos_porcent',
            'pix_amarillo_bajos_area_porcent',

            #ROJOS

            'pix_rojo_total',
            'pix_rojo_total_porcent',

            'pix_rojo_altos_total',
            'pix_rojo_altos_porcent',
            'pix_rojo_altos_area_porcent',

            'pix_rojo_medios_total',
            'pix_rojo_medios_porcent',
            'pix_rojo_medios_area_porcent',

            'pix_rojo_bajos_total',
            'pix_rojo_bajos_porcent',
            'pix_rojo_bajos_area_porcent',

            #VERDES

            'pix_verde_total',
            'pix_verde_total_porcent',

            'pix_verde_altos_total',
            'pix_verde_altos_porcent',
            'pix_verde_altos_area_porcent',

            'pix_verde_medios_total',
            'pix_verde_medios_porcent',
            'pix_verde_medios_area_porcent',

            #NUBES

            'nubes_porcent',

            'image',
            'nubesImage',
            'trueColorImage',
            'date'
        )

class NdviMonitorSerializer(serializers.Serializer):

    parcel = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)

    # AZULES
    pix_azul_total = serializers.FloatField(required=False)
    pix_azul_total_porcent = serializers.FloatField(required=False)

    pix_azul_altos_total= serializers.FloatField(required=False)
    pix_azul_altos_porcent = serializers.FloatField(required=False)
    pix_azul_altos_area_porcent = serializers.FloatField(required=False)

    pix_azul_medios_total= serializers.FloatField(required=False)
    pix_azul_medios_porcent = serializers.FloatField(required=False)
    pix_azul_medios_area_porcent = serializers.FloatField(required=False)

    pix_azul_bajos_total= serializers.FloatField(required=False)
    pix_azul_bajos_porcent = serializers.FloatField(required=False)
    pix_azul_bajos_area_porcent = serializers.FloatField(required=False)

    #AMARILLOS

    pix_amarillo_total = serializers.FloatField(required=False)
    pix_amarillo_total_porcent = serializers.FloatField(required=False)

    pix_amarillo_altos_total= serializers.FloatField(required=False)
    pix_amarillo_altos_porcent = serializers.FloatField(required=False)
    pix_amarillo_altos_area_porcent = serializers.FloatField(required=False)

    pix_amarillo_medios_total= serializers.FloatField(required=False)
    pix_amarillo_medios_porcent = serializers.FloatField(required=False)
    pix_amarillo_medios_area_porcent = serializers.FloatField(required=False)

    pix_amarillo_bajos_total= serializers.FloatField(required=False)
    pix_amarillo_bajos_porcent = serializers.FloatField(required=False)
    pix_amarillo_bajos_area_porcent = serializers.FloatField(required=False)

    #ROJOS

    pix_rojo_total = serializers.FloatField(required=False)
    pix_rojo_total_porcent = serializers.FloatField(required=False)

    pix_rojo_altos_total= serializers.FloatField(required=False)
    pix_rojo_altos_porcent = serializers.FloatField(required=False)
    pix_rojo_altos_area_porcent = serializers.FloatField(required=False)

    pix_rojo_medios_total= serializers.FloatField(required=False)
    pix_rojo_medios_porcent = serializers.FloatField(required=False)
    pix_rojo_medios_area_porcent = serializers.FloatField(required=False)

    pix_rojo_bajos_total= serializers.FloatField(required=False)
    pix_rojo_bajos_porcent = serializers.FloatField(required=False)
    pix_rojo_bajos_area_porcent = serializers.FloatField(required=False)

    #VERDES

    pix_verde_total = serializers.FloatField(required=False)
    pix_verde_total_porcent = serializers.FloatField(required=False)

    pix_verde_altos_total= serializers.FloatField(required=False)
    pix_verde_altos_porcent = serializers.FloatField(required=False)
    pix_verde_altos_area_porcent = serializers.FloatField(required=False)

    pix_verde_medios_total= serializers.FloatField(required=False)
    pix_verde_medios_porcent = serializers.FloatField(required=False)
    pix_verde_medios_area_porcent = serializers.FloatField(required=False)

    #NUBES

    nubes_porcent = serializers.FloatField(required=False)

    image = serializers.CharField(required=False)
    nubesImage = serializers.CharField(required=False)
    trueColorImage = serializers.CharField(required=False)
    date =  serializers.DateTimeField(required=False)


    def validate(self, data):
        return data

    def create(self, data):
        document = NdviMonitor.objects.create(**data)
        return document