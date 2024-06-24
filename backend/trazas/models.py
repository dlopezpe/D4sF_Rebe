from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Log(models.Model):
    user_email = models.TextField(blank=False,null=False)
    app_name = models.TextField(default='Parcelas',null=True)
    path = models.TextField(default='',null=True)
    method = models.TextField(default='',null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    message = models.TextField(null=False)
    status = models.CharField(max_length=30,blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    extra_data = JSONField(blank=True, null=True)

    class Meta:
        ordering = ["create_at"]
        verbose_name_plural = "logs"

class Trazas(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.TextField(max_length=255, blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    updated_model = models.TextField(max_length=255, blank=True, null=True)
    crud = models.TextField(max_length=1000,blank=True, null=True)
    ip_user = models.GenericIPAddressField(protocol='both', blank=True, null=True)
    enterprise_code = models.TextField(max_length=255, blank=True, null=True)
    user_email = models.EmailField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'trazas'