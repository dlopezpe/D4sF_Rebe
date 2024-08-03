import uuid

from django.db import models

from backend.get_username import get_request
from utils.Utils import save_log


# Create your models here.
class Cooperative(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=False, null=False, blank=False)
    direction = models.CharField(max_length=255, unique=False, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=False, null=True, blank=True)
    cif = models.CharField(max_length=20, unique=False, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'cooperatives'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # log purpose
        request = get_request()
        message = 'Cooperativa creada'

        if request.method == 'PUT':
            message = 'Cooperativa actualizada'

        # log purpuse
        extra_data = {
            'id': str(self.id),
            'name': self.name,
            'direction': self.direction,
            'phone_number': self.phone_number,
            'cif': self.cif,
            'is_active': self.is_active,
        }

        save_log(message, request, extra_data)
        super(Cooperative, self).save(*args, **kwargs)

        if request.method != 'DELETE':
            pass

    def delete(self, *args, **kwargs):
        # log purpose
        request = get_request()
        extra_data = {
                'id': str(self.id),
                'name': self.name,
                'direction': self.direction,
                'phone_number': self.phone_number,
                'cif': self.cif,
                'is_active': self.is_active,
            }

        save_log("Cooperativa Eliminada", request, extra_data)
        super(Cooperative, self).delete(*args, **kwargs)
