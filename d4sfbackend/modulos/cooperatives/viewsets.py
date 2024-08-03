from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from modulos.cooperatives.models import Cooperative
from modulos.cooperatives.serializer import CooperativeSerializer, CooperativeSerializerRR
from modulos.enterprises.models import Enterprise


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
        Enterprise.objects.filter(cooperative=id_cooperativa).update(cooperative='')
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
        Enterprise.objects.filter(id__in=id_empresas).update(cooperative=cooperativa_id)
        return Response(data='OK')


class CooperativeViewsetOnEnRlt(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    model = Cooperative

    def get_queryset(self):
        # Filtrar las empresas con is_monitor=True
        # return Cooperative.objects.filter(enterprise__in=empresas_monitor).order_by('-name')
        queryset = Cooperative.objects.filter(enterprises__is_monitor=True).distinct()
        return queryset


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
        Enterprise.objects.filter(cooperative=id_cooperativa).update(cooperative='')
        cooperative.delete()
        return Response(data='OK')
