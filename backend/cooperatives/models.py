from django.db import models
import uuid

from trazas.utils import savelog
from backend.get_username import get_request

# Create your models here.
class Cooperative(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=False, null=False, blank=False)
    direction = models.CharField(max_length=255, unique=False, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=False, null=True, blank=True)
    cif = models.CharField(max_length=20, unique=False, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # log purpose
        request = get_request()
        message = 'Cooperativa creada'

        if request.method == 'PUT': 
            message = 'Cooperativa actualizada'


        contextLogs = {
            'user_email': request.user,
            'message': message,
            'status': 'success',
            'extra_data': {
                'id': str(self.id),
                'name': self.name,
                'direction': self.direction,
                'phone_number': self.phone_number,
                'cif': self.cif,
                'is_active': self.is_active,
            }
        }
        super(Cooperative, self).save(*args, **kwargs)

        if request.method != 'DELETE':
            pass  
            #savelog(contextLogs,request)

    def delete(self, *args, **kwargs):
        # log purpose
        request = get_request()
        contextLogs = {
            'user_email': request.user,
            'message': "Cooperativa Eliminada",
            'status': 'success',
            'extra_data': {
                'id': str(self.id),
                'name': self.name,
                'direction': self.direction,
                'phone_number': self.phone_number,
                'cif': self.cif,
                'is_active': self.is_active,
            }
        } 
        #savelog(contextLogs,request)
        super(Cooperative, self).delete(*args, **kwargs)