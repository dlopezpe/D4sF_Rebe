import os
from django.conf import settings
from datetime import datetime
from sentinelhub import SHConfig
import numpy as np
import cv2
import matplotlib

from utils.NpEncoder import NpEncoder
from sentinelhub import WcsRequest, MimeType, CRS, BBox, DataCollection, CustomUrlParam, WebFeatureService
# from s2cloudless import S2PixelCloudDetector, CloudMaskRequest, get_s2_evalscript
import uuid
import json
from threading import Thread
from modulos.parcelas.models import Parcel
from django.contrib.gis.geos import GEOSGeometry
import pandas as pd
from .jsontoexcel import json2xlsx
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

matplotlib.use('Agg')
# Configuracion Sentinel
CLIENT_ID = '33467c23-fada-4405-8a5b-33ee38169273'
CLIENT_SECRET = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'
CLIENT_INSTANCE = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'

# Configuración de colores NDVI
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


def procesar_moisture(serializer, email_user, name_user, uid, request=None):
    if request is None:
        request = {}

    def sup_process(sub_serializer, sub_email_user, sub_name_user, sub_uid, sub_request=None):

        if sub_request is None:
            sub_request = {}
        now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        # nombre_archivo_errores = str(uuid.uuid1().int) + '.log'
        nombre_archivo_errores = sub_serializer.validated_data['nombre'] + "__" + str(now) + '.log'
        file_err = open(settings.PARCEL_FOLDER + nombre_archivo_errores, 'w')
        cadena_parcelas = ''
        nombre = sub_serializer.validated_data['nombre']
        capa = sub_serializer.validated_data['capa']
        id_parcelas = sub_serializer.validated_data['id_parcelas']
        fecha_inicio = sub_serializer.validated_data['fecha_inicio']
        fecha_fin = sub_serializer.validated_data['fecha_fin']
        enterprise_id = sub_serializer.validated_data['enterprise_id']
        es_cooperative = sub_serializer.validated_data['es_cooperative']
        include_clouds = sub_serializer.validated_data['include_clouds']
        time_interval = (fecha_inicio, fecha_fin)
        errores = False
        fallidas = ""
        # flag var to check if file exists
        file_exists = False

        # log purpuse or check file errors implemented default
        context_logs = {
            'user_email': sub_email_user,
            'message': 'Generando documento procesarMOISTURE via sup_process',
            'status': 'success',
            'extra_data': {
                'cadena_parcelas': cadena_parcelas,
                'nombre': nombre,
                'capa': capa,
                'id_parcelas': id_parcelas,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'enterprise_id': enterprise_id,
                'es_cooperative': es_cooperative,
                'include_clouds': include_clouds,
                'time_interval': time_interval,
                'errores': errores,
                'fallida': fallidas,
            }
        }

        # savelog(context_logs,request)

        file_err.write(str(sub_email_user) + '\n')
        file_err.write(str(sub_name_user) + '\n')
        file_err.write(str(sub_uid) + '\n')
        for id_parcela in id_parcelas:
            parcel = Parcel.objects.get(pk=int(id_parcela))
            nombre_parcela = parcel.name
            cadena_parcelas += str(parcel) + ' -> ' + nombre_parcela + '\n'
        file_err.write(str(cadena_parcelas) + '\n')

        file_err.close()

        db_informe = sub_serializer
        db_informe.save(
            nombre=nombre,
            capa=capa,
            fechaInicio=fecha_inicio,
            fechaFin=fecha_fin,
            enterprise_id=enterprise_id,
            esCooperative=es_cooperative,
            id_parcelas=cadena_parcelas,
            includeClouds=include_clouds,
            user_created=sub_uid,
            estado=1
        )

        try:
            # Envio de mail PRE (solo para nosotros)
            # CONFIG EMAIL
            site_shortcut_name = 'Data4SmartFarming'
            context = {
                'site_name': site_shortcut_name,
                'nombre_informe': nombre,
                'nombre_user': sub_name_user,
                'email_user': sub_email_user,
                'parcelas': id_parcelas,
                'capa': capa,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            }
            # ENVIO DE CORREO OK
            title = "=?utf-8?Q?=F0=9F=91=B7_Nuevo_informe_solicitado?="
            email_html_message_enterprise = render_to_string('Informe_solicitud_adm_empezar.html', context)
            # ENVIAMOS EL MAIL
            msg = EmailMultiAlternatives(
                # title:
                title,
                # message:
                email_html_message_enterprise,
                # from:
                "D4SmartFarming <soporte@d4smartfarming.com>",
                # to:
                ['soported4sf@smartbits.es'],
                # BCC
                ['backups@smartbits.es']
            )
            msg.attach_alternative(email_html_message_enterprise, "text/html")
            is_send_email = msg.send()
            # log purpuse
            context_logs['status'] = 'success'
            context_logs['extra_data']['is_send_email'] = is_send_email
            context_logs['message'] = 'Enviado email Nuevo_informe_solicitado procesarMOISTURE via sup_process'
            # savelog(context_logs,request)
            # end log purpuse
        except Exception as Error:
            file_err = open(settings.PARCEL_FOLDER + "catch_" + nombre_archivo_errores, 'a')
            file_err.write(" -- Linea 168 - {Error}  " + str(Error) + "\n")
            file_err.close()

            context_logs['extra_data']['error'] = str(Error)
            context_logs['status'] = 'error'
            context_logs['message'] = 'Error al enviar email Nuevo_informe_solicitado procesarMOISTURE via sup_process'
            # savelog(context_logs,request)
            # end log purpuse
        try:
            # Establecemos la configuración con sentinel
            config = SHConfig()
            if CLIENT_ID and CLIENT_SECRET:
                config.sh_client_id = CLIENT_ID
                config.sh_client_secret = CLIENT_SECRET
                config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
            if config.instance_id == '':
                print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")

                file_err = open(settings.PARCEL_FOLDER + nombre_archivo_errores, 'a')
                file_err.write(
                    "Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.\n")
                file_err.close()

            arrRespuesta = {}
            arrError = []
            for id_parcela in id_parcelas:
                parcel = Parcel.objects.get(pk=int(id_parcela))
                nombre_parcela = parcel.name
                polygon = GEOSGeometry(parcel.polygon)
                nombreJson = str(id_parcela) + '.json'
                file = open(settings.PARCEL_FOLDER + nombreJson, 'w')
                file.write(str(polygon.geojson))
                file.close()

                fallidas = ""

                geometry_string = str(polygon.wkt)
                areaCrud = polygon.area
                # area = float(decimal.Context(prec=3).create_decimal(float(str(areaCrud)[:10])))
                area = parcel.area
                bbox = BBox(polygon.extent, crs=CRS.WGS84)

                file_err = open(settings.PARCEL_FOLDER + nombre_archivo_errores, 'a')
                file_err.write("--------MOISTURE-------\n")
                file_err.write("bbox=" + str(bbox) + "\n")
                file_err.write("config=" + str(config) + "\n")
                file_err.write("time=" + str(time_interval) + "\n")
                file_err.write("geometry_string=" + str(geometry_string) + "\n")
                file_err.close()
                try:
                    wms_ndvi_request = WcsRequest(
                        data_collection=DataCollection.SENTINEL2_L1C,
                        layer='MOISTURE_INDEX',
                        bbox=bbox,
                        time=time_interval,
                        resx='1m',
                        resy='1m',
                        custom_url_params={
                            CustomUrlParam.SHOWLOGO: False,
                            CustomUrlParam.GEOMETRY: geometry_string
                        },
                        config=config,
                        image_format=MimeType.PNG
                    )
                    images = wms_ndvi_request.get_data()
                    # log purpuse
                    context_logs['status'] = 'success'
                    context_logs['message'] = 'llamada sentinel layer MOISTURE_INDEX procesarMOISTURE via sup_process'
                    # savelog(context_logs,request)
                    # end log purpuse
                except Exception as Error:
                    file_err = open(settings.PARCEL_FOLDER + "catch_" + nombre_archivo_errores, 'a')
                    file_err.write(id_parcela + " -- Linea 251 - {Error} " + str(Error) + "\n")
                    file_err.close()
                    fallidas += str(id_parcela) + " "
                    errores = True
                    # log
                    context_logs['errores'] = str(errores)
                    context_logs['fallidas'] = fallidas
                    context_logs['extra_data']['id_parcela'] = id_parcela
                    context_logs['extra_data']['error'] = str(Error)
                    context_logs['status'] = 'error'
                    context_logs[
                        'message'] = 'Error sentinel WcsRequest request layer MOISTURE_INDEX procesarMOISTURE via sup_process'
                    # savelog(context_logs,request)

                file_err = open(settings.PARCEL_FOLDER + nombre_archivo_errores, 'a')
                file_err.write("MOISTURE request = " + str(wms_ndvi_request) + "\n")
                file_err.write("MOISTURE URLs = " + str(wms_ndvi_request.get_url_list()) + "\n")
                # url="https://services.sentinel-hub.com/ogc/wcs/"+CLIENT_INSTANCE+"?SERVICE=wcs&WARNINGS=False&MAXCC=100.0&ShowLogo=False&Geometry=POLYGON+%28%28&FORMAT=image%2Fpng&CRS=EPSG%3A4326&TIME=2022-11-04T14%3A52%3A49Z%2F2022-11-04T14%3A52%3A49Z&RESX=1m&RESY=1m&COVERAGE=TRUE_COLOR&REQUEST=GetCoverage&VERSION=1.1.2"

                file_err.close()

                if include_clouds:
                    file_err = open(settings.PARCEL_FOLDER + nombre_archivo_errores, 'a')
                    file_err.write("---------NUBES----------\n")
                    file_err.write("bbox=" + str(bbox) + "\n")
                    file_err.write("config=" + str(config) + "\n")
                    file_err.write("time=" + str(time_interval) + "\n")
                    file_err.write("geometry_string=" + str(geometry_string) + "\n")
                    file_err.close()
                    try:
                        wms_true_color_clouds_request = WcsRequest(
                            data_collection=DataCollection.SENTINEL2_L1C,
                            layer='PRUEBAS-NUBES',
                            bbox=bbox,
                            time=time_interval,
                            resx='1m',
                            resy='1m',
                            custom_url_params={
                                CustomUrlParam.SHOWLOGO: False,
                                CustomUrlParam.GEOMETRY: geometry_string
                            },
                            config=config,
                            image_format=MimeType.TIFF
                        )
                        images_true_color_cloud = wms_true_color_clouds_request.get_data()
                        wfs_iterator = WebFeatureService(
                            bbox,
                            time_interval,
                            data_collection=DataCollection.SENTINEL2_L1C,
                            maxcc=100,
                            config=config
                        )
                        results_cloud_wfs = list(wfs_iterator)

                        # True Color
                        file_err = open(settings.PARCEL_FOLDER + nombre_archivo_errores, 'a')
                        file_err.write("------------True color---------------\n")
                        file_err.write("bbox=" + str(bbox) + "\n")
                        file_err.write("config=" + str(config) + "\n")
                        file_err.write("time=" + str(time_interval) + "\n")
                        file_err.write("geometry_string=" + str(geometry_string) + "\n")
                        file_err.write("MOISTURE request = " + str(wms_true_color_clouds_request) + "\n")
                        file_err.write("MOISTURE URLs = " + str(wms_true_color_clouds_request.get_url_list()) + "\n")
                        file_err.close()

                        # log purpuse
                        context_logs['status'] = 'success'
                        context_logs['message'] = 'llamada sentinel layer PRUEBAS-NUBES procesarMOISTURE via sup_process'
                        # savelog(context_logs,request)
                        # end log purpuse

                    except Exception as Error:
                        file_err = open(settings.PARCEL_FOLDER + "catch_" + nombre_archivo_errores, 'a')
                        file_err.write(id_parcela + " -- Linea 308 - {Error} " + str(Error) + "\n")
                        file_err.close()
                        fallidas += str(id_parcela) + " "
                        errores = True
                        # log
                        context_logs['errores'] = str(errores)
                        context_logs['fallidas'] = fallidas
                        context_logs['extra_data']['id_parcela'] = id_parcela
                        context_logs['extra_data']['error'] = str(Error)
                        context_logs['status'] = 'error'
                        context_logs[
                            'message'] = 'Error sentinel WcsRequest request layer PRUEBAS-NUBES procesarMOISTURE via sup_process'
                        # savelog(context_logs,request)

                try:
                    wms_true_color_request = WcsRequest(
                        data_collection=DataCollection.SENTINEL2_L1C,
                        layer='TRUE_COLOR',
                        bbox=bbox,
                        time=time_interval,
                        resx='1m',
                        resy='1m',
                        custom_url_params={
                            CustomUrlParam.SHOWLOGO: False,
                            CustomUrlParam.GEOMETRY: geometry_string
                        },
                        config=config,
                        image_format=MimeType.PNG
                    )
                    images_true_color = wms_true_color_request.get_data()
                    # log purpuse
                    context_logs['status'] = 'success'
                    context_logs['message'] = 'llamada sentinel layer TRUE_COLOR procesarMOISTURE via sup_process'
                    # savelog(context_logs,request)
                    # end log purpuse
                except Exception as Error:
                    file_err = open(settings.PARCEL_FOLDER + "catch_" + nombre_archivo_errores, 'a')
                    file_err.write(id_parcela + " -- Linea 338 - {Error} " + str(Error) + " \n")
                    file_err.close()
                    fallidas += str(id_parcela) + " "
                    errores = True
                    # log
                    context_logs['errores'] = fallidas
                    context_logs['fallidas'] = fallidas
                    context_logs['extra_data']['id_parcela'] = id_parcela
                    context_logs['extra_data']['error'] = str(Error)
                    context_logs['status'] = 'error'
                    context_logs[
                        'message'] = 'Error sentinel WcsRequest request layer TRUE_COLOR procesarMOISTURE via sup_process'
                    # savelog(context_logs,request)

                file_err = open(settings.PARCEL_FOLDER + nombre_archivo_errores, 'a')
                file_err.write("------------True color---------------\n")
                file_err.write("bbox=" + str(bbox) + "\n")
                file_err.write("config=" + str(config) + "\n")
                file_err.write("time=" + str(time_interval) + "\n")
                file_err.write("geometry_string=" + str(geometry_string) + "\n")
                file_err.write("MOISTURE request = " + str(wms_true_color_request) + "\n")
                file_err.write("MOISTURE URLs = " + str(wms_true_color_request.get_url_list()) + "\n")
                file_err.close()

                fechaAnterior = "0"
                validImage = False
                for idx, (image, time) in enumerate(zip(images, wms_ndvi_request.get_dates())):

                    file_err = open(settings.PARCEL_FOLDER + nombre_archivo_errores, 'a')
                    file_err.write("----------------------\n")
                    file_err.write(str(nombre_parcela) + '\n')
                    file_err.write(str(time.date().isoformat()) + '\n')
                    file_err.write(str(idx) + '\n')
                    file_err.write("----------------------\n")
                    file_err.close()

                    if str(time.date().isoformat()) != fechaAnterior:
                        try:
                            nombreArchivo = str(uuid.uuid1().int) + '_' + str(idx) + '_' + id_parcela + '.png'
                            trans_mask = image[:, :, 3] == 0
                            image[trans_mask] = [255, 255, 255, 255]
                            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            cv2.imwrite(settings.PARCEL_FOLDER + nombreArchivo, img)
                            cv2.imwrite(settings.PARCEL_FOLDER + 'trueColor_' + nombreArchivo,
                                        cv2.cvtColor(images_true_color[idx], cv2.COLOR_BGR2RGB))
                            # cv2.imwrite(settings.PARCEL_FOLDER + 'natural_img_' + nombreArchivo, images_true_color[idx])

                            if include_clouds:
                                cv2.imwrite(settings.PARCEL_FOLDER + 'cloud_' + nombreArchivo,
                                            cv2.cvtColor(images_true_color_cloud[idx], cv2.COLOR_BGR2RGB))

                            # CALCULOS /*******************************************************************
                            image2 = cv2.imread(settings.PARCEL_FOLDER + nombreArchivo, cv2.IMREAD_UNCHANGED)
                            img = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
                            # img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
                            # ROJO/NARANJAS
                            ligth_green = (1, 255, 0)
                            dark_green = (25, 255, 255)
                            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                            mask_rojo = cv2.inRange(img_hsv, ligth_green, dark_green)
                            unique, counts = np.unique(mask, return_counts=True)
                            pixeles_naranjas = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
                            # AMARILLOS
                            ligth_green = (26, 255, 0)
                            dark_green = (50, 255, 255)
                            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                            mask_amarillos = cv2.inRange(img_hsv, ligth_green, dark_green)
                            unique, counts = np.unique(mask, return_counts=True)
                            pixeles_amarillos = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
                            # VERDES
                            ligth_green = (31, 0, 0)
                            dark_green = (50, 255, 255)
                            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                            mask_verdes = cv2.inRange(img_hsv, ligth_green, dark_green)
                            unique, counts = np.unique(mask, return_counts=True)
                            pixeles_verdes = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
                            # AZULES CLARITOS
                            ligth_green = (51, 255, 0)
                            dark_green = (100, 255, 255)
                            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                            mask_azules_claro = cv2.inRange(img_hsv, ligth_green, dark_green)
                            unique, counts = np.unique(mask, return_counts=True)
                            pixeles_a_claro = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
                            # AZULES MEDIOS
                            ligth_green = (101, 255, 0)
                            dark_green = (115, 255, 255)
                            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                            mask_azules_medios = cv2.inRange(img_hsv, ligth_green, dark_green)
                            unique, counts = np.unique(mask, return_counts=True)
                            pixeles_a_medio = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)
                            # AZULES OSCURO
                            ligth_green = (116, 255, 0)
                            dark_green = (200, 255, 255)
                            mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                            mask_azules_oscuros = cv2.inRange(img_hsv, ligth_green, dark_green)
                            unique, counts = np.unique(mask, return_counts=True)
                            pixeles_a_oscuro = NpEncoder.get_pixeles(np.asarray((unique, counts)).T)

                            # UNIONES DE MASCARAS
                            mask_union = cv2.bitwise_or(mask_rojo, mask_amarillos)
                            mask_union2 = cv2.bitwise_or(mask_union, mask_verdes)
                            mask_union3 = cv2.bitwise_or(mask_union2, mask_azules_claro)
                            mask_union4 = cv2.bitwise_or(mask_union3, mask_azules_medios)
                            mask_union5 = cv2.bitwise_or(mask_union4, mask_azules_oscuros)
                            unique, counts = np.unique(mask_union5, return_counts=True)
                            arr_total = np.asarray((unique, counts)).T
                            total_pixeles = arr_total[1][1]
                            print(total_pixeles)
                            # FIN CALCULOS /*******************************************************************

                            total_pix_detectados = sum(
                                [pixeles_naranjas, pixeles_amarillos, pixeles_verdes, pixeles_a_claro, pixeles_a_medio,
                                 pixeles_a_oscuro])
                            total_pixeles_naranja = {"total": pixeles_naranjas,
                                                     "porcent": NpEncoder.percentage(pixeles_naranjas,
                                                                                     total_pix_detectados),
                                                     "area_porcent": (
                                                             NpEncoder.percentage(pixeles_naranjas,
                                                                                  total_pix_detectados) * area / 100)}
                            total_pixeles_amarillo = {"total": pixeles_amarillos,
                                                      "porcent": NpEncoder.percentage(pixeles_amarillos,
                                                                                      total_pix_detectados),
                                                      "area_porcent": (
                                                              NpEncoder.percentage(pixeles_amarillos,
                                                                                   total_pix_detectados) * area / 100)}
                            total_pixeles_verde = {"total": pixeles_verdes,
                                                   "porcent": NpEncoder.percentage(pixeles_verdes, total_pix_detectados),
                                                   "area_porcent": (NpEncoder.percentage(pixeles_verdes,
                                                                                         total_pix_detectados) * area / 100)}
                            total_pixeles_a_claro = {"total": pixeles_a_claro,
                                                     "porcent": NpEncoder.percentage(pixeles_a_claro,
                                                                                     total_pix_detectados),
                                                     "area_porcent": (NpEncoder.percentage(pixeles_a_claro,
                                                                                           total_pix_detectados) * area / 100)}
                            total_pixeles_a_medio = {"total": pixeles_a_medio,
                                                     "porcent": NpEncoder.percentage(pixeles_a_medio,
                                                                                     total_pix_detectados),
                                                     "area_porcent": (NpEncoder.percentage(pixeles_a_medio,
                                                                                           total_pix_detectados) * area / 100)}
                            total_pixeles_a_oscuro = {"total": pixeles_a_oscuro,
                                                      "porcent": NpEncoder.percentage(pixeles_a_oscuro,
                                                                                      total_pix_detectados),
                                                      "area_porcent": (
                                                              NpEncoder.percentage(pixeles_a_oscuro,
                                                                                   total_pix_detectados) * area / 100)}
                            # UNION TOTALES
                            if include_clouds:
                                results_cloud_wfs_invertido = results_cloud_wfs[::-1]
                                # D4SF-86
                                total_pixeles_nubes = {"total": "yes",
                                                       "porcent": results_cloud_wfs_invertido[idx]['properties'][
                                                           'cloudCoverNpEncoder.percentage']}
                            else:
                                total_pixeles_nubes = {"total": "n/a",
                                                       "porcent": "n/a"}
                            # ESTABLECEMOS EL RESULTADO
                            id_json = id_parcela + '_' + str(idx)
                            arrResult = {
                                id_json: {"img": nombreArchivo, "totalPixeles": total_pix_detectados,
                                         "fecha": time.date().isoformat(),
                                         "nombre": nombre_parcela, "area": area, "naranja": total_pixeles_naranja,
                                         "amarillo": total_pixeles_amarillo, "verdes": total_pixeles_verde,
                                         "azul_claro": total_pixeles_a_claro, "azul_medio": total_pixeles_a_medio,
                                         "azul_oscuro": total_pixeles_a_oscuro, "nubes": total_pixeles_nubes}}
                            arrRespuesta.update(arrResult)
                            fechaAnterior = str(time.date().isoformat())
                            validImage = True
                            # log purpuse
                            context_logs['extra_data']['error'] = ''  # clean error
                            context_logs['status'] = 'success'
                            context_logs['message'] = 'Proceso calculo procesarMOISTURE via sup_process'
                            # savelog(context_logs,request)
                            # end log purpuse
                        except Exception as Error:
                            print(Error)
                            file_err = open(settings.PARCEL_FOLDER + "catch_" + nombre_archivo_errores, 'a')
                            file_err.write(id_parcela + " -- Linea 559 - {Error} " + str(Error) + " \n")
                            file_err.close()
                            arrError.append({"nombre_parcela": nombre_parcela, "fecha": time.date().isoformat(),
                                             "error": str(Error)})
                            # log
                            context_logs['extra_data']['error'] = str(Error)
                            context_logs['extra_data']['id_parcela'] = id_parcela
                            context_logs['status'] = 'error'
                            context_logs['message'] = 'Error calculos en procesarMOISTURE via sup_process Imagenes'
                            # savelog(context_logs,request)

                # Termina el for de las imagenes / Eliminado de los errores si se ha llegado a procesar la imagen
                for error in arrError:
                    print(nombre_parcela)
                    print(validImage)
                    print(error)

                    file_err = open(settings.PARCEL_FOLDER + nombre_archivo_errores, 'a')
                    file_err.write('------------ERROR---------\n')
                    file_err.write(str(nombre_parcela) + '\n')
                    file_err.write(str(validImage) + '\n')
                    file_err.write(str(error) + '\n')
                    file_err.write('---------------------------\n')
                    file_err.close()

                    if validImage:
                        key = arrError.index(error)
                        arrError.pop(key)

            # Termina el for de las parcelas
            db_informe.save(
                nombre=nombre,
                capa=capa,
                fechaInicio=fecha_inicio,
                fechaFin=fecha_fin,
                enterprise_id=enterprise_id,
                esCooperative=es_cooperative,
                id_parcelas=cadena_parcelas,
                includeClouds=include_clouds,
                user_created=sub_uid,
                estado=2
            )
            app_json = json.dumps(arrRespuesta, cls=NpEncoder)
            # Creación del Json
            nombreJson = str(uuid.uuid1().int) + '.json'
            file = open(settings.PARCEL_FOLDER + nombreJson, 'w')
            file.write(app_json)
            file.close()
            # Odenacion del Json por fechas por si tiene varias parcelas
            arrPandasDf = []
            jsons = pd.read_json(settings.PARCEL_FOLDER + nombreJson)
            arrPandasDf.append(jsons)
            arrRespuesta = []
            for dataFrame in arrPandasDf:
                for dictt in dataFrame.to_dict():
                    arrRespuesta.append(dataFrame.to_dict().get(dictt))
            df = pd.DataFrame(arrRespuesta)
            try:
                # valid if df is empty
                if df.empty:
                    dfSort = df
                else:
                    dfSort = df.sort_values('fecha', ascending=True)
                    dfSort.index = range(len(dfSort.index))
                    dfSort.transpose().to_json(settings.PARCEL_FOLDER + 'order_' + nombreJson)

                    # HACEMOS EL FICHERO xls
                    nombreXlsx = str(uuid.uuid1().int) + '.xlsx'
                    json2xlsx('order_' + nombreJson, nombreXlsx, capa)
                # check if file exists
                if os.path.isfile(settings.PARCEL_FOLDER + nombreXlsx):
                    file_exists = True
                    context_logs['status'] = 'success'
                    context_logs['file'] = settings.PARCEL_FOLDER + 'order_' + nombreJson
                    context_logs['extra_data']['nombreXlsx'] = nombreXlsx
                    context_logs['message'] = 'creado archivo .xlsx via sup_process'
                    # savelog(context_logs,request)
                    # log purpuse



            except Exception as Error:
                file_exists = False
                file_err = open(settings.PARCEL_FOLDER + nombre_archivo_errores, 'a')
                file_err.write(str(Error) + '\n')
                file_err.close()
                file_err = open(settings.PARCEL_FOLDER + "catch_" + nombre_archivo_errores, 'a')
                file_err.write(id_parcela + " -- Linea 611 - {Error} " + str(Error) + " \n")
                file_err.close()
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': sub_name_user
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
                    [sub_email_user],  # ['soported4sf@smartbits.es']
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                isSendEmailForEnterprise = msg.send()
                # MAIL PARA NOSOTROS CON DETALLE DEL ERROR
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': sub_name_user,
                    'email_user': sub_email_user,
                    'parcelas': id_parcelas,
                    'capa': capa,
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'parcels_err': arrError,
                    'error_no_completado': str(Error)
                }
                # ENVIO DE CORREO OK
                title = "=?utf-8?Q?=F0=9F=91=B7_Error_total_informe?="
                email_html_message_enterprise = render_to_string('Informe_solicitud_adm_error.html', context)
                # ENVIAMOS EL MAIL
                msg = EmailMultiAlternatives(
                    # title:
                    title,
                    # message:
                    email_html_message_enterprise,
                    # from:
                    "D4SmartFarming <soporte@d4smartfarming.com>",
                    # to:
                    ['soported4sf@smartbits.es'],
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                isSendEmailForEnterpriseTotalInforme = msg.send()
                # log
                context_logs['extra_data']['error'] = str(Error)
                context_logs['extra_data']['isSendEmailForEnterprise'] = isSendEmailForEnterprise
                context_logs['extra_data']['isSendEmailForEnterpriseTotalInforme'] = isSendEmailForEnterpriseTotalInforme
                context_logs['status'] = 'error'
                context_logs['message'] = 'Envio correo errores procesarMOISTURE via sup_process'
                # savelog(context_logs,request)

                exit()

            if sub_serializer.save(
                    nombre=nombre,
                    capa=capa,
                    fechaInicio=fecha_inicio,
                    fechaFin=fecha_fin,
                    enterprise_id=enterprise_id,
                    esCooperative=es_cooperative,
                    jsonFile=nombreJson,
                    xlsxFile=nombreXlsx,
                    id_parcelas='',
                    includeClouds=include_clouds,
                    user_created=sub_uid,
                    estado=3,
                    error=not file_exists,  # TODO: check not file_exists
                    parcelas_fallidas=fallidas) and file_exists:
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': sub_name_user,
                    # 'img_plot': my_string,
                    'parcels_err': arrError
                }
                # ENVIO DE CORREO OK
                title = "=?utf-8?Q?=F0=9F=93=8B_Informe_generado_Correctamente?="
                email_html_message_enterprise = render_to_string('Informe_generado_correctamente.html', context)
                # ENVIAMOS EL MAIL
                msg = EmailMultiAlternatives(
                    # title:
                    title,
                    # message:
                    email_html_message_enterprise,
                    # from:
                    "D4SmartFarming <soporte@d4smartfarming.com>",
                    # to:
                    [sub_email_user],  # ['soported4sf@smartbits.es']
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_file(settings.PARCEL_FOLDER + nombreXlsx)

                msg.attach_alternative(email_html_message_enterprise, "text/html")
                IsSendEmailGenerateSuccess = msg.send()
                # MAIL PARA NOSOTROS CON DETALLE DEL ERROR
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': sub_name_user,
                    'email_user': sub_email_user,
                    'parcelas': id_parcelas,
                    'capa': capa,
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'parcels_err': arrError,
                }
                # ENVIO DE CORREO OK
                title = "=?utf-8?Q?=F0=9F=91=B7_Informe_generado_Correctamente?="
                email_html_message_enterprise = render_to_string('Informe_solicitud_adm_final_proceso.html', context)
                # ENVIAMOS EL MAIL
                msg = EmailMultiAlternatives(
                    # title:
                    title,
                    # message:
                    email_html_message_enterprise,
                    # from:
                    "D4SmartFarming <soporte@d4smartfarming.com>",
                    # to:
                    ['soported4sf@smartbits.es'],
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                IsSendEmailGenerateSuccessEnterprise = msg.send()

                # log purpuse
                context_logs['status'] = 'success'
                context_logs['extra_data']['IsSendEmailGenerateSuccessEnterprise'] = IsSendEmailGenerateSuccessEnterprise
                context_logs['extra_data']['IsSendEmailGenerateSuccess'] = IsSendEmailGenerateSuccess
                context_logs['message'] = 'Guardado de imagenes db  procesarMOISTURE via sup_process'
                # savelog(context_logs,request)
                # end log purpuse
            else:
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': sub_name_user
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
                    [sub_email_user],  # ['soported4sf@smartbits.es']
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                Informe_generado_error = msg.send()
                # MAIL PARA NOSOTROS CON DETALLE DEL ERROR
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': sub_name_user,
                    'email_user': sub_email_user,
                    'parcelas': id_parcelas,
                    'capa': capa,
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'parcels_err': arrError,
                    'error_no_completado': "ERROR EN EL GUARDADO"
                }
                # ENVIO DE CORREO OK
                title = "=?utf-8?Q?=F0=9F=91=B7_Error_total_informe?="
                email_html_message_enterprise = render_to_string('Informe_solicitud_adm_error.html', context)
                # ENVIAMOS EL MAIL
                msg = EmailMultiAlternatives(
                    # title:
                    title,
                    # message:
                    email_html_message_enterprise,
                    # from:
                    "D4SmartFarming <soporte@d4smartfarming.com>",
                    # to:
                    ['soported4sf@smartbits.es'],
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                informe_solicitud_adm = msg.send()
                # log

                context_logs['extra_data']['informe_solicitud_adm'] = informe_solicitud_adm
                context_logs['extra_data']['Informe_generado_error'] = Informe_generado_error
                context_logs['status'] = 'error'
                context_logs['message'] = 'Envio correo errores Error_total_informe procesarMOISTURE via sup_process'
                # savelog(context_logs,request)

        except Exception as Error:
            context_logs['extra_data']['error'] = str(Error)
            context_logs['extra_data']['file_exists'] = str(file_exists)
            context_logs['status'] = 'error'
            context_logs['message'] = 'Error runtime procesarMOISTURE via sup_process'
            # savelog(context_logs,request)

            file_err = open(settings.PARCEL_FOLDER + "catch_" + nombre_archivo_errores, 'a')
            file_err.write(id_parcela + " -- Linea 806 - {Error} " + str(Error) + " \n")
            file_err.close()

            # if file_exists is false
            if not file_exists:
                db_informe.save(
                    nombre=nombre,
                    capa=capa,
                    fechaInicio=fecha_inicio,
                    fechaFin=fecha_fin,
                    enterprise_id=enterprise_id,
                    esCooperative=es_cooperative,
                    id_parcelas=cadena_parcelas,
                    includeClouds=include_clouds,
                    user_created=sub_uid,
                    estado=4
                )

                # MAIL PARA NOSOTROS CON DETALLE DEL ERROR
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': sub_name_user,
                    'email_user': sub_email_user,
                    'parcelas': id_parcelas,
                    'capa': capa,
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'parcels_err': arrError,
                    'error_no_completado': str(Error)
                }
                # ENVIO DE CORREO OK
                title = "=?utf-8?Q?=F0=9F=91=B7_Error_total_informe?="
                email_html_message_enterprise = render_to_string('Informe_solicitud_adm_error.html', context)
                # ENVIAMOS EL MAIL
                msg = EmailMultiAlternatives(
                    # title:
                    title,
                    # message:
                    email_html_message_enterprise,
                    # from:
                    "D4SmartFarming <soporte@d4smartfarming.com>",
                    # to:
                    ['soported4sf@smartbits.es'],
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                informe_solicitud_adm_error = msg.send()
                context_logs['message'] = 'Error runtime procesarMOISTURE via sup_process'
                context_logs['extra_data']['informe_solicitud_adm_error'] = informe_solicitud_adm_error
                # savelog(context_logs,request)

    thread = Thread(target=sup_process,
                    kwargs=dict(serializer=serializer, email_user=email_user, name_user=name_user, uid=uid,
                                request=request))
    thread.start()
