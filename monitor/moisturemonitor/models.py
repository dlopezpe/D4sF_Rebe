from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

# Create your models here.
class MoistureMonitor(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

    parcel = models.IntegerField(null=True, blank=True)
    name = models.CharField(null=True, max_length=255, blank=True)

    # Naranja
    pix_naranja_total = models.FloatField(null=True, blank=True)
    pix_naranja_porcent = models.FloatField(null=True, blank=True)
    pix_naranja_area_porcent = models.FloatField(null=True, blank=True)

    # Amarillo
    pix_amarillo_total = models.FloatField(null=True, blank=True)
    pix_amarillo_porcent = models.FloatField(null=True, blank=True)
    pix_amarillo_area_porcent = models.FloatField(null=True, blank=True)

    # Verde
    pix_verde_total = models.FloatField(null=True, blank=True)
    pix_verde_porcent = models.FloatField(null=True, blank=True)
    pix_verde_area_porcent = models.FloatField(null=True, blank=True)

    # Azul Claro
    pix_azul_claro_total = models.FloatField(null=True, blank=True)
    pix_azul_claro_porcent = models.FloatField(null=True, blank=True)
    pix_azul_claro_area_porcent = models.FloatField(null=True, blank=True)

    # Azul medio
    pix_azul_medio_total = models.FloatField(null=True, blank=True)
    pix_azul_medio_porcent = models.FloatField(null=True, blank=True)
    pix_azul_medio_area_porcent = models.FloatField(null=True, blank=True)

    # Azul oscuro
    pix_azul_oscuro_total = models.FloatField(null=True, blank=True)
    pix_azul_oscuro_porcent = models.FloatField(null=True, blank=True)
    pix_azul_oscuro_area_porcent = models.FloatField(null=True, blank=True)

    
    #NUBES

    nubes_porcent = models.FloatField(null=True, blank=True)

    image = models.CharField(null=True, max_length=255, blank=True)
    nubesImage = models.CharField(null=True, max_length=255, blank=True)
    trueColorImage = models.CharField(null=True, max_length=255, blank=True)
    date =  models.DateTimeField(null=True, blank=True)

    modified = models.DateTimeField(auto_now=True)