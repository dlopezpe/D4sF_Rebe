from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class ImagenPro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parcela = models.CharField(max_length=254)
    urlSentinel = models.CharField(max_length=254)
    imagen = models.CharField(max_length=254)
    xlsxFile = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now=True)
    fechas = models.CharField(max_length=254)
    finifin = models.CharField(max_length=254)
    tipo = models.IntegerField(blank=True, null=True)
    capa = models.CharField(max_length=254)
    fechaElegida = models.CharField(max_length=254)
    checkDellOtros = models.BooleanField(default=False)
    alias = models.CharField(max_length=254)
    id_parcelas = models.CharField(max_length=254, null=True)
    polygon = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=8,
        ),
        size=8,
    )
    enterprise_id = models.CharField(max_length=255)
    esCooperative = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'imgprocess'

    def __str__(self):
        return self.id
