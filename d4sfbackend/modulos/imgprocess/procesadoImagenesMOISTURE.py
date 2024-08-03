# IMPORT LIBRERIAS
import json
import time
import urllib.request
import uuid
from datetime import datetime

import cv2
import numpy as np
import requests
from django.conf import settings
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from backend.settings.common import url_api_token, url_api_data_sets, url_api_data_source
from modulos.parcelas.models import Parcel
from utils import ConfigMail
from utils.D4sfConstants import url_api_instances_const, url_api_wms_const, url_api_id_const, \
    url_api_secret_const, protocol_url_const, url_api_data_products_1242_const, url_api_false_layers_const, \
    url_api_crs_const, url_api_time_const, url_api_eval_script_const
from utils.NpEncoder import NpEncoder
from utils.Utils import save_log
from .jsontoexcel import json2xlsx


def calculate_colors_images(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # ROJO/NARANJAS
    ligth_green = (1, 255, 0)
    dark_green = (25, 255, 255)
    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
    unique, counts = np.unique(mask, return_counts=True)
    pixeles_naranjas = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)

    # AMARILLOS
    ligth_green = (26, 255, 0)
    dark_green = (50, 255, 255)
    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
    unique, counts = np.unique(mask, return_counts=True)
    pixeles_amarillos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
    # VERDES
    ligth_green = (31, 0, 0)
    dark_green = (50, 255, 255)
    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
    unique, counts = np.unique(mask, return_counts=True)
    pixeles_verdes = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)

    # AZULES CLARITOS
    ligth_green = (51, 255, 0)
    dark_green = (100, 255, 255)
    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
    unique, counts = np.unique(mask, return_counts=True)
    pixeles_a_claro = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)

    # AZULES MEDIOS
    ligth_green = (101, 255, 0)
    dark_green = (115, 255, 255)
    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
    unique, counts = np.unique(mask, return_counts=True)
    pixeles_a_medio = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)

    # AZULES OSCURO
    ligth_green = (116, 255, 0)
    dark_green = (200, 255, 255)
    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
    unique, counts = np.unique(mask, return_counts=True)
    pixeles_a_oscuro = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
    return pixeles_a_claro, pixeles_a_medio, pixeles_a_oscuro, pixeles_amarillos, pixeles_naranjas, pixeles_verdes


def read_images(nombre_archivo):
    image = cv2.imread(settings.PARCEL_FOLDER + nombre_archivo, cv2.IMREAD_UNCHANGED)
    trans_mask = image[:, :, 3] == 0
    image[trans_mask] = [255, 255, 255, 255]
    return image


def create_data_moisture(name, coordinates):
    data = {
        'name': name,
        'additionalData': {
            'showLogo': False,
            'showWarnings': False,
            'imageQuality': 30,
            'disabled': False
        },
        'areaOfInterest': {
            'type': 'Polygon',
            'coordinates': coordinates,
            'crs': {
                'type': 'name',
                'properties': {
                    'name': 'urn:ogc:def:crs:EPSG::4326'
                }
            }
        },
    }
    return data


