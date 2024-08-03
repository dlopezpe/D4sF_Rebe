import logging
import os
import time
from datetime import datetime, date

import numpy as np
import pandas as pd
from django.conf import settings
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.Utils import save_log
from .models import Parcel, Campanas, Producciones, Siembras
from .serializer import CampanasSerializer, SiembrasSerializer, ProduccionesSerializer
from ..enterprises.models import Enterprise


def add_parcelas(row, queryset, encontrada, arr_parcelas, arr_errores_parcelas):
    for parcela in queryset.iterator():
        encontrada = True
        id_parcela = parcela.id
        porcentaje = parcela.area_porc / 100
        arr_parcelas.append(
            {"ID_PARCELA": id_parcela, "ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]),
             "CULTIVO": str(row[2]), "VARIEDAD": str(row[3]), "SUPERFICIE": row[4] * porcentaje,
             "PLANTAS": round(int(row[5]) * porcentaje, 0), "PLANTAS_HA": row[6] * porcentaje,
             "OBSERVACIONES": row[16]})

    if not encontrada:
        arr_errores_parcelas.append({"ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]),
                                     'ERROR': 'No encontrada la parcela en el sistema'})

    return arr_parcelas, arr_errores_parcelas


def add_siembras(row, queryset, encontrada, arr_siembra, arr_errores_siembra):
    for parcela in queryset.iterator():
        encontrada = True
        id_parcela = parcela.id
        porcentaje = parcela.area_porc / 100
        arr_siembra.append(
            {"ID_PARCELA": id_parcela, "ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]),
             "FECHA_INICIO": str(row[3])[:10], "FECHA_FIN": str(row[4])[:10],
             "VARIEDAD": str(row[5]), "SUBVARIEDAD": str(row[6]),
             "TIPO_SIEMBRA": str(row[7]),
             "SUPERFICIE": row[8] * porcentaje, "SEMILLAS_HA": int(row[9]) * porcentaje,
             "PLANTAS_TEORICAS_HA": int(row[10] * porcentaje),
             "PLANTAS_REALES_HA": int(row[11] * porcentaje), "VIVERO": str(row[12]),
             "TIPO_RIEGO": str(row[12])})

    if not encontrada:
        arr_errores_siembra.append({"ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]),
                                    'ERROR': 'No encontrada la parcela en el sistema'})

    return arr_siembra, arr_errores_siembra


def add_producciones(row, queryset, encontrada, arr_produccion, arr_errores_produccion):
    for parcela in queryset.iterator():
        encontrada = True
        id_parcela = parcela.id
        porcentaje = parcela.area_porc / 100
        arr_produccion.append(
            {"ID_PARCELA": id_parcela, "ID_FINCA": str(int(row[2])), "PARCELA": str(row[3]),
             "FECHA": str(row[1])[:10], "CAMPANA": str(row[0]),
             "FECHA_INICIO": str(row[5])[:10], "FECHA_FIN": str(row[6])[:10],
             "PLANTAS": int(row[7]) * porcentaje, "PRODUCCION": int(row[8]) * porcentaje,
             "TIPO_UD": str(row[9]), "KG_PLANTA": row[10] * porcentaje,
             "KG_HA": row[11] * porcentaje, "AFORO": row[12] * porcentaje,
             "AFORO_PLANTA": row[13] * porcentaje, "AFORO_HA": row[14] * porcentaje,
             "DESVIACION": row[15] * porcentaje, "DESVIACION_PLANTA": row[16] * porcentaje,
             "DESVIACION_HA": row[17] * porcentaje, "VARIEDAD": str(row[18]),
             "SUBVARIEDAD": str(row[19])})

    if not encontrada:
        arr_errores_produccion.append({"ID_FINCA": str(int(row[0])), "PARCELA": str(row[1]),
                                       'ERROR': 'No encontrada la parcela en el sistema'})
    return arr_produccion, arr_errores_produccion


