from django.db import models
from django.db.models import Sum
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import uuid
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Polygon, GEOSGeometry
from enterprises.models import Enterprise
from profiles.models import UserProfile

from django.utils import timezone

from trazas.utils import savelog
from backend.get_username import get_request

class ParcelManager(models.Manager):
    def get_queryset(self):
        # we override the parcel query filtered by deleted_at equal to None
        #return super().get_queryset().filter(deleted_at=None)
        return super().get_queryset().exclude(deleted_at__isnull=False)

# Create your models here.

class Parcel(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    area = models.FloatField(max_length=254)
    polygon = gis_models.PolygonField(default=Polygon(((0, 0), (0, 10), (10, 10), (0, 10), (0, 0)), ((4, 4), (4, 6), (6, 6), (6, 4), (4, 4))))
    #enterprise_id = models.UUIDField(max_length=10, unique=False, null=False, blank=False, default='e20af9fa-892c-4099-9a5f-002e759d2948')
    enterprise = models.ForeignKey(Enterprise, on_delete=models.DO_NOTHING, related_name='parcels')
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now_add=True, blank=True)
    user_created = models.CharField(max_length=254)
    user_updated = models.CharField(max_length=254)
    sentinel_instance = models.CharField(max_length=255, unique=False, null=True, blank=False)
    id_importado = models.CharField(max_length=255, unique=False, null=True, blank=False)
    id_sufijo = models.CharField(max_length=255, unique=False, null=True, blank=False)
    id_productor_importado = models.CharField(max_length=255, unique=False, null=True, blank=False)
    productor_importado = models.CharField(max_length=255, unique=False, null=True, blank=False)
    id_variedad_importado = models.CharField(max_length=255, unique=False, null=True, blank=False)
    variedad_importado = models.CharField(max_length=255, unique=False, null=True, blank=False)
    is_LYC=models.BooleanField(default=False)
    sigpac_importado = models.CharField(max_length=255, unique=False, null=True, blank=False)
    polygon_init = gis_models.PolygonField(default=Polygon(((0, 0), (0, 10), (10, 10), (0, 10), (0, 0)), ((4, 4), (4, 6), (6, 6), (6, 4), (4, 4))))
    area_calc = models.FloatField(max_length=254, null=True, blank=False)
    area_porc = models.FloatField(max_length=254, null=True, blank=False)
    deleted_at  = models.DateTimeField(auto_now_add=False)
    objects = ParcelManager() # The EnterpriseManager.

    def delete(self):
        # we add date stamp but do not delete the record
        self.deleted_at = timezone.now()
        request = get_request()
        contextLogs = {
            'user_email': request.user,
            'message': 'Parcela eliminada',
            'status': 'success',
            'extra_data': {
                'id': self.id,
                'name': self.name,
            }
        }    
        #savelog(contextLogs,request)

        self.save()

    def save(self, *args, **kwargs): 
        self.date_updated = timezone.now()
        object_id = 0
        if self.id:
            object_id = self.id
        hectares_poligon = self.area
        # Datos de la empresa
        hectares_avariable = getattr(self.enterprise, 'hectares_available')
        enterprise_name = getattr(self.enterprise, 'name')
        cif = getattr(self.enterprise, 'cif')
        phone_number = getattr(self.enterprise, 'phone_number')
        direction = getattr(self.enterprise, 'direction')
        # Datos de los perfiles de usuarios
        usersPer = UserProfile.objects.select_related('user').filter(enterprise_id=getattr(self.enterprise, 'id'))
        arrEnterAdmins = []
        for profiles in usersPer:
            if(profiles.user.__dict__['is_enterpriseadmin']):
                arrEnterAdmins.append({'email': profiles.user.__dict__['email'], 'lang': profiles.user.__dict__['language']})
        if object_id == 0:
            areaOcuQry = Parcel.objects.filter(enterprise_id=getattr(self.enterprise, 'id')).aggregate(Sum('area'))
        else:
            areaOcuQry = Parcel.objects.filter(enterprise_id=getattr(self.enterprise, 'id')).exclude(id=object_id).aggregate(Sum('area'))
        area_ocu = areaOcuQry['area__sum'] or 0
        porcentaje = '{0:.2f}'.format(((float(area_ocu)+float(hectares_poligon)) / float(hectares_avariable) * 100))
        if float(porcentaje) >= 90.00:
            site_shortcut_name = 'Data4SmartFarming'
            context = {
                'site_name': site_shortcut_name,
                'hectares_avariable': hectares_avariable,
                'enterprise_name': enterprise_name,
                'cif': cif,
                'phone_number': phone_number,
                'direction': direction,
                'porcentaje': porcentaje,
                'area_ocu': str(round(float(area_ocu), 2))
            }
            for user in arrEnterAdmins:
                if user['lang'] == 'es':
                    email_html_message_enterprise = render_to_string('pasado_limite_empresa.html', context)
                    title = "=?utf-8?Q?=F0=9F=9A=A7_Aviso_de_l=C3=ADmite_de_hect=C3=A1reas?="
                    email_html_message_enterprise = render_to_string('pasado_limite_empresa.html', context)
                    if float(porcentaje) >= 100.00:
                        title = "=?utf-8?Q?=F0=9F=8F=81_L=C3=ADmite_de_hect=C3=A1reas_excedido?="
                        email_html_message_enterprise = render_to_string('excedido_limite_empresa.html', context)
                else:
                    title = "=?utf-8?Q?=F0=9F=9A=A7_Hectare_limit_notice?="
                    email_html_message_enterprise = render_to_string('pasado_limite_empresa_en.html', context)
                    if float(porcentaje) >= 100.00:
                        title = "=?utf-8?Q?=F0=9F=8F=81_Limit_of_hectares_exceeded?="
                        email_html_message_enterprise = render_to_string('excedido_limite_empresa_en.html', context)
                # Mail para los admin de la empresa
                msg = EmailMultiAlternatives(
                    # title:
                    title,
                    # message:
                    email_html_message_enterprise,
                    # from:
                    "D4SmartFarming <soporte@d4smartfarming.com>",
                    # to:
                    [user['email']],#['soporte@d4smartfarming.com']
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                msg.send()
            # Mail para los Admins de la plataforma
            title = "=?utf-8?Q?=F0=9F=9A=A7_Aviso_de_l=C3=ADmite_de_hect=C3=A1reas?="
            email_html_message_admins = render_to_string('pasado_limite.html', context)
            if float(porcentaje) >= 100.00:
                title = "=?utf-8?Q?=F0=9F=8F=81_L=C3=ADmite_de_hect=C3=A1reas_excedido?="
                email_html_message_admins = render_to_string('excedido_limite.html', context)
            msg_adm = EmailMultiAlternatives(
                # title:
                title,
                # message:
                email_html_message_admins,
                # from:
                "D4SmartFarming <soporte@d4smartfarming.com>",
                # to:
                ['soporte@d4smartfarming.com'], ##PENDIENTE DE QUE NOS DEN LOS CORREOS
                #['soporte@d4smartfarming.com']
                # BCC
                ['backups@smartbits.es']
            )
            msg_adm.attach_alternative(email_html_message_admins, "text/html")
            msg_adm.send()
            
        super(Parcel, self).save(*args, **kwargs) 
        # set for loogin purpose
        request = get_request()
        message = 'Parcela creada'
        if object_id != 0:
            message = 'Parcela actualizada'

        if self.deleted_at is not None:
            message = 'Parcela actualizada (Eliminada)'

        contextLogs = {
            'user_email': request.user,
            'message': message,
            'status': 'success',
            'extra_data': {
                'id': self.id,
                'name': self.name,
                'area': self.area,
                'sentinel_instance': self.sentinel_instance,
                'area_calc': self.area_calc,
                'area_porc': self.area_porc
            }
        }  
        if request.method != 'DELETE':
            pass 
            #savelog(contextLogs,request)
         
