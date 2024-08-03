import uuid

from django.db import models
from django.utils import timezone

from backend.get_username import get_request
from modulos.cooperatives.models import Cooperative
from utils.Utils import save_log


class EnterpriseManager(models.Manager):
    def get_queryset(self):
        # we override the enterprise query filtered by deleted_at equal to None
        return super().get_queryset().filter(deleted_at=None)


class Enterprise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=False, null=False, blank=False)
    direction = models.CharField(max_length=255, unique=False, null=False, blank=False)
    phone_number = models.CharField(max_length=20, unique=False, null=False, blank=False)
    cif = models.CharField(max_length=20, unique=False, null=False, blank=False)
    hectares_available = models.CharField(max_length=254, unique=False, null=True, blank=False)
    type_metric = models.CharField(max_length=50, unique=False, null=True, blank=False)
    is_active = models.BooleanField(default=True)
    sentinel_instance = models.CharField(max_length=255, unique=False, null=False, blank=False,
                                         default='96738ec4-8db4-452f-bf50-6ceee33c1c4e')
    cooperative = models.ForeignKey(Cooperative, on_delete=models.DO_NOTHING, related_name='enterprises', null=True,
                                    blank=True)
    continent = models.CharField(max_length=50, unique=False, null=True, blank=False)
    is_monitor = models.BooleanField(default=False, null=True, blank=False)
    deleted_at = models.DateTimeField(auto_now_add=False)
    objects = EnterpriseManager()  # The EnterpriseManager.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'enterprises'

    def __str__(self):
        return self.name

    def delete(self, **kwargs):
        # we add date stamp but do not delete the record
        self.deleted_at = timezone.now()
        request = get_request()

        # log purpuse
        extra_data = {
            'id': str(self.id),
            'name': self.name,
            'deleted_at': str(self.deleted_at)
        }

        save_log('Empresa eliminada', request, extra_data)

        self.save()

    def save(self, *args, **kwargs):
        # log purpose
        """
        El frontend realiza 2 peticiones al crear una empresa get/put
        el log registrara dos registros al crear una empresa 
        """
        request = get_request()
        message = 'Empresa creada'

        if request.method == 'PUT':
            message = 'Empresa actualizada'

        if self.deleted_at is not None:
            message = 'Empresa actualizada (Eliminada)'

        # log purpuse
        extra_data = {
                'id': str(self.id),
                'name': self.name,
            }

        save_log(message, request, extra_data)
        super(Enterprise, self).save(*args, **kwargs)

        if request.method != 'DELETE':
            pass
