from rest_framework import viewsets

from .models import Enterprise
from .serializer import EnterpriseSerializer, EnterpriseSerializerCount, EnterpriseSerializerExcept

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class EnterpriseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.all()
        is_monitor = self.request.query_params.get('is_monitor', False)
        if is_monitor:
            # Filtrar solo los empresas que ejecuten monitor
            queryset = queryset.filter(is_monitor=True)
        return queryset

class EnterpriseViewSetCount(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializerCount

class EnterpriseViewSetExcept(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializerExcept

class EnterpriseViewSetActive(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Enterprise.objects.filter(is_active=True)
    serializer_class = EnterpriseSerializer

    model = Enterprise
    def get_queryset(self):
        profile = self.request.user.profile   
        #sacamos las propiedades del profile
        enterprise_id = profile.enterprise_id
        cooperative_user = profile.cooperative_user
        
        if cooperative_user:
            queryset = Enterprise.objects.filter(is_active=True, cooperative_id=enterprise_id).all()
            return queryset
        else:
            return Enterprise.objects.filter(is_active=True).all()
        #elif enterprise_id is None:
        #    return Enterprise.objects.filter(is_active=True).all()
        #else:
        #    queryset = Enterprise.objects.filter(id=enterprise_id).all()
        #    return queryset
class EnterpriseViewSetActiveAndMonitor(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Enterprise.objects.filter(is_active=True, is_monitor=True)
    serializer_class = EnterpriseSerializer
