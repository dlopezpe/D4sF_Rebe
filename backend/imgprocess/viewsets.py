from django.conf import settings
from rest_framework import viewsets, generics

from django.core.serializers import serialize

from .models import ImagenPro
from parcelas.models import Parcel
from user.models import User
from profiles.models import UserProfile
from .serializer import ImagenProSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.http import HttpResponse

from django.contrib.gis.geos import GEOSGeometry

import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import uuid
import urllib.request

from .jsontoexcel import json2xlsx

import codecs, json
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import time
from datetime import datetime
import pandas as pd
client_id = '33467c23-fada-4405-8a5b-33ee38169273'
client_secret = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
hed = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type' : 'client_credentials'
}

from .procesadoImagenesNDVI import ndviImgT2, ndviImgT1
from .procesadoImagenesMOISTURE import moistureImgT2, moistureImgT1
import asyncio
from asgiref.sync import sync_to_async
from threading import Thread
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

class ImagenProViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = ImagenPro.objects.all()
    serializer_class = ImagenProSerializer
    model = ImagenPro

    def get_queryset(self):
        enterprise_id = self.request.query_params.get('enterprise_id')
        colum_name = self.request.query_params.get('colum_name')
        order = self.request.query_params.get('order')
        if order == 'descending':
            return ImagenPro.objects.filter(enterprise_id=enterprise_id).order_by('-'+colum_name)
        else:
            return ImagenPro.objects.filter(enterprise_id=enterprise_id).order_by(colum_name)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        capa = serializer.validated_data['capa']
        # BUSCAMOS EL NOMBRE DE USUARIO A PARTIR DEL MAIL
        email = self.request.user
        usersPer = UserProfile.objects.select_related('user').filter(user__email = email)
        name = usersPer[0].__dict__['first_name']
        if capa == 'NDVI':
            #asyncio.run(ndviImgT2(serializer, self.request.user))
            t = Thread(target = ndviImgT1, kwargs=dict(serializer=serializer, email_user = email, name_user = name))
            #t.daemon = True
            t.start()
        elif capa == 'MOISTURE_INDEX':
            t = Thread(target = moistureImgT1, kwargs=dict(serializer=serializer, email_user = email, name_user = name))
            #t.daemon = True
            t.start()
        return Response({"data" : "OK"})


class ImagenProViewSetAll(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = ImagenPro.objects.all()
    serializer_class = ImagenProSerializer

    def get_queryset(self):
        return ImagenPro.objects.all()

class ImagenProViewSetTypeTwo(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = ImagenPro.objects.all()
    serializer_class = ImagenProSerializer
    model = ImagenPro

    def get_queryset(self):
        return ImagenPro.objects.all()
    

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        capa = serializer.validated_data['capa']
        # BUSCAMOS EL NOMBRE DE USUARIO A PARTIR DEL MAIL
        email = self.request.user
        usersPer = UserProfile.objects.select_related('user').filter(user__email = email)
        name = usersPer[0].__dict__['first_name']
        if capa == 'NDVI':
            #asyncio.run(ndviImgT2(serializer, self.request.user))
            t = Thread(target = ndviImgT2, kwargs=dict(serializer=serializer, email_user = email, name_user = name))
            #t.daemon = True
            t.start()
        elif capa == 'MOISTURE_INDEX':
            t = Thread(target = moistureImgT2, kwargs=dict(serializer=serializer, email_user = email, name_user = name))
            #t.daemon = True
            t.start()
        return Response({"data" : "OK"})

class ImagenProViewSetUnificar(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = ImagenPro.objects.all()
    serializer_class = ImagenProSerializer
    model = ImagenPro

    def get_queryset(self):
        return ImagenPro.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        urlSent = serializer.validated_data['urlSentinel']
        parcela = serializer.validated_data['parcela']
        polygon = serializer.validated_data['polygon']
        capa = serializer.validated_data['capa']
        tipo = serializer.validated_data['tipo']
        enterprise_id = serializer.validated_data['enterprise_id']
        checkDellOtros = serializer.validated_data['checkDellOtros']
        alias = serializer.validated_data['alias'] or ''
        arrPandasDf = []
        arrFechas = []
        arrId = []
        for informe in polygon[0]:
            results = ImagenPro.objects.filter(id=informe.get('id'))
            arrId.append(informe.get('id'))
            for result in results:
                json = pd.read_json(settings.PARCEL_FOLDER+result.__dict__['imagen'])
                fecha = result.__dict__['finifin']
                arrFechas.append(result.__dict__['finifin'])
                if tipo == 2:
                    if 'fechaGeneada' in json.index:
                        json.rename(index={'fechaGeneada': 'fechaGenerada'}, inplace=True)
                    else:
                        df1 = pd.DataFrame(np.repeat(fecha, len(json.columns))[None, :], columns=json.columns, index=['fechaGenerada'])
                        json = pd.concat([json, df1])
                arrPandasDf.append(json)
        arrRespuesta = []
        for dataFrame in arrPandasDf:
            for dictt in dataFrame.to_dict():
                arrRespuesta.append(dataFrame.to_dict().get(dictt))
        df = pd.DataFrame(arrRespuesta)
        fechaElegida = ''

        if tipo == 2:
            dfSort = df.sort_values('fechaGenerada')
            dfSort.index = range(len(dfSort.index))
            fechaElegida = dfSort['fechaGenerada'].iloc[0]+' - '+dfSort['fechaGenerada'].iloc[-1]
            df = dfSort
            df = df.loc[df.astype(str).drop_duplicates(subset=['fechaGenerada', 'fecha']).index]
        elif tipo == 1:
            dfSort = df.sort_values('fecha')
            dfSort.index = range(len(dfSort.index))
            fechaElegida = dfSort['fecha'].iloc[0]+' - '+dfSort['fecha'].iloc[-1]
            df = dfSort
            df = df.loc[df.astype(str).drop_duplicates(subset=['fecha']).index]
        
        #GUARDADOS
        eventid = datetime.now().strftime('%Y%m-%d%H-%M%S-')
        nombreJson = str(eventid)+'.json'
        nombreXlsx = str(eventid)+'.xlsx'
        df.transpose().to_json(settings.PARCEL_FOLDER+nombreJson)
        json2xlsx(nombreJson, nombreXlsx, capa)
        if parcela == 0:
            parcela = 'Gráfico Tipo 2'
        finicioFin = fechaElegida
        if not fechaElegida:
            finicioFin = datetime.now().strftime('%Y-%m-%d')
        if serializer.save(parcela=parcela, urlSentinel="https://", imagen=nombreJson, xlsxFile=nombreXlsx, finifin=finicioFin, tipo=tipo, polygon=[], fechas=datetime.now().strftime('%Y-%m-%d - %H:%M:%S'), capa=capa, fechaElegida=fechaElegida, checkDellOtros=checkDellOtros, alias=alias):
            colorPrint('Creado')
            if(checkDellOtros):
                ImagenPro.objects.filter(id__in=arrId).delete()
        return Response(arrRespuesta)
