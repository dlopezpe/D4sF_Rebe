import uuid
from django.db import models
from user.models import User

from trazas.utils import savelog
from backend.get_username import get_request

class UserProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
    enterprise_id = models.UUIDField(max_length=10, unique=False, null=False, blank=False, default=uuid.uuid4)
    cooperative_user = models.BooleanField(default=False)
    
    class Meta:
        '''
        to set table name in database
        '''
        db_table = "profile"

    def save(self, *args, **kwargs):
        # log purpose
        request = get_request()
        message = 'Usuario creado'

        if request.method == 'PUT': 
            message = 'Usuario actualizado'


        contextLogs = {
            'user_email': request.user,
            'message': message,
            'status': 'success',
            'extra_data': {
                'id': str(self.id),
                'user': str(self.user.id),
                'first_name': self.first_name,
                'last_name': self.last_name,
                'phone_number': self.phone_number,
                'enterprise_id': str(self.enterprise_id),
                'cooperative_user': self.cooperative_user,
            }
        }
        super(UserProfile, self).save(*args, **kwargs)

        if request.method != 'DELETE': 
            pass 
            #savelog(contextLogs,request)

    def delete(self, *args, **kwargs):
        # log purpose
        request = get_request()
        contextLogs = {
            'user_email': request.user,
            'message': "Usuario Eliminado",
            'status': 'success',
            'extra_data': {
                'id': str(self.id),
                'user': str(self.user.id),
                'first_name': self.first_name,
                'last_name': self.last_name,
                'phone_number': self.phone_number,
                'enterprise_id': str(self.enterprise_id),
                'cooperative_user': self.cooperative_user,
            }
        } 
        #savelog(contextLogs,request)
        super(UserProfile, self).delete(*args, **kwargs)