def read_sheet(pestania, archivo_excel, enterprise_id, id_row):
    logging.debug("PESTAÑA %s", pestania)

    sheet = pd.read_excel(archivo_excel, engine='openpyxl', sheet_name=pestania, header=1)
    sheet = sheet.replace(np.nan, 0)

    arr_parcelas = []
    arr_siembra = []
    arr_produccion = []

    arr_errores_parcelas = []
    arr_errores_siembra = []
    arr_errores_produccion = []

    for index, row in sheet.iterrows():
        # Saltamos las filas en blanco y las cabeceras
        if str(row[1]) != "" and str(row[0]) != id_row:
            if pestania == 'Parcelas':
                # Añadimos la campaña
                encontrada = False
                queryset = Parcel.objects.filter(id_importado=str(int(row[0])),
                                                 enterprise=enterprise_id)
                # si existe la parcela, cogemos sus datos
                if queryset:
                    arr_parcelas, arr_errores_parcelas = add_parcelas(row, queryset, encontrada, arr_parcelas,
                                                                      arr_errores_parcelas)
                if not encontrada:
                    queryset_multi = Parcel.objects.filter(id_importado__contains=str(int(row[0])) + "-",
                                                           enterprise=enterprise_id)

                    # Añadimos la campaña
                    arr_parcelas, arr_errores_parcelas = add_parcelas(row, queryset_multi, encontrada, arr_parcelas,
                                                                      arr_errores_parcelas)
                return arr_parcelas, arr_errores_parcelas

            elif pestania == 'Siembras':
                # Añadimos la siembra
                encontrada = False
                queryset = Parcel.objects.filter(id_importado=str(int(row[0])), enterprise=enterprise_id)
                # si existe la siembra, cogemos sus datos
                if queryset:
                    arr_siembra, arr_errores_siembra = add_siembras(row, queryset, encontrada, arr_siembra,
                                                                    arr_errores_siembra)

                return arr_siembra, arr_errores_siembra

            elif pestania == 'Datos Producción':
                # Añadimos la produccion
                encontrada = False
                queryset = Parcel.objects.filter(id_importado=str(int(row[2])), enterprise=enterprise_id)
                # si existe la produccion, cogemos sus datos
                if queryset:
                    arr_produccion, arr_errores_produccion = add_producciones(row, queryset, encontrada, arr_produccion,
                                                                              arr_errores_produccion)
                return arr_produccion, arr_errores_produccion

            else:
                logging.error("No es correcta el nombre de la pestaña %s", pestania)


def save_parcela(arr_parcelas, request, anio_hoy):
    for parcela in arr_parcelas:
        try:
            logging.debug(parcela["ID_PARCELA"])
            queryset_campana = Campanas.objects.filter(parcela_id=parcela["ID_PARCELA"],
                                                       name=parcela["CULTIVO"]).first()
            data_parcela = {
                "name": parcela["CULTIVO"],
                "parcela": parcela[
                    "ID_PARCELA"],
                "variedad": str(
                    parcela["VARIEDAD"]),
                "superficie": parcela[
                    "SUPERFICIE"],
                "plantas": parcela["PLANTAS"],
                "plantas_ha": parcela[
                    "PLANTAS_HA"],
                "observaciones": parcela[
                    "OBSERVACIONES"],
                "anio": anio_hoy}
            if queryset_campana:
                logging.debug("editar campaña")
                # Si el registro existe, lo actualizamos
                serializer = CampanasSerializer(queryset_campana, data=data_parcela)
            else:
                logging.debug("nueva campaña")
                # Si el registro es nuevo, lo insertamos
                serializer = CampanasSerializer(data=data_parcela)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            # log purpuse
            extra_data = {
                'ID_PARCELA': parcela["ID_PARCELA"],
            }
            save_log('Campaña guardada', request, extra_data)

        except Exception as Error:
            logging.debug(str(Error))
            # log purpuse
            extra_data = {
                'ID_PARCELA': parcela["ID_PARCELA"],
                'error': str(Error),
            }
            save_log('Error al guardar la campañas', request, extra_data)


def save_produccion(arr_produccion, request, anio_hoy):
    for parcela in arr_produccion:
        try:
            logging.debug(parcela["ID_PARCELA"])
            queryset_produccion = Producciones.objects.filter(parcela_id=parcela["ID_PARCELA"],
                                                              anio=anio_hoy).first()

            data_produccion = {"parcela": parcela["ID_PARCELA"], "campana": parcela["CAMPANA"],
                               "anio": anio_hoy,
                               "fecha_registro": datetime.strptime(parcela["FECHA"], '%Y-%m-%d').date(),
                               "fecha_inicio": datetime.strptime(parcela["FECHA_INICIO"], '%Y-%m-%d').date(),
                               "fecha_fin": datetime.strptime(parcela["FECHA_FIN"], '%Y-%m-%d').date(),
                               "plantas": parcela["PLANTAS"], "produccion": parcela["PRODUCCION"],
                               "tipo_ud": parcela["TIPO_UD"], "kg_planta": parcela["KG_PLANTA"],
                               "kg_ha": parcela["KG_HA"], "aforo": parcela["AFORO"],
                               "aforo_plantas": parcela["AFORO_PLANTA"], "desviacion": parcela["DESVIACION"],
                               "desviacion_planta": parcela["DESVIACION_PLANTA"],
                               "desviacion_ha": parcela["DESVIACION_HA"], "variedad": parcela["VARIEDAD"],
                               "subvariedad": parcela["SUBVARIEDAD"]}
            if queryset_produccion:
                logging.debug("editar produccion")
                # Si el registro existe, lo actualizamos
                serializer = ProduccionesSerializer(queryset_produccion,
                                                    data=data_produccion)
            else:
                logging.debug("nueva produccion")
                # Si el registro es nuevo, lo insertamos
                serializer = ProduccionesSerializer(data=data_produccion)

            serializer.is_valid(raise_exception=True)

            if serializer.is_valid:
                logging.debug("serializer OK")
            serializer.save()

            # log purpuse
            extra_data = {
                'ID_PARCELA': parcela["ID_PARCELA"],
            }
            save_log('Produccion guardada', request, extra_data)

        except Exception as Error:
            logging.debug(str(Error))
            # log purpuse
            extra_data = {
                'ID_PARCELA': parcela["ID_PARCELA"],
                'error': str(Error),
            }
            save_log('Error al guardar la produccion', request, extra_data)


