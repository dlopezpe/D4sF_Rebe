# IMPORT LIBRERIAS
from django.conf import settings
from rest_framework import viewsets, generics
from django.core.serializers import serialize

import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
from datetime import datetime
import codecs, json
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import time

from backend.settings.common import url_api_data_sets, url_api_data_source
from utils.D4sfConstants import url_api_instances_const, protocol_url_const, url_api_data_products_647_const, \
    url_api_token_const, url_api_wms_const, url_api_false_layers_const, url_api_crs_const, url_api_time_const
from utils.NpEncoder import NpEncoder
from .jsontoexcel import json2xlsx
import uuid
import urllib.request

from .models import ImagenPro
from modulos.parcelas.models import Parcel
from .serializer import ImagenProSerializer

from rest_framework.response import Response

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import asyncio
from asgiref.sync import sync_to_async, async_to_sync

# CONFIG NDVI
azul_altos = [np.array([255, 255, 51]), np.array([256, 256, 51])]
azul_medios = [np.array([204, 204, 51]), np.array([205, 205, 51])]
azul_bajos = [np.array([102, 102, 0]), np.array([103, 103, 0])]

amarillo_altos = [np.array([51, 255, 255]), np.array([51, 256, 256])]
amarillo_medios = [np.array([51, 204, 204]), np.array([51, 205, 205])]
amarillo_bajos = [np.array([0, 102, 102]), np.array([0, 103, 103])]

rojo_altos = [np.array([0, 0, 254]), np.array([0, 0, 255])]
rojo_medios = [np.array([0, 0, 154]), np.array([0, 0, 155])]
rojo_bajos = [np.array([0, 0, 102]), np.array([0, 0, 103])]

verde_altos = [np.array([51, 255, 51]), np.array([52, 255, 52])]
verde_medios = [np.array([51, 204, 51]), np.array([52, 204, 52])]


