from django.db import models
from django.utils import timezone
import uuid
from cooperatives.models import Cooperative

from trazas.utils import savelog
from backend.get_username import get_request



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
    sentinel_instance = models.CharField(max_length=255, unique=False, null=False, blank=False, default='96738ec4-8db4-452f-bf50-6ceee33c1c4e')
    cooperative = models.ForeignKey(Cooperative, on_delete=models.DO_NOTHING, related_name='enterprises', null=True, blank=True)
    continent = models.CharField(max_length=50, unique=False, null=True, blank=False)
    is_monitor = models.BooleanField(default=False, null=True, blank=False)
    deleted_at  = models.DateTimeField(auto_now_add=False)
    objects = EnterpriseManager() # The EnterpriseManager.

    def delete(self):
        # we add date stamp but do not delete the record
        self.deleted_at = timezone.now()
        # log purpose
        request = get_request()
        contextLogs = {
            'user_email': request.user,
            'message': 'Empresa eliminada',
            'status': 'success',
            'extra_data': {
                'id': str(self.id),
                'name': self.name,
                'deleted_at': str(self.deleted_at)
            }
        }    
        #savelog(contextLogs,request)
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
        

        contextLogs = {
            'user_email': request.user,
            'message': message,
            'status': 'success',
            'extra_data': {
                'id': str(self.id),
                'name': self.name,
            }
        }
        super(Enterprise, self).save(*args, **kwargs)
        
        if request.method != 'DELETE':
            pass  
            #savelog(contextLogs,request)
        