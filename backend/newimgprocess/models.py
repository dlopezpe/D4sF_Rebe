from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
# Create your models here.
"""
    id -> Id del informe
    name -> Nombre del Informe
    jsonFile -> Fichero de salida Json
    xlsxFile -> Fichero de salida xlsx
    capa = Layer de sentinel seleccionado
    fechaInicio = Fecha de inicio seleccionada
    fechaFin = Fecha de fin seleccionada
    enterprise_id = Id de la empresa relacionada
    esCooperative = Id de la cooperativa relacionada
    user_created = Id del usuario que lo ha creado
    created = fecha de la creacion del informe
"""

class NewImagenPro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=254)
    jsonFile = models.CharField(max_length=254)
    xlsxFile = models.CharField(max_length=254)
    capa = models.CharField(max_length=254)
    fechaInicio = models.CharField(max_length=254)
    fechaFin = models.CharField(max_length=254)
    enterprise_id = models.CharField(max_length=255)
    esCooperative = models.BooleanField(default=False)
    user_created = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now=True)
    id_parcelas = models.CharField(max_length=254, null=True)
    includeClouds = models.BooleanField(default=False)
    esUnificado = models.BooleanField(default=False)
    estado = models.CharField(max_length=1, unique=False, null=True, blank=False)
    error = models.BooleanField(default=False)
    parcelas_fallidas=models.CharField(max_length=254, null=True)