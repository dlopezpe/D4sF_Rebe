from rest_framework import viewsets, generics

from .models import Cooperative
from enterprises.models import Enterprise
from enterprises.serializer import EnterpriseSerializer
from .serializer import CooperativeSerializer, CooperativeSerializerOnlyEnterprisesRelated, CooperativeSerializerRR

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response

from django.http import JsonResponse


class CooperativeViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    model = Cooperative

    def get_queryset(self):
        return Cooperative.objects.all().order_by('-name')

    def destroy(self, request, *args, **kwargs):
        cooperative = self.get_object()
        id_cooperativa = cooperative.id
        Enterprise.objects.filter(cooperative = id_cooperativa).update(cooperative = '')
        cooperative.delete()
        return Response(data='OK')

class CooperativeInsViewset(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    model = Cooperative

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_empresas = request.data['id_empresas']
        cooperativa = serializer.save()
        cooperativa_id = cooperativa.id
        Enterprise.objects.filter(id__in=id_empresas).update(cooperative = cooperativa_id)
        return Response(data='OK')

class CooperativeViewsetOnEnRlt(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    model = Cooperative

    def get_queryset(self):
        # Filtrar las empresas con is_monitor=True
        #return Cooperative.objects.filter(enterprise__in=empresas_monitor).order_by('-name')
        queryset = Cooperative.objects.filter(enterprises__is_monitor=True, enterprises__is_active = True).distinct()
        return queryset
    
    #del objeto cooperative tenemos que filtrar en enterprises solo las que tengan is_monitor=True
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        enterprises = data['enterprises']
        enterprises = [enterprise for enterprise in enterprises if enterprise['is_active'] == True]
        data['enterprises'] = enterprises
        return Response(data)

class CooperativeViewsetUpdate(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializerRR
    model = Cooperative

    def get_queryset(self):
        return Cooperative.objects.all().order_by('-name')

    def destroy(self, request, *args, **kwargs):
        cooperative = self.get_object()
        id_cooperativa = cooperative.id
        Enterprise.objects.filter(cooperative = id_cooperativa).update(cooperative = '')
        cooperative.delete()
        return Response(data='OK')
