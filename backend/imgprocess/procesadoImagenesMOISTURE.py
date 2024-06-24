#IMPORT LIBRERIAS
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
from .jsontoexcel import json2xlsx
import uuid
import urllib.request


from .models import ImagenPro
from parcelas.models import Parcel
from .serializer import ImagenProSerializer


from rest_framework.response import Response

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import asyncio
from asgiref.sync import sync_to_async, async_to_sync

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
#FUNCIONES
def getPixeles(arr_mask):
    if len(arr_mask) == 2:
        return arr_mask[1][1]
    else:
        return 0
def percentage(part, whole):
    if part > 0:
        return float(round(100 * float(part)/float(whole), 2))
    else:
        return 0
def moistureImgT2(serializer, email_user, name_user):
    #await asyncio.sleep(10)
    # RECOGIDA DE DATOS GLOBAL
    urlSent = serializer.validated_data['urlSentinel']
    fechas = serializer.validated_data['fechas']
    parcela = serializer.validated_data['parcela']
    capa = serializer.validated_data['capa']
    # RECOGIDA DE DATOS T1
    #alias = serializer.validated_data['alias'] or ''
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
    token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token', client_id=client_id, client_secret=client_secret)
    hed = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer '+token['access_token']
    }
    # CREAMOS UN BUCLE POR CADA UNO DE LOS POLIGONOS
    for poly in polygon:
        # CREAMOS LA INSTANCIA TEMPORAL
        layer = {
            'id': 'MOISTURE_INDEX',
            'title': 'Moisture Index',
            'description': 'Based on combination of bands (B8A - B11)/(B8A + B11)',
            'styles': [
                {
                    'name': 'default',
                    'dataProduct': {
                        '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/1242',
                        'id': 1242,
                        'name': 'MOISTURE_INDEX.MOISTURE',
                        'description': 'Moisture Index - Moisture color gradient visualization',
                        'evalScript': '//VERSION=3\n\nlet index = (B8A - B11)/(B8A + B11);\n\nlet val = colorBlend(index, [-0.8, -0.24, -0.032, 0.032, 0.24, 0.8], [[0.5,0,0], [1,0,0], [1,1,0], [0,1,1], [0,0,1], [0,0,0.5]]);\nval.push(dataMask);\nreturn val;\n\n',
                        'dataset': {
                            '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C'
                        },
                        'baseProduct': 'MOISTURE_INDEX',
                        'visualization': 'MOISTURE',
                        'scriptVersion': 3,
                        'listed': True,
                        'additionalData': {
                            'preV3EquivalentId': 425
                        }
                    }
                }
            ],
            'orderHint': 6,
            'dataset': {
                '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C'
            },
            'datasetSource': {
                '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1'
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
                ,'crs': {
                    'type':'name',
                    'properties': {
                        'name': 'urn:ogc:def:crs:EPSG::4326'
                    }
                }
            },
        }
        try:
            urlS = 'https://services.sentinel-hub.com/configuration/v1/wms/instances'
            reponses = requests.request("POST", urlS, headers=hed, data = json.dumps(data))
            responseJson = reponses.json()
            instanceTmp = responseJson['id']
            # CONFIGURAMOS LOS LAYERS
            urlS = 'https://services.sentinel-hub.com/configuration/v1/wms/instances/'+instanceTmp+'/layers'
            requests.request("POST", urlS, headers=hed, data = json.dumps(layer))
        

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
            nombreArchivo = str(uuid.uuid1().int)+'.png'
            if fechaElegida:
                urllib.request.urlretrieve(str('https://services.sentinel-hub.com/ogc/wms/'+instanceTmp+'?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=false&LAYERS='+capa+'&TIME=2019-01-01%2F'+fechaElegida+'&CRS=EPSG%3A4326&WIDTH=2248&HEIGHT=1449&MAXCC=100&BBOX='+url), settings.PARCEL_FOLDER+nombreArchivo)
                #print('https://services.sentinel-hub.com/ogc/wms/'+instanceTmp+'?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=false&LAYERS='+capa+'&TIME=2019-01-01%2F'+fechaElegida+'&CRS=EPSG%3A4326&WIDTH=2248&HEIGHT=1449&MAXCC=100&BBOX='+url)
            else:
                urllib.request.urlretrieve(str('https://services.sentinel-hub.com/ogc/wms/'+instanceTmp+'?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=false&LAYERS='+capa+'&CRS=EPSG%3A4326&WIDTH=2248&HEIGHT=1449&MAXCC=100&BBOX='+url), settings.PARCEL_FOLDER+nombreArchivo)
            # LEEMOS LA IMAGEN
            image = cv2.imread(settings.PARCEL_FOLDER+nombreArchivo, cv2.IMREAD_UNCHANGED)
            trans_mask = image[:,:,3] == 0
            image[trans_mask] = [255, 255, 255, 255]
            img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

            # CALCULOS /*******************************************************************
            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            #ROJO/NARANJAS
            ligth_green = (1, 255, 0)
            dark_green = (25, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_naranjas = getPixeles(np.asarray((unique, counts)).T)
            #AMARILLOS
            ligth_green = (26, 255, 0)
            dark_green = (50, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_amarillos = getPixeles(np.asarray((unique, counts)).T)
            #VERDES
            ligth_green = (31, 0, 0)
            dark_green = (50, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_verdes = getPixeles(np.asarray((unique, counts)).T)
            #AZULES CLARITOS
            ligth_green = (51, 255, 0)
            dark_green = (100, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_a_claro = getPixeles(np.asarray((unique, counts)).T)
            #AZULES MEDIOS
            ligth_green = (101, 255, 0)
            dark_green = (115, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_a_medio = getPixeles(np.asarray((unique, counts)).T)
            #AZULES OSCURO
            ligth_green = (116, 255, 0)
            dark_green = (200, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_a_oscuro = getPixeles(np.asarray((unique, counts)).T)

            # UNION TOTALES
            totalPixDetectados = sum([pixeles_naranjas, pixeles_amarillos, pixeles_verdes, pixeles_a_claro, pixeles_a_medio, pixeles_a_oscuro])
            total_pixeles_naranja = {"total": pixeles_naranjas, "porcent": percentage(pixeles_naranjas, totalPixDetectados), "area_porcent": (percentage(pixeles_naranjas, totalPixDetectados)*area/100)}
            total_pixeles_amarillo = {"total": pixeles_amarillos, "porcent": percentage(pixeles_amarillos, totalPixDetectados), "area_porcent": (percentage(pixeles_amarillos, totalPixDetectados)*area/100)}
            total_pixeles_verde = {"total": pixeles_verdes, "porcent": percentage(pixeles_verdes, totalPixDetectados), "area_porcent": (percentage(pixeles_verdes, totalPixDetectados)*area/100)}
            total_pixeles_a_claro = {"total": pixeles_a_claro, "porcent": percentage(pixeles_a_claro, totalPixDetectados), "area_porcent": (percentage(pixeles_a_claro, totalPixDetectados)*area/100)}
            total_pixeles_a_medio = {"total": pixeles_a_medio, "porcent": percentage(pixeles_a_medio, totalPixDetectados), "area_porcent": (percentage(pixeles_a_medio, totalPixDetectados)*area/100)}
            total_pixeles_a_oscuro = {"total": pixeles_a_oscuro, "porcent": percentage(pixeles_a_oscuro, totalPixDetectados), "area_porcent": (percentage(pixeles_a_oscuro, totalPixDetectados)*area/100)}
            # ESTABLECEMOS EL RESULTADO
            arrResult = {urlSent.index(url):{"img": nombreArchivo, "totalPixeles": totalPixDetectados, "fecha": fechas[urlSent.index(url)], "area": area, "naranja": total_pixeles_naranja, "amarillo": total_pixeles_amarillo, "verdes": total_pixeles_verde, "azul_claro": total_pixeles_a_claro, "azul_medio": total_pixeles_a_medio, "azul_oscuro": total_pixeles_a_oscuro}}
            arrRespuesta.update(arrResult)
        except Exception as Error:
            #CONFIG EMAIL
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
                [email_user],#['soporte@d4smartfarming.com']
                # BCC
                ['backups@smartbits.es']
            )
            msg.attach_alternative(email_html_message_enterprise, "text/html")
            msg.send()
            exit()
    # HACEMOS EL FICHERO JSON
    app_json = json.dumps(arrRespuesta, cls=NpEncoder)
    eventid = datetime.now().strftime('%Y%m-%d%H-%M%S')
    nombreJson = str(uuid.uuid1().int)+'.json'
    file = open(settings.PARCEL_FOLDER+nombreJson, 'w')
    file.write(app_json)
    file.close()
    # HACEMOS EL FICHERO xls
    nombreXlsx = str(uuid.uuid1().int)+'.xlsx'
    json2xlsx(nombreJson, nombreXlsx, capa)
    
    # AJUSTE DE NOMBRE
    if parcela == str(0):
        parcela = 'Gráfico Tipo 2'
    #AJUSTE DE FECHA
    finicioFin = fechaElegida
    if not fechaElegida:
        finicioFin = datetime.now().strftime('%Y-%m-%d')
    #CONFIG EMAIL
    site_shortcut_name = 'Data4SmartFarming'
    context = {
        'site_name': site_shortcut_name,
        'nombre_informe': parcela,
        'nombre_user': name_user
    }
    ## GUARDADO
    if serializer.save(parcela=parcela, urlSentinel="https://", imagen=nombreJson, xlsxFile=nombreXlsx, finifin=finicioFin, tipo=2, polygon=[], fechas=datetime.now().strftime('%Y-%m-%d - %H:%M:%S'), capa=capa, fechaElegida=fechaElegida):
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
        [email_user],#['soporte@d4smartfarming.com']
        # BCC
        ['backups@smartbits.es']
    )
    msg.attach_alternative(email_html_message_enterprise, "text/html")
    msg.send()
    # ELIMINACION DE LA INSTANCIA TEMPORAL
    urlS = 'https://services.sentinel-hub.com/configuration/v1/wms/instances/'+instanceTmp
    requests.request("DELETE", urlS, headers=hed)
    
    #return Response(arrRespuesta)


def moistureImgT1(serializer, email_user, name_user):
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
    token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token', client_id=client_id, client_secret=client_secret)
    hed = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer '+token['access_token']
    }

    # CREAMOS LA INSTANCIA TEMPORAL
    layer = {
        'id': 'MOISTURE_INDEX',
        'title': 'Moisture Index',
        'description': 'Based on combination of bands (B8A - B11)/(B8A + B11)',
        'styles': [
            {
                'name': 'default',
                'dataProduct': {
                    '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/dataproducts/1242',
                    'id': 1242,
                    'name': 'MOISTURE_INDEX.MOISTURE',
                    'description': 'Moisture Index - Moisture color gradient visualization',
                    'evalScript': '//VERSION=3\n\nlet index = (B8A - B11)/(B8A + B11);\n\nlet val = colorBlend(index, [-0.8, -0.24, -0.032, 0.032, 0.24, 0.8], [[0.5,0,0], [1,0,0], [1,1,0], [0,1,1], [0,0,1], [0,0,0.5]]);\nval.push(dataMask);\nreturn val;\n\n',
                    'dataset': {
                        '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C'
                    },
                    'baseProduct': 'MOISTURE_INDEX',
                    'visualization': 'MOISTURE',
                    'scriptVersion': 3,
                    'listed': True,
                    'additionalData': {
                        'preV3EquivalentId': 425
                    }
                }
            }
        ],
        'orderHint': 6,
        'dataset': {
            '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C'
        },
        'datasetSource': {
            '@id': 'https://services.sentinel-hub.com/configuration/v1/datasets/S2L1C/sources/1'
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
            ,'crs': {
                'type':'name',
                'properties': {
                    'name': 'urn:ogc:def:crs:EPSG::4326'
                }
            }
        },
    }

    try:
        urlS = 'https://services.sentinel-hub.com/configuration/v1/wms/instances'
        reponses = requests.request("POST", urlS, headers=hed, data = json.dumps(data))
        responseJson = reponses.json()
        instanceTmp = responseJson['id']
        # CONFIGURAMOS LOS LAYERS
        urlS = 'https://services.sentinel-hub.com/configuration/v1/wms/instances/'+instanceTmp+'/layers'
        requests.request("POST", urlS, headers=hed, data = json.dumps(layer))

        time.sleep(3)
        # OBTENEMOS EL URL DEL BOX
        #url = urlSent[polygon]
        # BUSCAMOS LA PARCELA PARA EL AREA
        results = Parcel.objects.filter(id=int(parcela))
        area = 0.0
        for result in results:
            area = result.__dict__['area']
        area = float(area)

        for fecha in fechas:
            nombreArchivo = str(uuid.uuid1().int)+'.png'
            urllib.request.urlretrieve(str('https://services.sentinel-hub.com/ogc/wms/'+instanceTmp+'?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=false&LAYERS='+capa+'&TIME='+fecha+'&CRS=EPSG%3A4326&WIDTH=2248&HEIGHT=1449&MAXCC=100&BBOX='+urlSent[0]), settings.PARCEL_FOLDER+nombreArchivo)
            # LEEMOS LA IMAGEN
            image = cv2.imread(settings.PARCEL_FOLDER+nombreArchivo, cv2.IMREAD_UNCHANGED)
            trans_mask = image[:,:,3] == 0
            image[trans_mask] = [255, 255, 255, 255]
            img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

            # CALCULOS /*******************************************************************
            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            #ROJO/NARANJAS
            ligth_green = (1, 255, 0)
            dark_green = (25, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_naranjas = getPixeles(np.asarray((unique, counts)).T)
            #AMARILLOS
            ligth_green = (26, 255, 0)
            dark_green = (50, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_amarillos = getPixeles(np.asarray((unique, counts)).T)
            #VERDES
            ligth_green = (31, 0, 0)
            dark_green = (50, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_verdes = getPixeles(np.asarray((unique, counts)).T)
            #AZULES CLARITOS
            ligth_green = (51, 255, 0)
            dark_green = (100, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_a_claro = getPixeles(np.asarray((unique, counts)).T)
            #AZULES MEDIOS
            ligth_green = (101, 255, 0)
            dark_green = (115, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_a_medio = getPixeles(np.asarray((unique, counts)).T)
            #AZULES OSCURO
            ligth_green = (116, 255, 0)
            dark_green = (200, 255, 255)
            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
            unique, counts = np.unique(mask, return_counts=True)
            pixeles_a_oscuro = getPixeles(np.asarray((unique, counts)).T)

            totalPixDetectados = sum([pixeles_naranjas, pixeles_amarillos, pixeles_verdes, pixeles_a_claro, pixeles_a_medio, pixeles_a_oscuro])
            total_pixeles_naranja = {"total": pixeles_naranjas, "porcent": percentage(pixeles_naranjas, totalPixDetectados), "area_porcent": (percentage(pixeles_naranjas, totalPixDetectados)*area/100)}
            total_pixeles_amarillo = {"total": pixeles_amarillos, "porcent": percentage(pixeles_amarillos, totalPixDetectados), "area_porcent": (percentage(pixeles_amarillos, totalPixDetectados)*area/100)}
            total_pixeles_verde = {"total": pixeles_verdes, "porcent": percentage(pixeles_verdes, totalPixDetectados), "area_porcent": (percentage(pixeles_verdes, totalPixDetectados)*area/100)}
            total_pixeles_a_claro = {"total": pixeles_a_claro, "porcent": percentage(pixeles_a_claro, totalPixDetectados), "area_porcent": (percentage(pixeles_a_claro, totalPixDetectados)*area/100)}
            total_pixeles_a_medio = {"total": pixeles_a_medio, "porcent": percentage(pixeles_a_medio, totalPixDetectados), "area_porcent": (percentage(pixeles_a_medio, totalPixDetectados)*area/100)}
            total_pixeles_a_oscuro = {"total": pixeles_a_oscuro, "porcent": percentage(pixeles_a_oscuro, totalPixDetectados), "area_porcent": (percentage(pixeles_a_oscuro, totalPixDetectados)*area/100)}
            # ESTABLECEMOS EL RESULTADO
            arrResult = {fechas.index(fecha):{"img": nombreArchivo, "totalPixeles": totalPixDetectados, "fecha": fecha, "area": area, "naranja": total_pixeles_naranja, "amarillo": total_pixeles_amarillo, "verdes": total_pixeles_verde, "azul_claro": total_pixeles_a_claro, "azul_medio": total_pixeles_a_medio, "azul_oscuro": total_pixeles_a_oscuro}}
            arrRespuesta.update(arrResult)
    except Exception as Error:
        #CONFIG EMAIL
        site_shortcut_name = 'Data4SmartFarming'
        context = {
            'site_name': site_shortcut_name,
            'nombre_informe': alias,
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
            [email_user],#['soporte@d4smartfarming.com']
            # BCC
            ['backups@smartbits.es']
        )
        msg.attach_alternative(email_html_message_enterprise, "text/html")
        msg.send()
        exit()
    # HACEMOS EL FICHERO JSON
    app_json = json.dumps(arrRespuesta, cls=NpEncoder)
    eventid = datetime.now().strftime('%Y%m-%d%H-%M%S')
    nombreJson = str(uuid.uuid1().int)+'.json'
    file = open(settings.PARCEL_FOLDER+nombreJson, 'w')
    file.write(app_json)
    file.close()
    # HACEMOS EL FICHERO xls
    nombreXlsx = str(uuid.uuid1().int)+'.xlsx'
    json2xlsx(nombreJson, nombreXlsx, capa)
    #CONFIG EMAIL
    site_shortcut_name = 'Data4SmartFarming'
    context = {
        'site_name': site_shortcut_name,
        'nombre_informe': alias,
        'nombre_user': name_user
    }
    ## GUARDADO
    if serializer.save(parcela=parcela, urlSentinel="https://", imagen=nombreJson, xlsxFile=nombreXlsx, finifin=str(fechas[0])+' - '+str(fechas[-1]), tipo=1, polygon=[], fechas=datetime.now().strftime('%Y-%m-%d - %H:%M:%S'), capa=capa, alias=alias):
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
        [email_user],#['soporte@d4smartfarming.com']
        # BCC
        ['backups@smartbits.es']
    )
    msg.attach_alternative(email_html_message_enterprise, "text/html")
    msg.send()
    # ELIMINACION DE LA INSTANCIA TEMPORAL
    urlS = 'https://services.sentinel-hub.com/configuration/v1/wms/instances/'+instanceTmp
    requests.request("DELETE", urlS, headers=hed)