def save_siembra(arr_siembra, request, anio_hoy):
    for parcela in arr_siembra:
        try:
            logging.debug(parcela["ID_PARCELA"])
            queryset_siembra = Siembras.objects.filter(parcela_id=parcela["ID_PARCELA"],
                                                       anio=anio_hoy).first()
            data_siembra = {
                "parcela": parcela["ID_PARCELA"],
                "fecha_inicio": datetime.strptime(
                    parcela["FECHA_INICIO"], '%Y-%m-%d').date(),
                "fecha_fin": datetime.strptime(
                    parcela["FECHA_FIN"], '%Y-%m-%d').date(),
                "anio": anio_hoy, "variedad": parcela["VARIEDAD"],
                "subvariedad": parcela["SUBVARIEDAD"],
                "tipo_siembra": parcela["TIPO_SIEMBRA"],
                "superficie": parcela["SUPERFICIE"],
                "semillas_ha": parcela["SEMILLAS_HA"],
                "plantas_teoricas_ha": parcela[
                    "PLANTAS_TEORICAS_HA"],
                "plantas_reales_ha": parcela["PLANTAS_REALES_HA"],
                "vivero": parcela["VIVERO"],
                "tipo_riego": parcela["TIPO_RIEGO"]
            }
            if queryset_siembra:
                logging.debug("editar siembra")
                # Si el registro existe, lo actualizamos
                serializer = SiembrasSerializer(queryset_siembra, data=data_siembra)
            else:
                logging.debug("nueva siembra")
                # Si el registro es nuevo, lo insertamos
                serializer = SiembrasSerializer(data=data_siembra)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            # log purpuse
            extra_data = {
                'ID_PARCELA': parcela["ID_PARCELA"],
            }
            save_log('Siembra guardada', request, extra_data)

        except Exception as Error:
            logging.debug(str(Error))
            # log purpuse
            extra_data = {
                'ID_PARCELA': parcela["ID_PARCELA"],
                'error': str(Error),
            }
            save_log('Error al guardar la siembra', request, extra_data)


