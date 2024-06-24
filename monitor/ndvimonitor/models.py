from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

# Create your models here.
class NdviMonitor(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

    parcel = models.IntegerField(null=True, blank=True)
    name = models.CharField(null=True, max_length=255, blank=True)

    # AZULES
    pix_azul_total = models.FloatField(null=True, blank=True)
    pix_azul_total_porcent = models.FloatField(null=True, blank=True)

    pix_azul_altos_total= models.FloatField(null=True, blank=True)
    pix_azul_altos_porcent = models.FloatField(null=True, blank=True)
    pix_azul_altos_area_porcent = models.FloatField(null=True, blank=True)

    pix_azul_medios_total= models.FloatField(null=True, blank=True)
    pix_azul_medios_porcent = models.FloatField(null=True, blank=True)
    pix_azul_medios_area_porcent = models.FloatField(null=True, blank=True)

    pix_azul_bajos_total= models.FloatField(null=True, blank=True)
    pix_azul_bajos_porcent = models.FloatField(null=True, blank=True)
    pix_azul_bajos_area_porcent = models.FloatField(null=True, blank=True)

    #AMARILLOS

    pix_amarillo_total = models.FloatField(null=True, blank=True)
    pix_amarillo_total_porcent = models.FloatField(null=True, blank=True)

    pix_amarillo_altos_total= models.FloatField(null=True, blank=True)
    pix_amarillo_altos_porcent = models.FloatField(null=True, blank=True)
    pix_amarillo_altos_area_porcent = models.FloatField(null=True, blank=True)

    pix_amarillo_medios_total= models.FloatField(null=True, blank=True)
    pix_amarillo_medios_porcent = models.FloatField(null=True, blank=True)
    pix_amarillo_medios_area_porcent = models.FloatField(null=True, blank=True)

    pix_amarillo_bajos_total= models.FloatField(null=True, blank=True)
    pix_amarillo_bajos_porcent = models.FloatField(null=True, blank=True)
    pix_amarillo_bajos_area_porcent = models.FloatField(null=True, blank=True)

    #ROJOS

    pix_rojo_total = models.FloatField(null=True, blank=True)
    pix_rojo_total_porcent = models.FloatField(null=True, blank=True)

    pix_rojo_altos_total= models.FloatField(null=True, blank=True)
    pix_rojo_altos_porcent = models.FloatField(null=True, blank=True)
    pix_rojo_altos_area_porcent = models.FloatField(null=True, blank=True)

    pix_rojo_medios_total= models.FloatField(null=True, blank=True)
    pix_rojo_medios_porcent = models.FloatField(null=True, blank=True)
    pix_rojo_medios_area_porcent = models.FloatField(null=True, blank=True)

    pix_rojo_bajos_total= models.FloatField(null=True, blank=True)
    pix_rojo_bajos_porcent = models.FloatField(null=True, blank=True)
    pix_rojo_bajos_area_porcent = models.FloatField(null=True, blank=True)

    #VERDES

    pix_verde_total = models.FloatField(null=True, blank=True)
    pix_verde_total_porcent = models.FloatField(null=True, blank=True)

    pix_verde_altos_total= models.FloatField(null=True, blank=True)
    pix_verde_altos_porcent = models.FloatField(null=True, blank=True)
    pix_verde_altos_area_porcent = models.FloatField(null=True, blank=True)

    pix_verde_medios_total= models.FloatField(null=True, blank=True)
    pix_verde_medios_porcent = models.FloatField(null=True, blank=True)
    pix_verde_medios_area_porcent = models.FloatField(null=True, blank=True)

    #NUBES

    nubes_porcent = models.FloatField(null=True, blank=True)

    image = models.CharField(null=True, max_length=255, blank=True)
    nubesImage = models.CharField(null=True, max_length=255, blank=True)
    trueColorImage = models.CharField(null=True, max_length=255, blank=True)
    date =  models.DateTimeField(null=True, blank=True)

    modified = models.DateTimeField(auto_now=True)

