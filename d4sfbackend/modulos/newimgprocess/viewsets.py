from django.conf import settings
from rest_framework import viewsets, generics,status
from .models import NewImagenPro
from modulos.parcelas.models import Parcel
from modulos.user.models import User
from modulos.profiles.models import UserProfile
from .serializer import NewImagenProSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.gis.geos import GEOSGeometry, polygon
from threading import Thread
from .procesar_NDVI import ndviImgT2
from .procesar_MOISTURE_INDEX import procesar_moisture
from .procesar_fechas import ndvi_img_fechas, get_bbox
import pandas as pd
import uuid
from .jsontoexcel import json2xlsx

from modulos.trazas.utils import savelog,getRequestIp

class NewImagenProViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = NewImagenPro.objects.all()
    serializer_class = NewImagenProSerializer
    model = NewImagenPro

    def get_queryset(self):
        enterprise_id = self.request.query_params.get('enterprise_id') or 'all'
        colum_name = self.request.query_params.get('colum_name')
        order = self.request.query_params.get('order')
        if enterprise_id is None or enterprise_id == 'undefined' or enterprise_id == 'all':
            if order == 'descending':
                return NewImagenPro.objects.all().order_by("-"+colum_name)
            else:
                return NewImagenPro.objects.all().order_by(colum_name)
        else:
            if order == 'descending':
                return NewImagenPro.objects.filter(enterprise_id=enterprise_id).order_by("-"+colum_name)
            else:
                return NewImagenPro.objects.filter(enterprise_id=enterprise_id).order_by(colum_name)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        capa = serializer.validated_data['capa']
        email = self.request.user
        usersPer = UserProfile.objects.select_related('user').filter(user__email=email)
        name = usersPer[0].__dict__['first_name']
        uid = usersPer[0].__dict__['id']
        if capa == 'NDVI':
            t = Thread(target=ndviImgT2, kwargs=dict(serializer=serializer, email_user=email, name_user=name, uid=uid))
            t.start()
        elif capa == 'MOISTURE_INDEX':
            t = Thread(target=procesar_moisture, kwargs=dict(serializer=serializer, email_user=email, name_user=name, uid=uid, request=self.request))
            t.start()
        
        """ # consultar al modelo parcelas de la conexion default_origen
        parcelas = Parcel.objects.using('default_origen').filter(enterprise_id='5acc1450-10b3-40a7-b9ea-097c5f3d1ea7')

        # guardo los registros de la variable parcelas en la base de datos de la conexion default
        for parcela in parcelas:
            parcela.save(using='default') """

        
        return Response({"data" : "OK"})

    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        id_parcelas = serializer.validated_data['id_parcelas']
        print(id_parcelas)
        NewImagenPro.objects.filter(pk__in=id_parcelas).delete()
        # log purpuse
        contextLogs = {
            'user_email': request.user,
            'message': 'Usuario solicita eliminar archivo',
            'status': 'success',
            'extra_data': {
                'id_parcelas': id_parcelas
            }
        }
        #savelog(contextLogs,request)
        # end log purpuse
        return Response({"data": "OK"})

    def put(self, request, pk=None):
        nombre = request.data['nombre']
        id = request.data['id']
        NewImagenPro.objects.filter(pk=id).update(nombre=nombre)
        # log purpuse
        contextLogs = {
            'user_email': request.user,
            'message': 'Usuario solicita Actualizar archivo',
            'status': 'success',
            'extra_data': {
                'id': id
            }
        }
        #savelog(contextLogs,request)
        # end log purpuse
        return Response({"data": "OK"})

class NewImagenProFechasViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = NewImagenPro.objects.all()
    serializer_class = NewImagenProSerializer
    model = NewImagenPro

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_parcelas = serializer.validated_data['id_parcelas']
        retorno = ndvi_img_fechas(serializer)
        return Response(retorno)

class NewImagenProGetBBoxViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = NewImagenPro.objects.all()
    serializer_class = NewImagenProSerializer
    model = NewImagenPro

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_parcelas = serializer.validated_data['id_parcelas']
        retorno = get_bbox(serializer)
        # log purpuse
        contextLogs = {
            'user_email': request.user,
            'message': 'Usuario solicitando fechas /getbbox/ NewImagenProGetBBoxViewSet',
            'status': 'succes',
            'extra_data': {
                'id_parcelas': id_parcelas,
                'request':request.data
            }
        }
        #savelog(contextLogs,request)
        # end log purpuse
        return Response(retorno)

class NewImagenProUnificarViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = NewImagenPro.objects.all()
    serializer_class = NewImagenProSerializer
    model = NewImagenPro

    def put(self, request, pk=None):
        email = self.request.user
        usersPer = UserProfile.objects.select_related('user').filter(user__email=email)
        uid = usersPer[0].__dict__['id']
        nombre = request.data['nombre']
        capa = request.data['capa']
        enterprise_id = request.data['enterprise_id']
        check_dell = request.data['check_dell']
        informes_sel = request.data['informes_sel']

        arrPandasDf = []
        fechasInicio = []
        fechasFin = []
        arrRespuesta = []
        for informe in informes_sel:
            json = pd.read_json(settings.PARCEL_FOLDER + informe['jsonFile'])
            arrPandasDf.append(json)
            fechasInicio.append(informe['fechaInicio'])
            fechasFin.append(informe['fechaFin'])
            print(informe['nombre'])
        for dataFrame in arrPandasDf:
            for dictt in dataFrame.to_dict():
                arrRespuesta.append(dataFrame.to_dict().get(dictt))
        df = pd.DataFrame(arrRespuesta)
        print(df)
        nombreJson = str(uuid.uuid1().int) + '.json'
        df.transpose().to_json(settings.PARCEL_FOLDER + nombreJson)
        dfSort = df.sort_values('fecha', ascending=True)
        fechaInicio = dfSort['fecha'].iloc[0]
        fechaFin = dfSort['fecha'].iloc[-1]
        dfSort.index = range(len(dfSort.index))
        dfSort.transpose().to_json(settings.PARCEL_FOLDER + 'order_' + nombreJson)
        print(fechaInicio)
        print(fechaFin)
        print(capa)
        nombreXlsx = str(uuid.uuid1().int) + '.xlsx'
        json2xlsx('order_' + nombreJson, nombreXlsx, capa)
        NewImagenPro.objects.create(nombre=nombre, capa=capa, fechaInicio=fechaInicio, fechaFin=fechaFin,
                                    enterprise_id=enterprise_id, esCooperative=False, jsonFile=nombreJson,
                                    xlsxFile=nombreXlsx, id_parcelas='', includeClouds=False, user_created=uid,
                                    esUnificado=True)
        if check_dell:
            for informe in informes_sel:
                NewImagenPro.objects.filter(pk=informe['id']).delete()
        #NewImagenPro.objects.filter(pk=id).update(nombre=nombre)
        # serializer.save(nombre=nombre, capa=capa, fechaInicio=fechaInicio, fechaFin=fechaFin,
        #                         enterprise_id=enterprise_id, esCooperative=esCooperative, jsonFile=nombreJson,
        #                         xlsxFile=nombreXlsx, id_parcelas='', includeClouds=includeClouds, user_created=uid)
        return Response({"data": "OK"})


# Metodos para generar excel con imagenes
class GenerarExcelViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = NewImagenPro.objects.all()
    serializer_class = NewImagenProSerializer

    @action(detail=False, methods=['POST'])
    def generar(self, request,*args, **kwargs):
        queryset = NewImagenPro.objects.filter(id=request.data['id']).all()
        informes = []
        data={}
        if len(queryset):
            for result in queryset:
                informes.append(NewImagenProSerializer(result).data)
        xlsx=informes[0]['xlsxFile']
        xlsxName=xlsx[0:38]+"img"+'.xlsx'    
        json2xlsx("order_"+str(informes[0]['jsonFile']),xlsxName, informes[0]['capa'],1)
        data=xlsxName
        name=str(informes[0]['nombre'])
        return Response({"data":data, "name":name}, status=status.HTTP_200_OK)