# @sync_to_async
def ndviImgT2(serializer, email_user, name_user):
    # await asyncio.sleep(10)
    # RECOGIDA DE DATOS GLOBAL
    urlSent = serializer.validated_data['urlSentinel']
    fechas = serializer.validated_data['fechas']
    parcela = serializer.validated_data['parcela']
    capa = serializer.validated_data['capa']
    # RECOGIDA DE DATOS T1
    # alias = serializer.validated_data['alias'] or ''
    # REGOGIDA DATOS T2
    polygon = serializer.validated_data['polygon']
    fechaElegida = serializer.validated_data['fechaElegida']
    id_parcelas = serializer.validated_data['id_parcelas']

    # VARIABLE DE RESPUESTA
    arrRespuesta = {}

    # CREAMOS LA INSTANCIA DE SENTINEL
    # OBTENEMOS EL TOKEN DE SESSION
    client_id = '33467c23-fada-4405-8a5b-33ee38169273'
    client_secret = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=url_api_token_const, client_id=client_id, client_secret=client_secret)
    hed = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token['access_token']
    }
    # CREAMOS UN BUCLE POR CADA UNO DE LOS POLIGONOS
    for poly in polygon:
        # CREAMOS LA INSTANCIA TEMPORAL
        if capa == 'NDVI':
            layer = {
                'id': 'NDVI',
                'title': 'NDVI (Normalized Difference Vegetation Index)',
                'description': 'Value = colorMap((B08 - B04) / (B08 + B04))',
                'styles': [
                    {
                        'name': 'default',
                        'description': 'Default layer style',
                        'dataProduct': {
                            '@id': url_api_data_products_647_const,
                        }
                    }
                ],
                'orderHint': 0,
                'dataset': {
                    '@id': url_api_data_sets
                },
                'datasetSource': {
                    '@id': url_api_data_source
                },
                'defaultStyleName': 'default',
                'datasourceDefaults': {
                    'upsampling': 'BICUBIC',
                    'mosaickingOrder': 'mostRecent',
                    'temporal': False,
                    'maxCloudCoverage': 20.0,
                    'previewMode': 'PREVIEW',
                    'type': 'S2L1C'
                }
            }
        # CREAMOS LA INSTANCIA CON EL/LOS POLIGONOS
        data = {
            'name': 'Polygons4GraficosType2Tmp',
            'additionalData': {
                'showLogo': False,
                'showWarnings': False,
                'imageQuality': 30,
                'disabled': False
            },
            'areaOfInterest': {
                'type': 'Polygon',
                'coordinates': poly
                , 'crs': {
                    'type': 'name',
                    'properties': {
                        'name': 'urn:ogc:def:crs:EPSG::4326'
                    }
                }
            },
        }
        try:
            reponses = requests.request("POST", url_api_instances_const, headers=hed, data=json.dumps(data))
            responseJson = reponses.json()
            instanceTmp = responseJson['id']
            # CONFIGURAMOS LOS LAYERS
            urlS = url_api_instances_const + instanceTmp + '/layers'
            requests.request("POST", urlS, headers=hed, data=json.dumps(layer))

            time.sleep(3)
            # OBTENEMOS EL URL DEL BOX
            url = urlSent[polygon.index(poly)]
            # BUSCAMOS LA PARCELA PARA EL AREA
            idParcela = id_parcelas[polygon.index(poly)]
            results = Parcel.objects.filter(id=int(idParcela))
            area = 0.0
            for result in results:
                area = result.__dict__['area']
            area = float(area)
            # ESTABLECEMOS EL NOMRBE DE ARCHIVO
            nombreArchivo = str(uuid.uuid1().int) + '.png'
            if fechaElegida:
                urllib.request.urlretrieve(
                    str(url_api_wms_const + instanceTmp + url_api_false_layers_const + capa + url_api_time_const + fechaElegida + url_api_crs_const + url),
                    settings.PARCEL_FOLDER + nombreArchivo)
                # print(url_api_wms_const+instanceTmp+url_api_false_layers_const+capa+url_api_time_const+fechaElegida+url_api_crs_const+url)
            else:
                urllib.request.urlretrieve(
                    str(url_api_wms_const + instanceTmp + url_api_false_layers_const + capa + url_api_crs_const + url),
                    settings.PARCEL_FOLDER + nombreArchivo)
            # LEEMOS LA IMAGEN
            image = cv2.imread(settings.PARCEL_FOLDER + nombreArchivo, cv2.IMREAD_UNCHANGED)
            trans_mask = image[:, :, 3] == 0
            image[trans_mask] = [255, 255, 255, 255]
            img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

            # CALCULOS /*******************************************************************
            """
            MASCARAS AZULES
            """
            # TOTAL
            mask = cv2.inRange(img, azul_bajos[0], azul_altos[0])
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_azules = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # ALTOS
            mask_azul_altos = cv2.inRange(img, azul_altos[0], azul_altos[1])
            unique, counts = np.unique(mask_azul_altos, return_counts=True)
            pixeles_azules_altos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # MEDIOS
            mask_azul_medios = cv2.inRange(img, azul_medios[0], azul_medios[1])
            unique, counts = np.unique(mask_azul_medios, return_counts=True)
            pixeles_azules_medios = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # BAJOS
            mask_azul_bajos = cv2.inRange(img, azul_bajos[0], azul_bajos[1])
            unique, counts = np.unique(mask_azul_bajos, return_counts=True)
            pixeles_azules_bajos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            """
            MASCARA AMARILLOS
            """
            # TOTAL
            mask_amarillo = cv2.inRange(img, amarillo_bajos[0], amarillo_altos[0])
            unique, counts = np.unique(mask_amarillo, return_counts=True)
            pixeles_amarillos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # alto
            mask_amarillo_altos = cv2.inRange(img, amarillo_altos[0], amarillo_altos[1])
            unique, counts = np.unique(mask_amarillo_altos, return_counts=True)
            pixeles_amarillos_altos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # MEDIOS
            mask_amarillo_medios = cv2.inRange(img, amarillo_medios[0], amarillo_medios[1])
            unique, counts = np.unique(mask_amarillo_medios, return_counts=True)
            pixeles_amarillos_medios = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # BAJOS
            mask_amarillo_bajos = cv2.inRange(img, amarillo_bajos[0], amarillo_bajos[1])
            unique, counts = np.unique(mask_amarillo_bajos, return_counts=True)
            pixeles_amarillos_bajos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            """
            MASCARA rojo
            """
            # TOTAL
            mask_rojo = cv2.inRange(img, rojo_bajos[0], rojo_altos[0])
            unique, counts = np.unique(mask_rojo, return_counts=True)
            pixeles_rojos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # alto
            mask_rojo_altos = cv2.inRange(img, rojo_altos[0], rojo_altos[1])
            unique, counts = np.unique(mask_rojo_altos, return_counts=True)
            pixeles_rojos_altos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # MEDIOS
            mask_rojo_medios = cv2.inRange(img, rojo_medios[0], rojo_medios[1])
            unique, counts = np.unique(mask_rojo_medios, return_counts=True)
            pixeles_rojos_medios = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # BAJOS
            mask_rojo_bajos = cv2.inRange(img, rojo_bajos[0], rojo_bajos[1])
            unique, counts = np.unique(mask_rojo_bajos, return_counts=True)
            pixeles_rojos_bajos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            """
            MASCARA VERDES
            """
            # TOTAL
            mask_verde = cv2.inRange(img, verde_medios[0], verde_altos[0])
            unique, counts = np.unique(mask_verde, return_counts=True)
            pixeles_verdes = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # ALTO
            mask_verde_altos = cv2.inRange(img, verde_altos[0], verde_altos[1])
            unique, counts = np.unique(mask_verde_altos, return_counts=True)
            pixeles_verdes_altos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # MEDIOS
            mask_verde_medios = cv2.inRange(img, verde_medios[0], verde_medios[1])
            unique, counts = np.unique(mask_verde_medios, return_counts=True)
            pixeles_verdes_medios = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # FIN CALCULOS /*******************************************************************

            # UNIONES DE MASCARAS
            mask_union = cv2.bitwise_or(mask, mask_amarillo)
            mask_union2 = cv2.bitwise_or(mask_union, mask_rojo)
            mask_union3 = cv2.bitwise_or(mask_union2, mask_verde)
            unique, counts = np.unique(mask_union3, return_counts=True)
            arr_total = np.asarray((unique, counts)).T
            # UNION TOTALES
            total_pixeles = arr_total[1][1]
            total_pixeles_azul = {"total": pixeles_azules,
                                  "porcent": NpEncoder.percentage(pixeles_azules, arr_total[1][1]),
                                  "altos": {"total": pixeles_azules_altos,
                                            "porcent": NpEncoder.percentage(pixeles_azules_altos, total_pixeles),
                                            "area_porcent": (NpEncoder.percentage(pixeles_azules_altos,
                                                                                  total_pixeles) * area / 100)},
                                  "medios": {"total": pixeles_azules_medios,
                                             "porcent": NpEncoder.percentage(pixeles_azules_medios, total_pixeles),
                                             "area_porcent": (NpEncoder.percentage(pixeles_azules_medios,
                                                                                   total_pixeles) * area / 100)},
                                  "bajos": {"total": pixeles_azules_bajos,
                                            "porcent": NpEncoder.percentage(pixeles_azules_bajos, total_pixeles),
                                            "area_porcent": (NpEncoder.percentage(pixeles_azules_bajos,
                                                                                  total_pixeles) * area / 100)}}
            total_pixeles_amarillo = {"total": pixeles_amarillos,
                                      "porcent": NpEncoder.percentage(pixeles_amarillos, arr_total[1][1]),
                                      "altos": {"total": pixeles_amarillos_altos,
                                                "porcent": NpEncoder.percentage(pixeles_amarillos_altos, total_pixeles),
                                                "area_porcent": (NpEncoder.percentage(pixeles_amarillos_altos,
                                                                                      total_pixeles) * area / 100)},
                                      "medios": {"total": pixeles_amarillos_medios,
                                                 "porcent": NpEncoder.percentage(pixeles_amarillos_medios,
                                                                                 total_pixeles), "area_porcent": (
                                                      NpEncoder.percentage(pixeles_amarillos_medios,
                                                                           total_pixeles) * area / 100)},
                                      "bajos": {"total": pixeles_amarillos_bajos,
                                                "porcent": NpEncoder.percentage(pixeles_amarillos_bajos, total_pixeles),
                                                "area_porcent": (NpEncoder.percentage(pixeles_amarillos_bajos,
                                                                                      total_pixeles) * area / 100)}}
            total_pixeles_rojo = {"total": pixeles_rojos,
                                  "porcent": NpEncoder.percentage(pixeles_rojos, arr_total[1][1]),
                                  "altos": {"total": pixeles_rojos_altos,
                                            "porcent": NpEncoder.percentage(pixeles_rojos_altos, total_pixeles),
                                            "area_porcent": (NpEncoder.percentage(pixeles_rojos_altos,
                                                                                  total_pixeles) * area / 100)},
                                  "medios": {"total": pixeles_rojos_medios,
                                             "porcent": NpEncoder.percentage(pixeles_rojos_medios, total_pixeles),
                                             "area_porcent": (NpEncoder.percentage(pixeles_rojos_medios,
                                                                                   total_pixeles) * area / 100)},
                                  "bajos": {"total": pixeles_rojos_bajos,
                                            "porcent": NpEncoder.percentage(pixeles_rojos_bajos, total_pixeles),
                                            "area_porcent": (NpEncoder.percentage(pixeles_rojos_bajos,
                                                                                  total_pixeles) * area / 100)}}
            total_pixeles_verde = {"total": pixeles_verdes,
                                   "porcent": NpEncoder.percentage(pixeles_verdes, arr_total[1][1]),
                                   "altos": {"total": pixeles_verdes_altos,
                                             "porcent": NpEncoder.percentage(pixeles_verdes_altos, total_pixeles),
                                             "area_porcent": (NpEncoder.percentage(pixeles_verdes_altos,
                                                                                   total_pixeles) * area / 100)},
                                   "medios": {"total": pixeles_verdes_altos,
                                              "porcent": NpEncoder.percentage(pixeles_verdes_medios, total_pixeles),
                                              "area_porcent": (NpEncoder.percentage(pixeles_verdes_medios,
                                                                                    total_pixeles) * area / 100)}}
            # ESTABLECEMOS EL RESULTADO
            arrResult = {urlSent.index(url): {"img": nombreArchivo, "totalPixeles": arr_total[1][1],
                                              "fecha": fechas[urlSent.index(url)], "area": area,
                                              "azules": total_pixeles_azul, "amarillos": total_pixeles_amarillo,
                                              "rojos": total_pixeles_rojo, "verdes": total_pixeles_verde}}
            arrRespuesta.update(arrResult)
        except Exception as Error:
            # CONFIG EMAIL
            site_shortcut_name = 'Data4SmartFarming'
            context = {
                'site_name': site_shortcut_name,
                'nombre_informe': parcela,
                'nombre_user': name_user
            }
            # ENVIO CORREO KO
            title = "=?utf-8?Q?=E2=9D=97_Error_al_generar_el_Informe?="
            email_html_message_enterprise = render_to_string('Informe_generado_error.html', context)
            # ENVIAMOS EL MAIL
            msg = EmailMultiAlternatives(
                # title:
                title,
                # message:
                email_html_message_enterprise,
                # from:
                "D4SmartFarming <soporte@d4smartfarming.com>",
                # to:
                [email_user],  # ['soporte@d4smartfarming.com']
                # BCC
                ['backups@smartbits.es']
            )
            msg.attach_alternative(email_html_message_enterprise, "text/html")
            msg.send()
            exit()
    # HACEMOS EL FICHERO JSON
    app_json = json.dumps(arrRespuesta, cls=NpEncoder)
    eventid = datetime.now().strftime('%Y%m-%d%H-%M%S')
    nombreJson = str(uuid.uuid1().int) + '.json'
    file = open(settings.PARCEL_FOLDER + nombreJson, 'w')
    file.write(app_json)
    file.close()
    # HACEMOS EL FICHERO xls
    nombreXlsx = str(uuid.uuid1().int) + '.xlsx'
    json2xlsx(nombreJson, nombreXlsx, capa)
    # AJUSTE DE NOMBRE
    if parcela == str(0):
        parcela = 'Gráfico Tipo 2'
    # AJUSTE DE FECHA
    finicioFin = fechaElegida
    if not fechaElegida:
        finicioFin = datetime.now().strftime('%Y-%m-%d')
    # CONFIG EMAIL
    site_shortcut_name = 'Data4SmartFarming'
    context = {
        'site_name': site_shortcut_name,
        'nombre_informe': parcela,
        'nombre_user': name_user
    }
    ## GUARDADO
    if serializer.save(parcela=parcela, urlSentinel=protocol_url_const, imagen=nombreJson, xlsxFile=nombreXlsx,
                       finifin=finicioFin, tipo=2, polygon=[], fechas=datetime.now().strftime('%Y-%m-%d - %H:%M:%S'),
                       capa=capa, fechaElegida=fechaElegida):
        # ENVIO DE CORREO OK
        title = "=?utf-8?Q?=F0=9F=93=8B_Informe_generado_Correctamente?="
        email_html_message_enterprise = render_to_string('Informe_generado_correctamente.html', context)
    else:
        # ENVIO CORREO KO
        title = "=?utf-8?Q?=E2=9D=97_Error_al_generar_el_Informe?="
        email_html_message_enterprise = render_to_string('Informe_generado_error.html', context)
    # ENVIAMOS EL MAIL
    msg = EmailMultiAlternatives(
        # title:
        title,
        # message:
        email_html_message_enterprise,
        # from:
        "D4SmartFarming <soporte@d4smartfarming.com>",
        # to:
        [email_user],  # ['soporte@d4smartfarming.com']
        # BCC
        ['backups@smartbits.es']
    )
    msg.attach_alternative(email_html_message_enterprise, "text/html")
    msg.send()
    # ELIMINACION DE LA INSTANCIA TEMPORAL
    urlS = url_api_instances_const + instanceTmp
    requests.request("DELETE", urlS, headers=hed)

    # return Response(arrRespuesta)


