import openpyxl
import numpy as np
from rest_framework import viewsets, generics, status

from django.core.serializers import serialize

from .models import Parcel, Campanas, Enterprise, Producciones, Siembras
from .serializer import CampanasSerializer, SiembrasSerializer, ProduccionesSerializer

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.http import HttpResponse
from datetime import datetime, timedelta, date

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import json
import asyncio
import time
import os
import decimal
import pandas as pd


from django.contrib.gis.gdal import DataSource
from django.core.files import File
from django.conf import settings

from trazas.utils import savelog

import json



class ImportCampanaFromFileViewset(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = Parcel

    def post(self, request, *args, **kwargs):

        anioHoy = date.today().year

        archivo = request.FILES["file"]
        print("INICIO LECTURA EXCEL")
        
        queryset_empresa = Enterprise.objects.filter(id=request.data["enterprise_id"]).first()
        
        if queryset_empresa:
            enterprise_id = queryset_empresa.id
            enterprise_sentinel_instance = queryset_empresa.sentinel_instance
            t = time.localtime()
            timestamp = time.strftime('%Y-%m-%d_%H%M', t) + "_"
            archivoExcel = settings.CAMPANA_FOLDER+timestamp+archivo.name

            # log purpuse
            contextLogs = {
                'user_email': request.user,
                'message': 'Usuario subiendo un .zip',
                'status': 'success',
                'extra_data': {
                    'confirm_import':request.data["confirm_import"],
                    'enterprise_id': str(request.data["enterprise_id"]),
                    'archivoExcel': archivoExcel,
                    'enterprise_sentinel_instance': enterprise_sentinel_instance,
                }
            }
            #savelog(contextLogs,request)
            # end log purpuse

            arrCampana = []
            arrSiembra = []
            arrProduccion = []
            arrErroresParcelas = []
            arrErroresSiembra = []
            arrErroresProduccion = []
            with open(archivoExcel, 'wb') as destination:
                for chunk in archivo.chunks():
                    destination.write(chunk)
                destination.close()
                # ----------- LECTURA DE PARCELAS
                print("PESTAÑA PARCELAS")
                sheetParcelas = pd.read_excel (archivoExcel, engine='openpyxl', sheet_name='Parcelas', header = 1)
                sheetParcelas = sheetParcelas.replace(np.nan, 0)
                for index, row in sheetParcelas.iterrows():
                    #Saltamos las filas en blanco y las cabeceras
                    if (str(row[1]) != "" and str(row[0]) != "ID. Parcela") :
                        encontrada = False
                        id_parcela = 0
                        porcentaje = 1
                        queryset_parcela = Parcel.objects.filter(id_importado=str(int(row[0])), enterprise=enterprise_id)
                        # si existe la parcela, cogemos sus datos
                        if queryset_parcela:
                            for parcela in queryset_parcela.iterator():
                                encontrada = True
                                id_parcela = parcela.id
                                porcentaje = parcela.area_porc / 100
                                arrCampana.append({"ID_PARCELA": id_parcela, "ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]), "CULTIVO": str(row[2]), "VARIEDAD": str(row[3]), "SUPERFICIE": row[4]*porcentaje, "PLANTAS": round(int(row[5])*porcentaje, 0), "PLANTAS_HA": row[6]*porcentaje, "OBSERVACIONES": row[16]})
                        if(encontrada == False):
                            queryset_multi = Parcel.objects.filter(id_importado__contains=str(int(row[0])) + "-", enterprise=enterprise_id)
                            for parcela in queryset_multi.iterator():
                                encontrada = True
                                id_parcela = parcela.id
                                porcentaje = parcela.area_porc / 100
                                arrCampana.append({"ID_PARCELA": id_parcela, "ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]), "CULTIVO": str(row[2]), "VARIEDAD": str(row[3]), "SUPERFICIE": row[4]*porcentaje, "PLANTAS": round(int(row[5])*porcentaje, 0), "PLANTAS_HA": row[6]*porcentaje, "OBSERVACIONES": row[16]})        
                        if(encontrada == False):
                            arrErroresParcelas.append({"ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]), 'ERROR' : 'No encontrada la parcela en el sistema'})         
                
                # ----------- LECTURA DE DATOS DE SIEMBRAS
                print("PESTAÑA SIEMBRAS")
                sheetSiembras = pd.read_excel (archivoExcel,engine='openpyxl', sheet_name='Siembras', header = 1)
                sheetSiembras = sheetSiembras.replace(np.nan, 0)
                for index, row in sheetSiembras.iterrows():
                    #Saltamos las filas en blanco y las cabeceras
                    if (str(row[1]) != "" and str(row[0]) != "ID. FINCA") :
                        encontrada = False
                        id_parcela = 0
                        porcentaje = 1
                        # row[3] = pd.to_datetime(row[3], format='%d/%m/%y')
                        queryset_parcela = Parcel.objects.filter(id_importado=str(int(row[0])), enterprise=enterprise_id)
                        # si existe la parcela, cogemos sus datos
                        if queryset_parcela:
                            for parcela in queryset_parcela.iterator():
                                encontrada = True
                                id_parcela = parcela.id
                                porcentaje = parcela.area_porc / 100
                                arrSiembra.append({"ID_PARCELA": id_parcela, "ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]), "FECHA_INICIO": str(row[3])[:10], "FECHA_FIN": str(row[4])[:10], "VARIEDAD": str(row[5]), "SUBVARIEDAD": str(row[6]), "TIPO_SIEMBRA": str(row[7]), "SUPERFICIE": row[8]*porcentaje, "SEMILLAS_HA": int(row[9])*porcentaje, "PLANTAS_TEORICAS_HA": int(row[10]*porcentaje), "PLANTAS_REALES_HA": int(row[11]*porcentaje), "VIVERO": str(row[12]), "TIPO_RIEGO": str(row[12])})

                        if(encontrada == False):
                            arrErroresSiembra.append({"ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]), 'ERROR' : 'No encontrada la parcela en el sistema'})

                # ----------- LECTURA DE DATOS DE PRODUCCION
                print("PESTAÑA PRODUCCION")
                sheetProduccion = pd.read_excel (archivoExcel,engine='openpyxl', sheet_name='Datos Producción', header = 1)
                sheetProduccion = sheetProduccion.replace(np.nan, 0)
                for index, row in sheetProduccion.iterrows():
                    #Saltamos las filas en blanco y las cabeceras
                    if (str(row[1]) != "" and str(row[2]) != "ID. Parcela") :
                        encontrada = False
                        id_parcela = 0
                        porcentaje = 1
                        # row[3] = pd.to_datetime(row[3], format='%d/%m/%y')
                        queryset_parcela = Parcel.objects.filter(id_importado=str(int(row[2])), enterprise=enterprise_id)
                        # si existe la parcela, cogemos sus datos
                        if queryset_parcela:
                            for parcela in queryset_parcela.iterator():
                                encontrada = True
                                id_parcela = parcela.id
                                porcentaje = parcela.area_porc / 100
                                arrProduccion.append({"ID_PARCELA": id_parcela, "ID_FINCA": str(int(row[2])), "PARCELA": str(row[3]), "FECHA": str(row[1])[:10], "CAMPANA": str(row[0]), "FECHA_INICIO": str(row[5])[:10], "FECHA_FIN": str(row[6])[:10], "PLANTAS": int(row[7])*porcentaje, "PRODUCCION": int(row[8])*porcentaje, "TIPO_UD": str(row[9]), "KG_PLANTA": row[10]*porcentaje, "KG_HA": row[11]*porcentaje, "AFORO": row[12]*porcentaje, "AFORO_PLANTA": row[13]*porcentaje, "AFORO_HA": row[14]*porcentaje, "DESVIACION": row[15]*porcentaje, "DESVIACION_PLANTA": row[16]*porcentaje, "DESVIACION_HA": row[17]*porcentaje, "VARIEDAD": str(row[18]), "SUBVARIEDAD": str(row[19])})

                        if(encontrada == False):
                            arrErroresProduccion.append({"ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]), 'ERROR' : 'No encontrada la parcela en el sistema'})
            
                # Confirmación de importación
                if request.data["confirm_import"] == "true":
                    # ----------- GUARDADO DE PARCELAS
                    print("GUARDAR PARCELAS")
                    for parcela in arrCampana:
                        try:
                            print(parcela["ID_PARCELA"])
                            queryset_campana = Campanas.objects.filter(parcela_id=parcela["ID_PARCELA"], name=parcela["CULTIVO"]).first()
                            if queryset_campana:
                                print("editar campaña")
                                # Si el registro existe, lo actualizamos
                                serializer = CampanasSerializer(queryset_campana, data={"name": parcela["CULTIVO"], "parcela": parcela["ID_PARCELA"], "variedad": str(parcela["VARIEDAD"]), "superficie": parcela["SUPERFICIE"], "plantas": parcela["PLANTAS"], "plantas_ha": parcela["PLANTAS_HA"], "observaciones": parcela["OBSERVACIONES"], "anio": anioHoy})
                            else:
                                print("nueva campaña")
                                # Si el registro es nuevo, lo insertamos
                                serializer = CampanasSerializer(data={"name": parcela["CULTIVO"], "parcela": parcela["ID_PARCELA"], "variedad": str(parcela["VARIEDAD"]), "superficie": parcela["SUPERFICIE"], "plantas": parcela["PLANTAS"], "plantas_ha": parcela["PLANTAS_HA"], "observaciones": parcela["OBSERVACIONES"], "anio": anioHoy})
                            serializer.is_valid(raise_exception=True)
                            serializer.save()

                            # log purpuse
                            contextLogs = {
                                'user_email': request.user,
                                'message': 'Campanas guardadas',
                                'status': 'success',
                                'extra_data': {
                                    'ID_PARCELA':parcela["ID_PARCELA"],
                                }
                            }
                            #savelog(contextLogs,request)
                            # end log purpuse

                        except Exception as Error:
                            print(str(Error))
                            # log purpuse
                            contextLogs = {
                                'user_email': request.user,
                                'message': 'Error Guardando Campanas',
                                'status': 'error',
                                'extra_data': {
                                    'error':str(Error),
                                }
                            }
                            #savelog(contextLogs,request)
                            # end log purpuse

                    # ----------- GUARDADO DE SIEMBRAS
                    print("GUARDAR SIEMBRAS")
                    for parcela in arrSiembra:
                        try:
                            print(parcela["ID_PARCELA"])
                            queryset_siembra = Siembras.objects.filter(parcela_id=parcela["ID_PARCELA"], anio=anioHoy).first()
                            if queryset_siembra:
                                print("editar siembra")
                                # Si el registro existe, lo actualizamos
                                serializer = SiembrasSerializer(queryset_siembra, data={"parcela": parcela["ID_PARCELA"], "fecha_inicio": datetime.strptime(parcela["FECHA_INICIO"], '%Y-%m-%d').date(), "fecha_fin": datetime.strptime(parcela["FECHA_FIN"], '%Y-%m-%d').date(), "anio": anioHoy, "variedad": parcela["VARIEDAD"], "subvariedad": parcela["SUBVARIEDAD"], "tipo_siembra": parcela["TIPO_SIEMBRA"], "superficie": parcela["SUPERFICIE"], "semillas_ha": parcela["SEMILLAS_HA"], "plantas_teoricas_ha": parcela["PLANTAS_TEORICAS_HA"], "plantas_reales_ha": parcela["PLANTAS_REALES_HA"], "vivero": parcela["VIVERO"], "tipo_riego": parcela["TIPO_RIEGO"]})
                            else:
                                print("nueva siembra")
                                # Si el registro es nuevo, lo insertamos
                                serializer = SiembrasSerializer(data={"parcela": parcela["ID_PARCELA"], "fecha_inicio": datetime.strptime(parcela["FECHA_INICIO"], '%Y-%m-%d').date(), "fecha_fin": datetime.strptime(parcela["FECHA_FIN"], '%Y-%m-%d').date(), "anio": anioHoy, "variedad": parcela["VARIEDAD"], "subvariedad": parcela["SUBVARIEDAD"], "tipo_siembra": parcela["TIPO_SIEMBRA"], "superficie": parcela["SUPERFICIE"], "semillas_ha": parcela["SEMILLAS_HA"], "plantas_teoricas_ha": parcela["PLANTAS_TEORICAS_HA"], "plantas_reales_ha": parcela["PLANTAS_REALES_HA"], "vivero": parcela["VIVERO"], "tipo_riego": parcela["TIPO_RIEGO"]})
                            serializer.is_valid(raise_exception=True)
                            serializer.save()
                            # log purpuse
                            contextLogs = {
                                'user_email': request.user,
                                'message': 'Siembras guardadas',
                                'status': 'success',
                                'extra_data': {
                                    'ID_PARCELA':parcela["ID_PARCELA"],
                                }
                            }
                            #savelog(contextLogs,request)
                            # end log purpuse

                        except Exception as Error:
                            print(str(Error))            
                            # log purpuse
                            contextLogs = {
                                'user_email': request.user,
                                'message': 'Error Guardando Siembras',
                                'status': 'error',
                                'extra_data': {
                                    'error':str(Error),
                                }
                            }
                            #savelog(contextLogs,request)
                            # end log purpuse            
                    
                    # ----------- GUARDADO DE PRODUCCIONES
                    print("GUARDAR PRODUCCION")
                    for parcela in arrProduccion:
                        try:
                            print(parcela["ID_PARCELA"])
                            queryset_produccion = Producciones.objects.filter(parcela_id=parcela["ID_PARCELA"], anio=anioHoy).first()
                            if queryset_produccion:
                                print("editar produccion")
                                # Si el registro existe, lo actualizamos
                                serializer = ProduccionesSerializer(queryset_produccion, data={"parcela": parcela["ID_PARCELA"], "campana": parcela["CAMPANA"], "anio": anioHoy, "fecha_registro": datetime.strptime(parcela["FECHA"], '%Y-%m-%d').date(), "fecha_inicio": datetime.strptime(parcela["FECHA_INICIO"], '%Y-%m-%d').date(), "fecha_fin": datetime.strptime(parcela["FECHA_FIN"], '%Y-%m-%d').date(), "plantas": parcela["PLANTAS"], "produccion": parcela["PRODUCCION"], "tipo_ud": parcela["TIPO_UD"], "kg_planta": parcela["KG_PLANTA"], "kg_ha": parcela["KG_HA"], "aforo": parcela["AFORO"], "aforo_plantas": parcela["AFORO_PLANTA"], "desviacion": parcela["DESVIACION"], "desviacion_planta": parcela["DESVIACION_PLANTA"], "desviacion_ha": parcela["DESVIACION_HA"], "variedad": parcela["VARIEDAD"], "subvariedad": parcela["SUBVARIEDAD"]})
                            else:
                                print("nueva produccion")
                                # Si el registro es nuevo, lo insertamos
                                serializer = ProduccionesSerializer(data={"parcela": parcela["ID_PARCELA"], "campana": parcela["CAMPANA"], "anio": anioHoy, "fecha_registro": datetime.strptime(parcela["FECHA"], '%Y-%m-%d').date(), "fecha_inicio": datetime.strptime(parcela["FECHA_INICIO"], '%Y-%m-%d').date(), "fecha_fin":datetime.strptime(parcela["FECHA_FIN"], '%Y-%m-%d').date(), "plantas": parcela["PLANTAS"], "produccion": parcela["PRODUCCION"], "tipo_ud": parcela["TIPO_UD"], "kg_planta": parcela["KG_PLANTA"], "kg_ha": parcela["KG_HA"], "aforo": parcela["AFORO"], "aforo_plantas": parcela["AFORO_PLANTA"], "desviacion": parcela["DESVIACION"], "desviacion_planta": parcela["DESVIACION_PLANTA"], "desviacion_ha": parcela["DESVIACION_HA"], "variedad": parcela["VARIEDAD"], "subvariedad": parcela["SUBVARIEDAD"]})
                            serializer.is_valid(raise_exception=True)
                            if(serializer.is_valid):
                                print("serializer OK")
                            serializer.save()

                            # log purpuse
                            contextLogs = {
                                'user_email': request.user,
                                'message': 'PRODUCCION guardadas',
                                'status': 'success',
                                'extra_data': {
                                    'ID_PARCELA':parcela["ID_PARCELA"],
                                }
                            }
                            #savelog(contextLogs,request)
                            # end log purpuse

                        except Exception as Error:
                            print(str(Error))            
                            # log purpuse
                            contextLogs = {
                                'user_email': request.user,
                                'message': 'Error Guardando PRODUCCION',
                                'status': 'error',
                                'extra_data': {
                                    'error':str(Error),
                                }
                            }
                            #savelog(contextLogs,request)
                            # end log purpuse                 

            if request.data["confirm_import"] == "false":
                os.remove(archivoExcel)

            return Response({"campanas" : arrCampana, "erroresParcelas" : arrErroresParcelas, "siembra" : arrSiembra, "erroresSiembra" : arrErroresSiembra, "produccion" : arrProduccion, "erroresProduccion" : arrErroresProduccion}, status=status.HTTP_200_OK)
        return Response({"campanas": "No se puede procesar", "Overlaps": "No se puede procesar", "totalparcelas": "No se puede procesar"}, status=status.HTTP_400_BAD_REQUEST)



class campanaViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Campanas.objects.all()
    serializer_class = CampanasSerializer

    @action(detail=False, methods=['post'])
    def data(self, request,*args, **kwargs):
        finicio = datetime.strptime(request.data['finicio'], '%Y-%m-%d')
        ffin = datetime.strptime(request.data["ffin"], '%Y-%m-%d')
        # Establecemos los dias que hay entre las dos fechas
        arrFechas = pd.date_range(finicio,ffin).format(formatter=lambda x: x.strftime('%Y'))
        data = {}
        for fecha in arrFechas:
            queryset = Campanas.objects.filter(anio = int(fecha), parcela_id__in=request.data["parcels"]).all()
            arrResultados = []
            if len(queryset):
                for result in queryset:
                    arrResultados.append(CampanasSerializer(result).data)
                data[fecha] = {"resultado": arrResultados}

        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['POST'])
    def getplantas(self, request,*args, **kwargs):
        queryset = Campanas.objects.filter(anio__in = request.data["anios"], parcela_id__in=request.data["parcelas"]).all()
        data = []
        if len(queryset):
            for result in queryset:
                data.append(CampanasSerializer(result).data)
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['PUT'])
    def recogida(self, request,*args, **kwargs):
        print (request.data['fecha'])
        fecha=datetime.strptime(request.data['fecha'], '%Y-%m-%d').date()
        Campanas.objects.filter(parcela_id__in=request.data["parcelas"]).update(fecha_recogida_estimada=fecha)
        return Response({"data": "OK"})



class siembraViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Siembras.objects.all()
    serializer_class = SiembrasSerializer

    @action(detail=False, methods=['post'])
    def data(self, request,*args, **kwargs):
        finicio = datetime.strptime(request.data["finicio"], '%Y-%m-%d')
        ffin = datetime.strptime(request.data["ffin"], '%Y-%m-%d')
        # Establecemos los dias que hay entre las dos fechas
        arrFechas = pd.date_range(finicio,ffin).format(formatter=lambda x: x.strftime('%Y'))
        data = {}
        for fecha in arrFechas:
            queryset = Siembras.objects.filter(anio = int(fecha), parcela_id__in=request.data["parcels"]).all()
            arrResultados = []
            if len(queryset):
                for result in queryset:
                    arrResultados.append(SiembrasSerializer(result).data)
                data[fecha] = {"resultado": arrResultados}

        return Response(data, status=status.HTTP_200_OK)


class produccionViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Producciones.objects.all()
    serializer_class = ProduccionesSerializer

    @action(detail=False, methods=['post'])
    def data(self, request, *args, **kwargs):
        finicio = datetime.strptime(request.data["finicio"], '%Y-%m-%d')
        ffin = datetime.strptime(request.data["ffin"], '%Y-%m-%d')
        # Establecemos los dias que hay entre las dos fechas
        arrFechas = pd.date_range(finicio,ffin).format(formatter=lambda x: x.strftime('%Y'))
        data = {}
        for fecha in arrFechas:
            queryset = Producciones.objects.filter(anio = int(fecha), parcela_id__in=request.data["parcels"]).all()
            arrResultados = []
            if len(queryset):
                for result in queryset:
                    arrResultados.append(ProduccionesSerializer(result).data)
                data[fecha] = {"resultado": arrResultados}

        return Response(data, status=status.HTTP_200_OK) 

    @action(detail=False, methods=['POST'])
    def getproduccion(self, request,*args, **kwargs):
        queryset = Producciones.objects.filter(anio__in = request.data["anios"], parcela_id__in=request.data["parcelas"]).all()
        data = []
        if len(queryset):
            for result in queryset:
                data.append(ProduccionesSerializer(result).data)
        return Response(data, status=status.HTTP_200_OK)
    