def calculate_total_pixels(area, pixeles_a_claro, pixeles_a_medio, pixeles_a_oscuro, pixeles_amarillos,
                           pixeles_naranjas, pixeles_verdes):
    total_pix_detectados = sum(
        [pixeles_naranjas, pixeles_amarillos, pixeles_verdes, pixeles_a_claro, pixeles_a_medio,
         pixeles_a_oscuro])

    total_pixeles_naranja = {"total": pixeles_naranjas,
                             "porcent": NpEncoder.percentage(pixeles_naranjas, total_pix_detectados),
                             "area_porcent": (
                                         NpEncoder.percentage(pixeles_naranjas, total_pix_detectados) * area / 100)}
    total_pixeles_amarillo = {"total": pixeles_amarillos,
                              "porcent": NpEncoder.percentage(pixeles_amarillos, total_pix_detectados),
                              "area_porcent": (
                                      NpEncoder.percentage(pixeles_amarillos, total_pix_detectados) * area / 100)}
    total_pixeles_verde = {"total": pixeles_verdes,
                           "porcent": NpEncoder.percentage(pixeles_verdes, total_pix_detectados),
                           "area_porcent": (NpEncoder.percentage(pixeles_verdes, total_pix_detectados) * area / 100)}
    total_pixeles_a_claro = {"total": pixeles_a_claro,
                             "porcent": NpEncoder.percentage(pixeles_a_claro, total_pix_detectados),
                             "area_porcent": (NpEncoder.percentage(pixeles_a_claro, total_pix_detectados) * area / 100)}
    total_pixeles_a_medio = {"total": pixeles_a_medio,
                             "porcent": NpEncoder.percentage(pixeles_a_medio, total_pix_detectados),
                             "area_porcent": (NpEncoder.percentage(pixeles_a_medio, total_pix_detectados) * area / 100)}
    total_pixeles_a_oscuro = {"total": pixeles_a_oscuro,
                              "porcent": NpEncoder.percentage(pixeles_a_oscuro, total_pix_detectados),
                              "area_porcent": (
                                          NpEncoder.percentage(pixeles_a_oscuro, total_pix_detectados) * area / 100)}

    return (total_pix_detectados, total_pixeles_a_claro, total_pixeles_a_medio, total_pixeles_a_oscuro,
            total_pixeles_amarillo, total_pixeles_naranja, total_pixeles_verde)


