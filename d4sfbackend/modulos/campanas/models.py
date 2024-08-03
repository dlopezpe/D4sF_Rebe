from django.db import models
from modulos.parcelas.models import Parcel


# Create your models here.

class Campanas(models.Model):
    name = models.CharField(max_length=254)
    parcela = models.ForeignKey(Parcel, on_delete=models.DO_NOTHING, related_name='parcelscampana')
    variedad = models.CharField(max_length=254, blank=True, null=True)
    area = models.FloatField(max_length=254, blank=True, null=True)
    superficie = models.FloatField(max_length=254, blank=True, null=True)
    plantas = models.IntegerField(blank=True, null=True)
    plantas_ha = models.FloatField(max_length=254, blank=True, null=True)
    observaciones = models.CharField(max_length=254, blank=True, null=True)
    # deleted = models.BinaryField(default=0)
    anio = models.IntegerField()
    fecha_recogida_estimada = models.DateField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'campanas'

    def __str__(self):
        return self.name


class Siembras(models.Model):
    parcela = models.ForeignKey(Parcel, on_delete=models.DO_NOTHING, related_name='parcelssiembra')
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    anio = models.IntegerField()
    variedad = models.CharField(max_length=254, blank=True, null=True)
    subvariedad = models.CharField(max_length=254, blank=True, null=True)
    tipo_siembra = models.CharField(max_length=254, blank=True, null=True)
    superficie = models.FloatField(max_length=254)
    semillas_ha = models.IntegerField(blank=True, null=True)
    plantas_teoricas_ha = models.IntegerField(blank=True, null=True)
    plantas_reales_ha = models.FloatField(max_length=254)
    vivero = models.CharField(max_length=254)
    tipo_riego = models.CharField(max_length=254)
    # deleted = models.BinaryField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.parcela


class Producciones(models.Model):
    parcela = models.ForeignKey(Parcel, on_delete=models.DO_NOTHING, related_name='parcelsproduccion')
    campana = models.CharField(max_length=254)
    anio = models.IntegerField()
    fecha_registro = models.DateField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    plantas = models.IntegerField(blank=True, null=True)
    produccion = models.FloatField(max_length=254)
    tipo_ud = models.CharField(max_length=254, blank=True, null=True)
    kg_planta = models.FloatField(max_length=254)
    kg_ha = models.FloatField(max_length=254)
    aforo = models.FloatField(max_length=254)
    aforo_plantas = models.FloatField(max_length=254)
    desviacion = models.FloatField(max_length=254)
    desviacion_planta = models.FloatField(max_length=254)
    desviacion_ha = models.FloatField(max_length=254)
    variedad = models.CharField(max_length=254, blank=True, null=True)
    subvariedad = models.CharField(max_length=254, blank=True, null=True)
    # deleted = models.BinaryField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.campana