class ImportCampanaFromFileViewset(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = Parcel

    @staticmethod
    def post(request, *args, **kwargs):

        anio_hoy = date.today().year

        archivo = request.FILES["file"]
        logging.debug("INICIO LECTURA EXCEL")

        queryset_empresa = Enterprise.objects.filter(id=request.data["enterprise_id"]).first()

        if queryset_empresa:
            enterprise_id = queryset_empresa.id
            enterprise_sentinel_instance = queryset_empresa.sentinel_instance
            t = time.localtime()
            timestamp = time.strftime('%Y-%m-%d_%H%M', t) + "_"
            archivo_excel = settings.CAMPANA_FOLDER + timestamp + archivo.name

            # log purpuse
            extra_data = {
                'confirm_import': request.data["confirm_import"],
                'enterprise_id': str(request.data["enterprise_id"]),
                'archivoExcel': archivo_excel,
                'enterprise_sentinel_instance': enterprise_sentinel_instance,
            }
            save_log('Usuario subiendo un .zip', request, extra_data)

            with open(archivo_excel, 'wb') as destination:
                for chunk in archivo.chunks():
                    destination.write(chunk)
                destination.close()

                # ----------- LECTURA DE PARCELAS
                arr_parcelas, arr_errores_parcelas = read_sheet('Parcelas', archivo_excel, enterprise_id,
                                                                "ID. Parcela")

                # ----------- LECTURA DE DATOS DE SIEMBRAS
                arr_siembra, arr_errores_siembra = read_sheet('Siembras', archivo_excel, enterprise_id,
                                                              "ID. FINCA")

                # ----------- LECTURA DE DATOS DE PRODUCCION
                arr_produccion, arr_errores_produccion = read_sheet('Datos Producción', archivo_excel,
                                                                    enterprise_id, "ID. Parcela")

                # Confirmación de importación
                if request.data["confirm_import"] == "true":
                    # ----------- GUARDADO DE PARCELAS
                    logging.debug("GUARDAR PARCELAS")

                    save_parcela(arr_parcelas, request, anio_hoy)

                    # ----------- GUARDADO DE SIEMBRAS
                    logging.debug("GUARDAR SIEMBRAS")
                    save_siembra(arr_siembra, request, anio_hoy)

                    # ----------- GUARDADO DE PRODUCCIONES
                    logging.debug("GUARDAR PRODUCCION")
                    save_produccion(arr_produccion, request, anio_hoy)

            if request.data["confirm_import"] == "false":
                os.remove(archivo_excel)

            return Response({"campanas": arr_parcelas, "erroresParcelas": arr_errores_parcelas, "siembra": arr_siembra,
                             "erroresSiembra": arr_errores_siembra, "produccion": arr_produccion,
                             "erroresProduccion": arr_errores_produccion}, status=status.HTTP_200_OK)
        return Response({"campanas": "No se puede procesar", "Overlaps": "No se puede procesar",
                         "totalparcelas": "No se puede procesar"}, status=status.HTTP_400_BAD_REQUEST)


class Campanaviewset(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Campanas.objects.all()
    serializer_class = CampanasSerializer

    @action(detail=False, methods=['post'])
    def data(self, request, *args, **kwargs):
        finicio = datetime.strptime(request.data['finicio'], '%Y-%m-%d')
        ffin = datetime.strptime(request.data["ffin"], '%Y-%m-%d')
        # Establecemos los dias que hay entre las dos fechas
        arr_fechas = pd.date_range(finicio, ffin).format(formatter=lambda x: x.strftime('%Y'))
        data = {}
        for fecha in arr_fechas:
            queryset = Campanas.objects.filter(anio=int(fecha), parcela_id__in=request.data["parcels"]).all()
            arr_resultados = []
            if len(queryset):
                for result in queryset:
                    arr_resultados.append(CampanasSerializer(result).data)
                data[fecha] = {"resultado": arr_resultados}

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def getplantas(self, request, *args, **kwargs):
        queryset = Campanas.objects.filter(anio__in=request.data["anios"],
                                           parcela_id__in=request.data["parcelas"]).all()
        data = []
        if len(queryset):
            for result in queryset:
                data.append(CampanasSerializer(result).data)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['PUT'])
    def recogida(self, request, *args, **kwargs):
        logging.debug(request.data['fecha'])
        fecha = datetime.strptime(request.data['fecha'], '%Y-%m-%d').date()
        Campanas.objects.filter(parcela_id__in=request.data["parcelas"]).update(fecha_recogida_estimada=fecha)
        return Response({"data": "OK"})


class Siembraviewset(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Siembras.objects.all()
    serializer_class = SiembrasSerializer

    @action(detail=False, methods=['post'])
    def data(self, request, *args, **kwargs):
        finicio = datetime.strptime(request.data["finicio"], '%Y-%m-%d')
        ffin = datetime.strptime(request.data["ffin"], '%Y-%m-%d')
        # Establecemos los dias que hay entre las dos fechas
        arr_fechas = pd.date_range(finicio, ffin).format(formatter=lambda x: x.strftime('%Y'))
        data = {}
        for fecha in arr_fechas:
            queryset = Siembras.objects.filter(anio=int(fecha), parcela_id__in=request.data["parcels"]).all()
            arr_resultados = []
            if len(queryset):
                for result in queryset:
                    arr_resultados.append(SiembrasSerializer(result).data)
                data[fecha] = {"resultado": arr_resultados}

        return Response(data, status=status.HTTP_200_OK)


class Produccionviewset(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Producciones.objects.all()
    serializer_class = ProduccionesSerializer

    @action(detail=False, methods=['post'])
    def data(self, request, *args, **kwargs):
        finicio = datetime.strptime(request.data["finicio"], '%Y-%m-%d')
        ffin = datetime.strptime(request.data["ffin"], '%Y-%m-%d')
        # Establecemos los dias que hay entre las dos fechas
        arr_fechas = pd.date_range(finicio, ffin).format(formatter=lambda x: x.strftime('%Y'))
        data = {}
        for fecha in arr_fechas:
            queryset = Producciones.objects.filter(anio=int(fecha), parcela_id__in=request.data["parcels"]).all()
            arr_resultados = []
            if len(queryset):
                for result in queryset:
                    arr_resultados.append(ProduccionesSerializer(result).data)
                data[fecha] = {"resultado": arr_resultados}

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def getproduccion(self, request, *args, **kwargs):
        queryset = Producciones.objects.filter(anio__in=request.data["anios"],
                                               parcela_id__in=request.data["parcelas"]).all()
        data = []
        if len(queryset):
            for result in queryset:
                data.append(ProduccionesSerializer(result).data)
        return Response(data, status=status.HTTP_200_OK)