def ndviImgT1(serializer, email_user, name_user):
    # RECOGIDA DE DATOS GLOBAL
    urlSent = serializer.validated_data['urlSentinel']
    fechas = serializer.validated_data['fechas']
    parcela = serializer.validated_data['parcela']
    capa = serializer.validated_data['capa']
    # RECOGIDA DE DATOS T1
    alias = serializer.validated_data['alias'] or ''
    # REGOGIDA DATOS T2
    polygon = serializer.validated_data['polygon']

    # VARIABLE DE RESPUESTA
    arrRespuesta = {}

    # CREAMOS LA INSTANCIA DE SENTINEL
    # OBTENEMOS EL TOKEN DE SESSION
    client_id = '33467c23-fada-4405-8a5b-33ee38169273'
    client_secret = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=url_api_token_const, client_id=client_id, client_secret=client_secret)
    hed = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token['access_token']
    }

    # CREAMOS LA INSTANCIA TEMPORAL
    if capa == 'NDVI':
        layer = {
            'id': 'NDVI',
            'title': 'NDVI (Normalized Difference Vegetation Index)',
            'description': 'Value = colorMap((B08 - B04) / (B08 + B04))',
            'styles': [
                {
                    'name': 'default',
                    'description': 'Default layer style',
                    'dataProduct': {
                        '@id': url_api_data_products_647_const,
                    }
                }
            ],
            'orderHint': 0,
            'dataset': {
                '@id': url_api_data_sets
            },
            'datasetSource': {
                '@id': url_api_data_source
            },
            'defaultStyleName': 'default',
            'datasourceDefaults': {
                'upsampling': 'BICUBIC',
                'mosaickingOrder': 'mostRecent',
                'temporal': False,
                'maxCloudCoverage': 20.0,
                'previewMode': 'PREVIEW',
                'type': 'S2L1C'
            }
        }
    # CREAMOS LA INSTANCIA CON EL/LOS POLIGONOS
    data = {
        'name': 'Polygons4GraficosType1Tmp',
        'additionalData': {
            'showLogo': False,
            'showWarnings': False,
            'imageQuality': 30,
            'disabled': False
        },
        'areaOfInterest': {
            'type': 'Polygon',
            'coordinates': polygon
            , 'crs': {
                'type': 'name',
                'properties': {
                    'name': 'urn:ogc:def:crs:EPSG::4326'
                }
            }
        },
    }

    try:
        reponses = requests.request("POST", url_api_instances_const, headers=hed, data=json.dumps(data))
        responseJson = reponses.json()
        instanceTmp = responseJson['id']
        # CONFIGURAMOS LOS LAYERS
        urlS = url_api_instances_const + instanceTmp + '/layers'
        requests.request("POST", urlS, headers=hed, data=json.dumps(layer))

        time.sleep(3)
        # OBTENEMOS EL URL DEL BOX
        # url = urlSent[polygon]
        # BUSCAMOS LA PARCELA PARA EL AREA
        results = Parcel.objects.filter(id=int(parcela))
        area = 0.0
        for result in results:
            area = result.__dict__['area']
        area = float(area)

        for fecha in fechas:
            nombreArchivo = str(uuid.uuid1().int) + '.png'
            urllib.request.urlretrieve(
                str(url_api_wms_const + instanceTmp + url_api_false_layers_const + capa + '&TIME=' + fecha + url_api_crs_const +
                    urlSent[0]), settings.PARCEL_FOLDER + nombreArchivo)
            # LEEMOS LA IMAGEN
            image = cv2.imread(settings.PARCEL_FOLDER + nombreArchivo, cv2.IMREAD_UNCHANGED)
            trans_mask = image[:, :, 3] == 0
            image[trans_mask] = [255, 255, 255, 255]
            img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

            # CALCULOS /*******************************************************************
            """
            MASCARAS AZULES
            """
            # TOTAL
            mask = cv2.inRange(img, azul_bajos[0], azul_altos[0])
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_azules = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # ALTOS
            mask_azul_altos = cv2.inRange(img, azul_altos[0], azul_altos[1])
            unique, counts = np.unique(mask_azul_altos, return_counts=True)
            pixeles_azules_altos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # MEDIOS
            mask_azul_medios = cv2.inRange(img, azul_medios[0], azul_medios[1])
            unique, counts = np.unique(mask_azul_medios, return_counts=True)
            pixeles_azules_medios = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # BAJOS
            mask_azul_bajos = cv2.inRange(img, azul_bajos[0], azul_bajos[1])
            unique, counts = np.unique(mask_azul_bajos, return_counts=True)
            pixeles_azules_bajos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            """
            MASCARA AMARILLOS
            """
            # TOTAL
            mask_amarillo = cv2.inRange(img, amarillo_bajos[0], amarillo_altos[0])
            unique, counts = np.unique(mask_amarillo, return_counts=True)
            pixeles_amarillos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # alto
            mask_amarillo_altos = cv2.inRange(img, amarillo_altos[0], amarillo_altos[1])
            unique, counts = np.unique(mask_amarillo_altos, return_counts=True)
            pixeles_amarillos_altos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # MEDIOS
            mask_amarillo_medios = cv2.inRange(img, amarillo_medios[0], amarillo_medios[1])
            unique, counts = np.unique(mask_amarillo_medios, return_counts=True)
            pixeles_amarillos_medios = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # BAJOS
            mask_amarillo_bajos = cv2.inRange(img, amarillo_bajos[0], amarillo_bajos[1])
            unique, counts = np.unique(mask_amarillo_bajos, return_counts=True)
            pixeles_amarillos_bajos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            """
            MASCARA rojo
            """
            # TOTAL
            mask_rojo = cv2.inRange(img, rojo_bajos[0], rojo_altos[0])
            unique, counts = np.unique(mask_rojo, return_counts=True)
            pixeles_rojos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # alto
            mask_rojo_altos = cv2.inRange(img, rojo_altos[0], rojo_altos[1])
            unique, counts = np.unique(mask_rojo_altos, return_counts=True)
            pixeles_rojos_altos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # MEDIOS
            mask_rojo_medios = cv2.inRange(img, rojo_medios[0], rojo_medios[1])
            unique, counts = np.unique(mask_rojo_medios, return_counts=True)
            pixeles_rojos_medios = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # BAJOS
            mask_rojo_bajos = cv2.inRange(img, rojo_bajos[0], rojo_bajos[1])
            unique, counts = np.unique(mask_rojo_bajos, return_counts=True)
            pixeles_rojos_bajos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            """
            MASCARA VERDES
            """
            # TOTAL
            mask_verde = cv2.inRange(img, verde_medios[0], verde_altos[0])
            unique, counts = np.unique(mask_verde, return_counts=True)
            pixeles_verdes = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # ALTO
            mask_verde_altos = cv2.inRange(img, verde_altos[0], verde_altos[1])
            unique, counts = np.unique(mask_verde_altos, return_counts=True)
            pixeles_verdes_altos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # MEDIOS
            mask_verde_medios = cv2.inRange(img, verde_medios[0], verde_medios[1])
            unique, counts = np.unique(mask_verde_medios, return_counts=True)
            pixeles_verdes_medios = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
            # FIN CALCULOS /*******************************************************************

            # UNIONES DE MASCARAS
            mask_union = cv2.bitwise_or(mask, mask_amarillo)
            mask_union2 = cv2.bitwise_or(mask_union, mask_rojo)
            mask_union3 = cv2.bitwise_or(mask_union2, mask_verde)
            unique, counts = np.unique(mask_union3, return_counts=True)
            arr_total = np.asarray((unique, counts)).T
            # UNION TOTALES
            total_pixeles = arr_total[1][1]
            total_pixeles_azul = {"total": pixeles_azules,
                                  "porcent": NpEncoder.percentage(pixeles_azules, arr_total[1][1]),
                                  "altos": {"total": pixeles_azules_altos,
                                            "porcent": NpEncoder.percentage(pixeles_azules_altos, total_pixeles),
                                            "area_porcent": (NpEncoder.percentage(pixeles_azules_altos,
                                                                                  total_pixeles) * area / 100)},
                                  "medios": {"total": pixeles_azules_medios,
                                             "porcent": NpEncoder.percentage(pixeles_azules_medios, total_pixeles),
                                             "area_porcent": (NpEncoder.percentage(pixeles_azules_medios,
                                                                                   total_pixeles) * area / 100)},
                                  "bajos": {"total": pixeles_azules_bajos,
                                            "porcent": NpEncoder.percentage(pixeles_azules_bajos, total_pixeles),
                                            "area_porcent": (NpEncoder.percentage(pixeles_azules_bajos,
                                                                                  total_pixeles) * area / 100)}}
            total_pixeles_amarillo = {"total": pixeles_amarillos,
                                      "porcent": NpEncoder.percentage(pixeles_amarillos, arr_total[1][1]),
                                      "altos": {"total": pixeles_amarillos_altos,
                                                "porcent": NpEncoder.percentage(pixeles_amarillos_altos, total_pixeles),
                                                "area_porcent": (NpEncoder.percentage(pixeles_amarillos_altos,
                                                                                      total_pixeles) * area / 100)},
                                      "medios": {"total": pixeles_amarillos_medios,
                                                 "porcent": NpEncoder.percentage(pixeles_amarillos_medios,
                                                                                 total_pixeles), "area_porcent": (
                                                      NpEncoder.percentage(pixeles_amarillos_medios,
                                                                           total_pixeles) * area / 100)},
                                      "bajos": {"total": pixeles_amarillos_bajos,
                                                "porcent": NpEncoder.percentage(pixeles_amarillos_bajos, total_pixeles),
                                                "area_porcent": (NpEncoder.percentage(pixeles_amarillos_bajos,
                                                                                      total_pixeles) * area / 100)}}
            total_pixeles_rojo = {"total": pixeles_rojos,
                                  "porcent": NpEncoder.percentage(pixeles_rojos, arr_total[1][1]),
                                  "altos": {"total": pixeles_rojos_altos,
                                            "porcent": NpEncoder.percentage(pixeles_rojos_altos, total_pixeles),
                                            "area_porcent": (NpEncoder.percentage(pixeles_rojos_altos,
                                                                                  total_pixeles) * area / 100)},
                                  "medios": {"total": pixeles_rojos_medios,
                                             "porcent": NpEncoder.percentage(pixeles_rojos_medios, total_pixeles),
                                             "area_porcent": (NpEncoder.percentage(pixeles_rojos_medios,
                                                                                   total_pixeles) * area / 100)},
                                  "bajos": {"total": pixeles_rojos_bajos,
                                            "porcent": NpEncoder.percentage(pixeles_rojos_bajos, total_pixeles),
                                            "area_porcent": (NpEncoder.percentage(pixeles_rojos_bajos,
                                                                                  total_pixeles) * area / 100)}}
            total_pixeles_verde = {"total": pixeles_verdes,
                                   "porcent": NpEncoder.percentage(pixeles_verdes, arr_total[1][1]),
                                   "altos": {"total": pixeles_verdes_altos,
                                             "porcent": NpEncoder.percentage(pixeles_verdes_altos, total_pixeles),
                                             "area_porcent": (NpEncoder.percentage(pixeles_verdes_altos,
                                                                                   total_pixeles) * area / 100)},
                                   "medios": {"total": pixeles_verdes_altos,
                                              "porcent": NpEncoder.percentage(pixeles_verdes_medios, total_pixeles),
                                              "area_porcent": (NpEncoder.percentage(pixeles_verdes_medios,
                                                                                    total_pixeles) * area / 100)}}
            # ESTABLECEMOS EL RESULTADO
            arrResult = {fechas.index(fecha): {"img": nombreArchivo, "totalPixeles": arr_total[1][1], "fecha": fecha,
                                               "area": area, "azules": total_pixeles_azul,
                                               "amarillos": total_pixeles_amarillo, "rojos": total_pixeles_rojo,
                                               "verdes": total_pixeles_verde}}
            arrRespuesta.update(arrResult)
    except Exception as Error:
        # CONFIG EMAIL
        site_shortcut_name = 'Data4SmartFarming'
        context = {
            'site_name': site_shortcut_name,
            'nombre_informe': parcela,
            'nombre_user': name_user,
            'error': ''
        }
        # ENVIO CORREO KO
        title = "=?utf-8?Q?=E2=9D=97_Error_al_generar_el_Informe?="
        email_html_message_enterprise = render_to_string('Informe_generado_error.html', context)
        # ENVIAMOS EL MAIL
        msg = EmailMultiAlternatives(
            # title:
            title,
            # message:
            email_html_message_enterprise,
            # from:
            "D4SmartFarming <soporte@d4smartfarming.com>",
            # to:
            [email_user],  # ['soporte@d4smartfarming.com']
            # BCC
            ['backups@smartbits.es']
        )
        msg.attach_alternative(email_html_message_enterprise, "text/html")
        msg.send()

        # CONFIG EMAIL
        site_shortcut_name = 'Data4SmartFarming'
        context = {
            'site_name': site_shortcut_name,
            'nombre_informe': parcela,
            'nombre_user': name_user,
            'error': Error
        }
        # ENVIO CORREO KO
        title = "=?utf-8?Q?=E2=9D=97_Error_al_generar_el_Informe?="
        email_html_message_enterprise = render_to_string('Informe_generado_error.html', context)
        # ENVIAMOS EL MAIL
        msg = EmailMultiAlternatives(
            # title:
            title,
            # message:
            email_html_message_enterprise,
            # from:
            "D4SmartFarming <soporte@d4smartfarming.com>",
            # to:
            ['soporte@d4smartfarming.com'],
            # BCC
            ['backups@smartbits.es']
        )
        msg.attach_alternative(email_html_message_enterprise, "text/html")
        msg.send()
        exit()
    # HACEMOS EL FICHERO JSON
    app_json = json.dumps(arrRespuesta, cls=NpEncoder)
    eventid = datetime.now().strftime('%Y%m-%d%H-%M%S')
    nombreJson = str(uuid.uuid1().int) + '.json'
    file = open(settings.PARCEL_FOLDER + nombreJson, 'w')
    file.write(app_json)
    file.close()
    # HACEMOS EL FICHERO xls
    nombreXlsx = str(uuid.uuid1().int) + '.xlsx'
    json2xlsx(nombreJson, nombreXlsx, capa)
    # CONFIG EMAIL
    site_shortcut_name = 'Data4SmartFarming'
    context = {
        'site_name': site_shortcut_name,
        'nombre_informe': alias,
        'nombre_user': name_user
    }
    ## GUARDADO
    if serializer.save(parcela=parcela, urlSentinel=protocol_url_const, imagen=nombreJson, xlsxFile=nombreXlsx,
                       finifin=str(fechas[0]) + ' - ' + str(fechas[-1]), tipo=1, polygon=[],
                       fechas=datetime.now().strftime('%Y-%m-%d - %H:%M:%S'), capa=capa, alias=alias):
        # ENVIO DE CORREO OK
        title = "=?utf-8?Q?=F0=9F=93=8B_Informe_generado_Correctamente?="
        email_html_message_enterprise = render_to_string('Informe_generado_correctamente.html', context)
    else:
        # ENVIO CORREO KO
        title = "=?utf-8?Q?=E2=9D=97_Error_al_generar_el_Informe?="
        email_html_message_enterprise = render_to_string('Informe_generado_error.html', context)
    # ENVIAMOS EL MAIL
    msg = EmailMultiAlternatives(
        # title:
        title,
        # message:
        email_html_message_enterprise,
        # from:
        "D4SmartFarming <soporte@d4smartfarming.com>",
        # to:
        [email_user],  # ['soporte@d4smartfarming.com']
        # BCC
        ['backups@smartbits.es']
    )
    msg.attach_alternative(email_html_message_enterprise, "text/html")
    msg.send()
    # ELIMINACION DE LA INSTANCIA TEMPORAL
    urlS = url_api_instances_const + instanceTmp
    requests.request("DELETE", urlS, headers=hed)