def create_layer_moisture_index():
    layer = {
        'id': 'MOISTURE_INDEX',
        'title': 'Moisture Index',
        'description': 'Based on combination of bands (B8A - B11)/(B8A + B11)',
        'styles': [
            {
                'name': 'default',
                'dataProduct': {
                    '@id': url_api_data_products_1242_const,
                    'id': 1242,
                    'name': 'MOISTURE_INDEX.MOISTURE',
                    'description': 'Moisture Index - Moisture color gradient visualization',
                    'evalScript': url_api_eval_script_const,
                    'dataset': {
                        '@id': url_api_data_sets
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
    return layer


def moisture_img_t2(serializer, email_user, name_user):
    # await asyncio.sleep(10)
    # RECOGIDA DE DATOS GLOBAL

    url_sent = serializer.validated_data['urlSentinel']
    fechas = serializer.validated_data['fechas']
    parcela = serializer.validated_data['parcela']
    capa = serializer.validated_data['capa']
    # RECOGIDA DE DATOS T1
    # alias = serializer.validated_data['alias'] or ''
    # REGOGIDA DATOS T2
    polygon = serializer.validated_data['polygon']
    fecha_elegida = serializer.validated_data['fecha_elegida']
    id_parcelas = serializer.validated_data['id_parcelas']

    name_poligon = 'Polygons4GraficosType2Tmp'

    # CREAMOS UN BUCLE POR CADA UNO DE LOS POLIGONOS
    arr_respuesta, instance_tmp, header = generate_poligon_by_dates(name_poligon, capa, email_user, fecha_elegida,
                                                                    fechas, id_parcelas, name_user, parcela, polygon,
                                                                    url_sent)
    # HACEMOS EL FICHERO JSON
    app_json = json.dumps(arr_respuesta, cls=NpEncoder)

    # eventid = datetime.now().strftime('%Y%m-%d%H-%M%S')
    nombre_json = str(uuid.uuid1().int) + '.json'
    file = open(settings.PARCEL_FOLDER + nombre_json, 'w')
    file.write(app_json)
    file.close()
    # HACEMOS EL FICHERO xls
    nombre_xlsx = str(uuid.uuid1().int) + '.xlsx'
    json2xlsx(nombre_json, nombre_xlsx, capa)

    # AJUSTE DE NOMBRE
    if parcela == str(0):
        parcela = 'Gráfico Tipo 2'

    # AJUSTE DE FECHA
    finicio_fin = fecha_elegida
    if not fecha_elegida:
        finicio_fin = datetime.now().strftime('%Y-%m-%d')
    # CONFIG EMAIL
    site_shortcut_name = 'Data4SmartFarming'
    context = {
        'site_name': site_shortcut_name,
        'nombre_informe': parcela,
        'nombre_user': name_user
    }

    # GUARDADO
    if serializer.save(parcela=parcela, urlSentinel=protocol_url_const, imagen=nombre_json, xlsxFile=nombre_xlsx,
                       finifin=finicio_fin, tipo=2, polygon=[], fechas=datetime.now().strftime('%Y-%m-%d - %H:%M:%S'),
                       capa=capa, fechaElegida=fecha_elegida):
        # ENVIO DE CORREO OK
        title = "=?utf-8?Q?=F0=9F=93=8B_Informe_generado_Correctamente?="

        ConfigMail.send_email(title, email_user, 'Informe_generado_correctamente.html', context)
    else:
        # ENVIO CORREO KO
        title = "=?utf-8?Q?=E2=9D=97_Error_al_generar_el_Informe?="
        ConfigMail.send_email(title, email_user, 'Informe_generado_error.html', context)

    # ELIMINACION DE LA INSTANCIA TEMPORAL
    url_s = url_api_instances_const + instance_tmp
    requests.request("DELETE", url_s, headers=header)


def generate_poligon_by_dates(name_poligon, capa, email_user, fecha_elegida, fechas, id_parcelas,
                              name_user, parcela, polygon, url_sent):
    # VARIABLE DE RESPUESTA
    arr_respuesta = {}
    instance_tmp = ''

    # CREAMOS LA INSTANCIA DE SENTINEL
    # OBTENEMOS EL TOKEN DE SESSION
    client = BackendApplicationClient(client_id=url_api_id_const)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=url_api_token, client_id=url_api_id_const,
                              client_secret=url_api_secret_const)
    header = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + token['access_token']
    }

    for poly in polygon:
        # CREAMOS LA INSTANCIA TEMPORAL
        layer = create_layer_moisture_index()

        # CREAMOS LA INSTANCIA CON EL/LOS POLIGONOS
        data = create_data_moisture(name_poligon, poly)

        try:
            reponses = requests.request("POST", url_api_instances_const, headers=header, data=json.dumps(data))

            response_json = reponses.json()
            instance_tmp = response_json['id']
            # CONFIGURAMOS LOS LAYERS
            url_s = url_api_instances_const + instance_tmp + '/layers'
            requests.request("POST", url_s, headers=header, data=json.dumps(layer))

            time.sleep(3)
            # OBTENEMOS EL URL DEL BOX
            url = url_sent[polygon.index(poly)]
            # BUSCAMOS LA PARCELA PARA EL AREA
            area = 0.0

            if id_parcelas:
                id_parcela = id_parcelas[polygon.index(poly)]

                results = Parcel.objects.filter(id=int(id_parcela))

                for result in results:
                    area = result.__dict__['area']

                area = float(area)

            # ESTABLECEMOS EL NOMRBE DE ARCHIVO
            nombre_archivo = str(uuid.uuid1().int) + '.png'
            if fecha_elegida:
                urllib.request.urlretrieve(
                    str(url_api_wms_const + instance_tmp + url_api_false_layers_const + capa + url_api_time_const +
                        fecha_elegida + url_api_crs_const + url),
                    settings.PARCEL_FOLDER + nombre_archivo)
            else:
                urllib.request.urlretrieve(
                    str(url_api_wms_const + instance_tmp + url_api_false_layers_const + capa + url_api_crs_const + url),
                    settings.PARCEL_FOLDER + nombre_archivo)

            # LEEMOS LA IMAGEN
            image = read_images(nombre_archivo)

            # CALCULOS /*******************************************************************
            pixeles_a_claro, pixeles_a_medio, pixeles_a_oscuro, pixeles_amarillos, pixeles_naranjas, pixeles_verdes = (
                calculate_colors_images(image))

            # UNION TOTALES
            (total_pix_detectados, total_pixeles_a_claro, total_pixeles_a_medio, total_pixeles_a_oscuro,
             total_pixeles_amarillo, total_pixeles_naranja, total_pixeles_verde) = calculate_total_pixels(
                area, pixeles_a_claro, pixeles_a_medio, pixeles_a_oscuro, pixeles_amarillos, pixeles_naranjas,
                pixeles_verdes)

            # ESTABLECEMOS EL RESULTADO
            arr_result = {url_sent.index(url): {"img": nombre_archivo, "totalPixeles": total_pix_detectados,
                                                "fecha": fechas[url_sent.index(url)], "area": area,
                                                "naranja": total_pixeles_naranja, "amarillo": total_pixeles_amarillo,
                                                "verdes": total_pixeles_verde, "azul_claro": total_pixeles_a_claro,
                                                "azul_medio": total_pixeles_a_medio,
                                                "azul_oscuro": total_pixeles_a_oscuro}}
            arr_respuesta.update(arr_result)

        except Exception as Error:
            site_shortcut_name = 'Data4SmartFarming'
            # log purpuse
            extra_data = {
                'site_name': site_shortcut_name,
                'nombre_informe': parcela,
                'nombre_user': name_user,
                'error': str(Error),
            }
            save_log('Error en el procesado de imagenes MOISTURE', requests, extra_data)

            title = "=?utf-8?Q?=E2=9D=97_Error_al_generar_el_Informe?="
            context = {
                'site_name': site_shortcut_name,
                'nombre_informe': parcela,
                'nombre_user': name_user
            }
            template = 'Informe_generado_error.html'

            ConfigMail.send_email(title, email_user, template, context)

            exit()
    return arr_respuesta, instance_tmp, header


def moisture_img_t1(serializer, email_user, name_user):
    # RECOGIDA DE DATOS GLOBAL
    url_sent = serializer.validated_data['urlSentinel']
    fechas = serializer.validated_data['fechas']
    parcela = serializer.validated_data['parcela']
    capa = serializer.validated_data['capa']
    # RECOGIDA DE DATOS T1
    alias = serializer.validated_data['alias'] or ''
    # REGOGIDA DATOS T2
    polygon = serializer.validated_data['polygon']

    # VARIABLE DE RESPUESTA
    name_poligon = 'Polygons4GraficosType1Tmp'

    arr_respuesta, instance_tmp, header = generate_poligon_by_dates(name_poligon, capa, email_user, None,
                                                                    fechas, None, name_user, parcela, polygon,
                                                                    url_sent)

    # CREAMOS LA INSTANCIA TEMPORAL
    layer = create_layer_moisture_index()
    # CREAMOS LA INSTANCIA CON EL/LOS POLIGONOS
    data = create_data_moisture('Polygons4GraficosType1Tmp', polygon)

    try:
        url_s = url_api_instances_const
        reponses = requests.request("POST", url_s, headers=header, data=json.dumps(data))

        response_json = reponses.json()
        instance_tmp = response_json['id']
        # CONFIGURAMOS LOS LAYERS
        url_s = url_api_instances_const + instance_tmp + '/layers'
        requests.request("POST", url_s, headers=header, data=json.dumps(layer))

        time.sleep(3)
        # OBTENEMOS EL URL DEL BOX
        # url = url_sent[polygon]
        # BUSCAMOS LA PARCELA PARA EL AREA
        results = Parcel.objects.filter(id=int(parcela))
        area = 0.0
        for result in results:
            area = result.__dict__['area']
        area = float(area)

        for fecha in fechas:
            nombre_archivo = str(uuid.uuid1().int) + '.png'
            urllib.request.urlretrieve(
                str(url_api_wms_const + instance_tmp + url_api_false_layers_const + capa + '&TIME=' + fecha +
                    url_api_crs_const + url_sent[0]), settings.PARCEL_FOLDER + nombre_archivo)

            # LEEMOS LA IMAGEN
            image = read_images(nombre_archivo)

            # CALCULOS /*******************************************************************
            pixeles_a_claro, pixeles_a_medio, pixeles_a_oscuro, pixeles_amarillos, pixeles_naranjas, pixeles_verdes = (
                calculate_colors_images(
                    image))

            (total_pix_detectados, total_pixeles_a_claro, total_pixeles_a_medio, total_pixeles_a_oscuro,
             total_pixeles_amarillo, total_pixeles_naranja, total_pixeles_verde) = (
                calculate_total_pixels(
                    area, pixeles_a_claro, pixeles_a_medio, pixeles_a_oscuro, pixeles_amarillos, pixeles_naranjas,
                    pixeles_verdes))

            # ESTABLECEMOS EL RESULTADO
            arr_result = {
                fechas.index(fecha): {"img": nombre_archivo, "totalPixeles": total_pix_detectados, "fecha": fecha,
                                      "area": area, "naranja": total_pixeles_naranja,
                                      "amarillo": total_pixeles_amarillo, "verdes": total_pixeles_verde,
                                      "azul_claro": total_pixeles_a_claro, "azul_medio": total_pixeles_a_medio,
                                      "azul_oscuro": total_pixeles_a_oscuro}}
            arr_respuesta.update(arr_result)
    except Exception as Error:
        # CONFIG EMAIL
        site_shortcut_name = 'Data4SmartFarming'
        context = {
            'site_name': site_shortcut_name,
            'nombre_informe': alias,
            'nombre_user': name_user
        }

        # log purpuse
        extra_data = {
            'site_name': site_shortcut_name,
            'nombre_informe': parcela,
            'nombre_user': name_user,
            'error': str(Error),
        }
        save_log('Error en el procesado de imagenes MOISTURE', requests, extra_data)
        # ENVIO CORREO KO

        title = "=?utf-8?Q?=E2=9D=97_Error_al_generar_el_Informe?="
        ConfigMail.send_email(title, email_user, 'Informe_generado_error.html', context)
        exit()

    # HACEMOS EL FICHERO JSON
    app_json = json.dumps(arr_respuesta, cls=NpEncoder)
    # eventid = datetime.now().strftime('%Y%m-%d%H-%M%S')
    nombre_json = str(uuid.uuid1().int) + '.json'
    file = open(settings.PARCEL_FOLDER + nombre_json, 'w')
    file.write(app_json)
    file.close()
    # HACEMOS EL FICHERO xls
    nombre_xlsx = str(uuid.uuid1().int) + '.xlsx'
    json2xlsx(nombre_json, nombre_xlsx, capa)
    # CONFIG EMAIL
    site_shortcut_name = 'Data4SmartFarming'

    context = {
        'site_name': site_shortcut_name,
        'nombre_informe': alias,
        'nombre_user': name_user
    }
    # GUARDADO
    if serializer.save(parcela=parcela, urlSentinel=protocol_url_const, imagen=nombre_json, xlsxFile=nombre_xlsx,
                       finifin=str(fechas[0]) + ' - ' + str(fechas[-1]), tipo=1, polygon=[],
                       fechas=datetime.now().strftime('%Y-%m-%d - %H:%M:%S'), capa=capa, alias=alias):
        # ENVIO DE CORREO OK
        title = "=?utf-8?Q?=F0=9F=93=8B_Informe_generado_Correctamente?="
        ConfigMail.send_email(title, email_user, 'Informe_generado_correctamente.html', context)
    else:
        # ENVIO CORREO KO
        title = "=?utf-8?Q?=E2=9D=97_Error_al_generar_el_Informe?="
        ConfigMail.send_email(title, email_user, 'Informe_generado_error.html', context)

    # ELIMINACION DE LA INSTANCIA TEMPORAL
    url_s = url_api_instances_const + instance_tmp
    requests.request("DELETE", url_s, headers=header)
