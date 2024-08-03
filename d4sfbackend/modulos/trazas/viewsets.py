from rest_framework import viewsets

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from .models import Trazas
from modulos.user.models import User
from modulos.enterprises.models import Enterprise
from .utils import getRequestIp, getFrontAction
from .serializer import TrazasSerializer
from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class TrazasViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = Trazas.objects.all()
    serializer_class = TrazasSerializer

    def perform_create(self, serializer): 

        ip_user = getRequestIp(self.request)
        id_user = self.request.data.get('id_user')
        status = self.request.data.get('status')
        enterprise_old_status = self.request.data.get('old_status')

        try:
            user_email = User.objects.get(id=id_user).email
        except User.DoesNotExist:
            user_email = 'None'

        enterprise_code = self.request.data.get('enterprise_code')
        
        try:
            enterprise = Enterprise.objects.get(id=enterprise_code)
            enterprise_name = enterprise.name
             #Recibe un False o un True
        except User.DoesNotExist:
            enterprise_name = 'None'

        crud = self.request.data.get('crud')
        action = getFrontAction(self.request.method)
        model_name = enterprise._meta.db_table

        #se muestre el estado de la empresa como activa o inactiva

        enterprise_old_status = 'Activa' if enterprise_old_status == True else 'Inactiva'
        status = 'Activa' if status == '1' else 'Inactiva'

        #Si el estado de la empresa es distinto al que tenía antes, se envía un correo electrónico
        if status != enterprise_old_status:
            context = {
                'action': action,
                'model_name': model_name,
                'crud': crud,
                'enterprise_name': enterprise_name,
                'id_user': id_user,
                'user_email': user_email,
                'enterprise_code': enterprise_code,
                'ip_user': ip_user,
                'enterprise_status': status,
                'fecha_hora': datetime.now(),
                'old_status': enterprise_old_status,
                'new_status': status
            }
            
            #Renderizar plantilla HTML
            ConfigMail()
            html_content = render_to_string('cambio_estado_aviso.html', context)
            subject = 'Notificación de cambio de estado de empresa'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['alvaro.larrea@smartbits.es']
            # cc_list = ['soported4sf@smartbits.es']
            # recipient_list = ['alejandro.jimenez@smartbits.es']

            #Crear y enviar correo electrónico
            email = EmailMultiAlternatives(subject, '', email_from, recipient_list)
            email.attach_alternative(html_content, "text/html")
            email.send()

            serializer.save(ip_user=ip_user, updated_model=model_name, crud='Action: ' + 'UPDATE' + '; ' + crud, id_user=id_user, enterprise_code=enterprise_code, user_email=user_email)
