from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ndvimonitor.jsontoexcel import json2xlsx
from ndvimonitor.models import NdviMonitor
from ndvimonitor.serializer import NdviMonitorSerializer, NdviMonitorModelserializer
from monitor.utils import checkNumberOfImageForReport
from django.conf import settings

import os
import requests
import json

from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox, DataCollection, SentinelHubRequest, \
    bbox_to_dimensions, CustomUrlParam, FisRequest, Geometry, WebFeatureService, SHConfig

import uuid
import cv2
import numpy as np
import pandas
from threading import Thread
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format

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


def getPixeles(arr_mask):
    if len(arr_mask) == 2:
        return arr_mask[1][1]
    else:
        return 0


def percentage(part, whole):
    if part > 0:
        return float(round(100 * float(part) / float(whole), 2))
    else:
        return 0

def get_total_pixeles(arr_total):
    try:
        total_pixeles = arr_total[1][1]
        return total_pixeles
    except (IndexError, TypeError):
        print("Error en get_total_pixeles")
        print("Error: ", arr_total)
        # Si arr_total no tiene el índice [1][1], se devuelve un valor predeterminado
        return 0  # 0 cualquier otro valor que desees utilizar como predeterminado
        
# Create your views here.
class NdviMonitorViewSet(viewsets.GenericViewSet):

    queryset = NdviMonitor.objects.all()
    serializer_class = NdviMonitorModelserializer

    @action(detail=False, methods=['post'])
    def data(self, request):
        finicio = datetime.strptime(request.data["finicio"], '%Y-%m-%d')
        ffin = datetime.strptime(request.data["ffin"], '%Y-%m-%d')
        # Establecemos los dias que hay entre las dos fechas
        arrFechas = pandas.date_range(finicio,ffin).format(formatter=lambda x: x.strftime('%Y-%m-%d'))
        data = {}
        for fecha in arrFechas:
            #queryset = NdviMonitor.objects.filter(date = fecha, parcel__in=request.data["parcels"]).all()
            queryset = NdviMonitor.objects.filter(date = fecha, parcel__in=request.data["parcels"]).order_by('-modified').all()
            arrResultados = []
            if len(queryset):
                # D4SF-85
                parcel_group = []
                for result in queryset:
                    # D4SF-85
                    # arrResultados.append(NdviMonitorModelserializer(result).data)
                    if result.parcel not in parcel_group:
                        arrResultados.append(NdviMonitorModelserializer(result).data)
                        parcel_group.append(result.parcel)
                data[fecha] = {"resultado": arrResultados}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get', 'post'])
    def parcelas(self, request):
        
        def supProcess():
            master_url = "https://api-d4sf.smartbits-es.com" # https://api-d4sf.smartbits-es.com - http://127.0.0.1:8000/
            url = "{0}/api/v1.0/signin/".format(master_url)
            
            user_email = False
            if "email" in request.data:
                user_email = request.data["email"]

            users_to = ['soported4sf@smartbits.es']
            if user_email:
                users_to.append(user_email)
                
            # D4SF-88
            continent = request.GET.get("continent", False) 

            if "finicio" in request.data:
                finicio = datetime.strptime(request.data["finicio"], '%Y-%m-%d').date()
                ffin = datetime.strptime(request.data["ffin"], '%Y-%m-%d').date()
                enterprise_id = request.data["enterprise"]
                parcels = request.data["parcels"]
            else:
                print("*****************else***************")
                dt = datetime.now() - timedelta(days=1)
                df = DateFormat(dt).format('Y-m-d')
                finicio = df
                ffin = df
                enterprise_id = ""
                parcels = ""
            
            print("***********set date************")
            print("finicio: ", finicio)
            print("ffin: ", ffin)
            print("***********set date************")
            payload = json.dumps({
            "email": "rebeca.espana@smartbits.es",
            "password": "SMB2023#"
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            responsejson = response.json()
            token = responsejson["token"]
            if token:
                # D4SF-88
                if continent:
                    url = '{0}/api/v1.0/parcelasNoAuth/?continent={1}'.format(master_url,continent)
                else:
                    url = "{0}/api/v1.0/parcelasNoAuth/".format(master_url)

                print("url: ", url)
                
                payload = json.dumps({
                "token": token,
                "enterprise_id" : enterprise_id,
                "parcels" : parcels
                })
                headers = {
                'Authorization': 'Bearer '+token,
                'Content-Type': 'application/json'
                }

                response = requests.request("GET", url, headers=headers, data=payload)
                parcelas = response.json()
                print("parcelas: ", len(parcelas))
                # get the instance enterprises
                enterprise_name = ""
                if enterprise_id != "":
                    url_enterprise = "{0}/api/v1.0/enterprises/{1}".format(master_url,enterprise_id)
                    enterprise = requests.request("GET", url_enterprise, headers=headers)
                    enterprise_response = enterprise.json()
                    if 'name' in enterprise_response:
                        enterprise_name = enterprise_response['name']
                
                # Envío Mail Inicio proceso
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'enterprise_name': enterprise_name,
                    'capa': 'NDVI',
                    'fecha': str(finicio),
                    'fecha_fin': str(ffin),
                    'empresa' : enterprise_id,
                    'parcelas' : parcels,
                    'continent': continent
                }
                title = "=?utf-8?Q?=F0=9F=91=B7_Inicio Procesado datos?="
                email_html_message_enterprise = render_to_string('Informe_solicitud_adm_empezar.html', context)
                
                 

                msg = EmailMultiAlternatives(
                    # title:
                    title,
                    # message:
                    email_html_message_enterprise,
                    # from:
                    "D4SmartFarming <soporte@d4smartfarming.com>",
                    # to:
                    users_to, # 
                    # BCC
                    ['backups@smartbits.es'] # 'rebeca.espana@smartbits.es'
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                #msg.send()
                
                config = SHConfig()
                if settings.CLIENT_ID and settings.CLIENT_SECRET:
                    config.sh_client_id = settings.CLIENT_ID
                    config.sh_client_secret = settings.CLIENT_SECRET
                    config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
                arrError = []
                config = SHConfig()
                if settings.CLIENT_ID and settings.CLIENT_SECRET:
                    config.sh_client_id = settings.CLIENT_ID
                    config.sh_client_secret = settings.CLIENT_SECRET
                    config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
                arrError = []
                
                print("init process : ",len(parcelas["data"]))
                print("fecha de inicio : ",finicio)
                print("fecha de fin : ",ffin)

                for parcela in parcelas["data"]:
                    try:
                        print("Nombre de la Parcela: "+parcela["name"])
                         
                        if config.instance_id == '':
                            print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")
                        
                        bbox = BBox(bbox=parcela["polygon.extent"], crs=CRS.WGS84)
                        # Capa Ndvi
                        wms_ndvi_request = WcsRequest(
                            data_collection=DataCollection.SENTINEL2_L1C,
                            layer='NDVI',
                            bbox=bbox,
                            time=(str(finicio), str(ffin)),
                            resx='1m',
                            resy='1m',
                            custom_url_params={
                                CustomUrlParam.SHOWLOGO: False,
                                CustomUrlParam.GEOMETRY: parcela["geometry_string"]
                            },
                            config=config,
                            image_format=MimeType.PNG
                        )
                        # Capa Nubes
                        wms_true_color_clouds_request = WcsRequest(
                            data_collection=DataCollection.SENTINEL2_L1C,
                            layer='PRUEBAS-NUBES',
                            bbox=bbox,
                            time=(str(finicio), str(ffin)),
                            resx='1m',
                            resy='1m',
                            custom_url_params={
                                CustomUrlParam.SHOWLOGO: False,
                                CustomUrlParam.GEOMETRY:  parcela["geometry_string"]
                            },
                            config=config,
                            image_format=MimeType.TIFF
                        )
                        images_true_color_cloud = wms_true_color_clouds_request.get_data()

                        # Capa True Color
                        wms_true_color_request = WcsRequest(
                            data_collection=DataCollection.SENTINEL2_L1C,
                            layer='TRUE_COLOR',
                            bbox=bbox,
                            time=(str(finicio), str(ffin)),
                            resx='1m',
                            resy='1m',
                            custom_url_params={
                                CustomUrlParam.SHOWLOGO: False,
                                CustomUrlParam.GEOMETRY:  parcela["geometry_string"]
                            },
                            config=config,
                            image_format=MimeType.TIFF
                        )
                        images_true_color = wms_true_color_request.get_data()

                        #Procesado
                        wfs_iterator = WebFeatureService(
                            bbox,
                            (str(finicio), str(ffin)),
                            data_collection=DataCollection.SENTINEL2_L2A,
                            maxcc=100,
                            config=config
                        )
                        results_cloud_wfs = list(wfs_iterator)
                        images = wms_ndvi_request.get_data()
                        fechaAnterior = "0"
                        validImage = False
                        
                        print("+++++++++++++++++++++++++++init++++++++++++++++++++++++++++++++++++")
                        print("id de la Parcela: "+str(parcela["id"]))
                        print("Nombre de la Parcela: "+str(parcela["name"]))
                        print("geometry_string: ",parcela["geometry_string"])
                        print("wms_ndvi_request.get_dates: ",wms_ndvi_request.get_dates())
                        print("wms_ndvi_request.get_url_list: ",wms_ndvi_request.get_url_list())
                        print("images_ndvi: ",len(images))
                        print("wms_true_color_clouds_request.get_dates: ",wms_true_color_clouds_request.get_dates())
                        print("images_true_color_cloud: ",len(images_true_color_cloud))
                        print("wms_true_color_request.get_dates: ",wms_true_color_request.get_dates())
                        print("images_true_color: ",len(images_true_color))
                        print("fecha: ",str(finicio))
                        print("fecha_fin: ",str(ffin))
                        print("fechaAnterior",str(fechaAnterior))
                        print("+++++++++++++++++++++++++++++end++++++++++++++++++++++++++++++++++")
                        
                        for idx, (image, time) in enumerate(zip(images, wms_ndvi_request.get_dates())):
                            print("----------------------")
                            print("Nombre de la Parcela: "+parcela["name"])
                            print("time.date().isoformat(): ",str(time.date().isoformat()))
                            print("fechaAnterior: ",str(fechaAnterior))
                            print(idx)
                            print("----------------------")
                            
                            if str(time.date().isoformat()) != fechaAnterior:
                                try:
                                    nombreArchivo = str(uuid.uuid1().int) + '_' + str(idx) + '_' + str(parcela["id"]) + '.png'
                                    trans_mask = image[:, :, 3] == 0
                                    image[trans_mask] = [255, 255, 255, 255]
                                    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                                    cv2.imwrite('media/parcels/' + nombreArchivo, img)
                                    cv2.imwrite('media/parcels/cloud_' + nombreArchivo, cv2.cvtColor(images_true_color_cloud[idx], cv2.COLOR_BGR2RGB))
                                    cv2.imwrite('media/parcels/trueColor_' + nombreArchivo, cv2.cvtColor(images_true_color[idx], cv2.COLOR_BGR2RGB))

                                    # CALCULOS /*******************************************************************
                                    """
                                    MASCARAS AZULES
                                    """
                                    # TOTAL
                                    mask = cv2.inRange(img, azul_bajos[0], azul_altos[0])
                                    unique, counts = np.unique(mask, return_counts=True)
                                    pixeles_azules = getPixeles(np.asarray((unique, counts)).T)
                                    # ALTOS
                                    mask_azul_altos = cv2.inRange(img, azul_altos[0], azul_altos[1])
                                    unique, counts = np.unique(mask_azul_altos, return_counts=True)
                                    pixeles_azules_altos = getPixeles(np.asarray((unique, counts)).T)
                                    # MEDIOS
                                    mask_azul_medios = cv2.inRange(img, azul_medios[0], azul_medios[1])
                                    unique, counts = np.unique(mask_azul_medios, return_counts=True)
                                    pixeles_azules_medios = getPixeles(np.asarray((unique, counts)).T)
                                    # BAJOS
                                    mask_azul_bajos = cv2.inRange(img, azul_bajos[0], azul_bajos[1])
                                    unique, counts = np.unique(mask_azul_bajos, return_counts=True)
                                    pixeles_azules_bajos = getPixeles(np.asarray((unique, counts)).T)
                                    """
                                    MASCARA AMARILLOS
                                    """
                                    # TOTAL
                                    mask_amarillo = cv2.inRange(img, amarillo_bajos[0], amarillo_altos[0])
                                    unique, counts = np.unique(mask_amarillo, return_counts=True)
                                    pixeles_amarillos = getPixeles(np.asarray((unique, counts)).T)
                                    # alto
                                    mask_amarillo_altos = cv2.inRange(img, amarillo_altos[0], amarillo_altos[1])
                                    unique, counts = np.unique(mask_amarillo_altos, return_counts=True)
                                    pixeles_amarillos_altos = getPixeles(np.asarray((unique, counts)).T)
                                    # MEDIOS
                                    mask_amarillo_medios = cv2.inRange(img, amarillo_medios[0], amarillo_medios[1])
                                    unique, counts = np.unique(mask_amarillo_medios, return_counts=True)
                                    pixeles_amarillos_medios = getPixeles(np.asarray((unique, counts)).T)
                                    # BAJOS
                                    mask_amarillo_bajos = cv2.inRange(img, amarillo_bajos[0], amarillo_bajos[1])
                                    unique, counts = np.unique(mask_amarillo_bajos, return_counts=True)
                                    pixeles_amarillos_bajos = getPixeles(np.asarray((unique, counts)).T)
                                    """
                                    MASCARA rojo
                                    """
                                    # TOTAL
                                    mask_rojo = cv2.inRange(img, rojo_bajos[0], rojo_altos[0])
                                    unique, counts = np.unique(mask_rojo, return_counts=True)
                                    pixeles_rojos = getPixeles(np.asarray((unique, counts)).T)
                                    # alto
                                    mask_rojo_altos = cv2.inRange(img, rojo_altos[0], rojo_altos[1])
                                    unique, counts = np.unique(mask_rojo_altos, return_counts=True)
                                    pixeles_rojos_altos = getPixeles(np.asarray((unique, counts)).T)
                                    # MEDIOS
                                    mask_rojo_medios = cv2.inRange(img, rojo_medios[0], rojo_medios[1])
                                    unique, counts = np.unique(mask_rojo_medios, return_counts=True)
                                    pixeles_rojos_medios = getPixeles(np.asarray((unique, counts)).T)
                                    # BAJOS
                                    mask_rojo_bajos = cv2.inRange(img, rojo_bajos[0], rojo_bajos[1])
                                    unique, counts = np.unique(mask_rojo_bajos, return_counts=True)
                                    pixeles_rojos_bajos = getPixeles(np.asarray((unique, counts)).T)
                                    """
                                    MASCARA VERDES
                                    """
                                    # TOTAL
                                    mask_verde = cv2.inRange(img, verde_medios[0], verde_altos[0])
                                    unique, counts = np.unique(mask_verde, return_counts=True)
                                    pixeles_verdes = getPixeles(np.asarray((unique, counts)).T)
                                    # ALTO
                                    mask_verde_altos = cv2.inRange(img, verde_altos[0], verde_altos[1])
                                    unique, counts = np.unique(mask_verde_altos, return_counts=True)
                                    pixeles_verdes_altos = getPixeles(np.asarray((unique, counts)).T)
                                    # MEDIOS
                                    mask_verde_medios = cv2.inRange(img, verde_medios[0], verde_medios[1])
                                    unique, counts = np.unique(mask_verde_medios, return_counts=True)
                                    pixeles_verdes_medios = getPixeles(np.asarray((unique, counts)).T)
                                    # FIN CALCULOS /*******************************************************************

                                    # UNIONES DE MASCARAS
                                    mask_union = cv2.bitwise_or(mask, mask_amarillo)
                                    mask_union2 = cv2.bitwise_or(mask_union, mask_rojo)
                                    mask_union3 = cv2.bitwise_or(mask_union2, mask_verde)
                                    unique, counts = np.unique(mask_union3, return_counts=True)
                                    arr_total = np.asarray((unique, counts)).T
                                    # UNION TOTALES
                                    ifvalidImage = False
                                    total_pixeles = get_total_pixeles(arr_total)
                                    if total_pixeles != 0:
                                        ifvalidImage = True
                                    else:
                                        ifvalidImage = False   
                                        
                                    print("UNION TOTALES: total_pixeles: ",total_pixeles)
                                        
                                    if ifvalidImage and total_pixeles != 0:
                                        print("************ifvalidImage and total_pixeles != 0****************")
                                        # Nubes
                                        results_cloud_wfs_invertido = results_cloud_wfs[::-1]
                                        data = {
                                            'parcel': parcela["id"],
                                            'name': parcela["name"],

                                            # AZULES
                                            'pix_azul_total': pixeles_azules,
                                            'pix_azul_total_porcent': percentage(pixeles_azules, total_pixeles),#arr_total[1][1]

                                            'pix_azul_altos_total': pixeles_azules_altos,
                                            'pix_azul_altos_porcent': percentage(pixeles_azules_altos, total_pixeles),
                                            'pix_azul_altos_area_porcent': (percentage(pixeles_azules_altos, total_pixeles) * parcela["area"] / 100),

                                            'pix_azul_medios_total': pixeles_azules_medios,
                                            'pix_azul_medios_porcent': percentage(pixeles_azules_medios, total_pixeles),
                                            'pix_azul_medios_area_porcent': (percentage(pixeles_azules_medios, total_pixeles) * parcela["area"] / 100),

                                            'pix_azul_bajos_total': pixeles_azules_bajos,
                                            'pix_azul_bajos_porcent': percentage(pixeles_azules_bajos, total_pixeles),
                                            'pix_azul_bajos_area_porcent': (percentage(pixeles_azules_bajos, total_pixeles) * parcela["area"] / 100),

                                            #AMARILLOS

                                            'pix_amarillo_total': pixeles_amarillos,
                                            'pix_amarillo_total_porcent': percentage(pixeles_amarillos, total_pixeles),#arr_total[1][1]

                                            'pix_amarillo_altos_total': pixeles_amarillos_altos,
                                            'pix_amarillo_altos_porcent': percentage(pixeles_amarillos_altos, total_pixeles),
                                            'pix_amarillo_altos_area_porcent': (percentage(pixeles_amarillos_altos, total_pixeles) * parcela["area"] / 100),

                                            'pix_amarillo_medios_total': pixeles_amarillos_medios,
                                            'pix_amarillo_medios_porcent': percentage(pixeles_amarillos_medios, total_pixeles),
                                            'pix_amarillo_medios_area_porcent': (percentage(pixeles_amarillos_medios, total_pixeles) * parcela["area"] / 100),

                                            'pix_amarillo_bajos_total': pixeles_amarillos_bajos,
                                            'pix_amarillo_bajos_porcent': percentage(pixeles_amarillos_bajos, total_pixeles),
                                            'pix_amarillo_bajos_area_porcent': (percentage(pixeles_amarillos_bajos, total_pixeles) * parcela["area"] / 100),

                                            #ROJOS

                                            'pix_rojo_total': pixeles_rojos,
                                            'pix_rojo_total_porcent': percentage(pixeles_rojos, total_pixeles),#arr_total[1][1]

                                            'pix_rojo_altos_total': pixeles_rojos_altos,
                                            'pix_rojo_altos_porcent': percentage(pixeles_rojos_altos, total_pixeles),
                                            'pix_rojo_altos_area_porcent': (percentage(pixeles_rojos_altos, total_pixeles) * parcela["area"] / 100),

                                            'pix_rojo_medios_total': pixeles_rojos_medios,
                                            'pix_rojo_medios_porcent': percentage(pixeles_rojos_medios, total_pixeles),
                                            'pix_rojo_medios_area_porcent': (percentage(pixeles_rojos_medios, total_pixeles) * parcela["area"] / 100),

                                            'pix_rojo_bajos_total': pixeles_rojos_bajos,
                                            'pix_rojo_bajos_porcent': percentage(pixeles_rojos_bajos, total_pixeles),
                                            'pix_rojo_bajos_area_porcent': (percentage(pixeles_rojos_bajos, total_pixeles) * parcela["area"] / 100),

                                            #VERDES

                                            'pix_verde_total': pixeles_verdes,
                                            'pix_verde_total_porcent': percentage(pixeles_verdes, total_pixeles),#arr_total[1][1]

                                            'pix_verde_altos_total': pixeles_verdes_altos,
                                            'pix_verde_altos_porcent': percentage(pixeles_verdes_altos, total_pixeles),
                                            'pix_verde_altos_area_porcent': (percentage(pixeles_verdes_altos, total_pixeles) * parcela["area"] / 100),

                                            'pix_verde_medios_total': pixeles_verdes_medios,
                                            'pix_verde_medios_porcent': percentage(pixeles_verdes_medios, total_pixeles),
                                            'pix_verde_medios_area_porcent': (percentage(pixeles_verdes_medios, total_pixeles) * parcela["area"] / 100),

                                            #NUBES

                                            'nubes_porcent': results_cloud_wfs_invertido[idx]['properties']['cloudCoverPercentage'],

                                            'image': 'media/parcels/' + nombreArchivo,
                                            'nubesImage': 'media/parcels/cloud_' + nombreArchivo,
                                            'trueColorImage': 'media/parcels/trueColor_' + nombreArchivo,
                                            'date': time.date().isoformat()
                                        }
                                        
                                        # D4SF-85 si no existe el registro se crea 
                                        isNdviMonitorRecord = NdviMonitor.objects.filter(
                                            parcel=parcela["id"], 
                                            image= 'media/parcels/' + nombreArchivo,
                                            nubesImage= 'media/parcels/cloud_' + nombreArchivo,
                                            trueColorImage= 'media/parcels/trueColor_' + nombreArchivo,
                                            date=time.date().isoformat(),
                                        ).count()
                                        
                                        if isNdviMonitorRecord == 0:
                                            serializer = NdviMonitorSerializer(data=data)
                                            serializer.is_valid(raise_exception=True)
                                            # D4SF-87
                                            if ifvalidImage:
                                                serializer.save()
                                                print("**********Registro creado***********")
                                                print(('media/parcels/' + nombreArchivo))
                                            else:
                                                # delete image
                                                os.remove('media/parcels/' + nombreArchivo) 
                                                os.remove('media/parcels/cloud_' + nombreArchivo)
                                                os.remove('media/parcels/trueColor_' + nombreArchivo)   
                                        

                                    # D4SF-87
                                    if ifvalidImage:
                                        fechaAnterior = str(time.date().isoformat())
                                    else:
                                        fechaAnterior = "0"
                                    
                                    
                                    
                                    """
                                    isNdviMonitorRecord = NdviMonitor.objects.filter(parcel=parcela["id"], date=time.date().isoformat()).count()
                                    print("isNdviMonitorRecord: "+str(isNdviMonitorRecord))
                                    if isNdviMonitorRecord == 0:
                                        serializer = NdviMonitorSerializer(data=data)
                                        serializer.is_valid(raise_exception=True)
                                        serializer.save()
                                    else:
                                        print("**********Registro ya existe***********")

                                    fechaAnterior = str(time.date().isoformat())
                                    """
                                    
                                    
                                    """
                                    serializer = NdviMonitorSerializer(data=data)
                                    serializer.is_valid(raise_exception=True)
                                    print("**********serializer.errors***********")
                                    print(serializer.errors)
                                    print("*********************")
                                    serializer.save()
                                    fechaAnterior = str(time.date().isoformat())
                                    """
                                except Exception as Error:
                                    print('Error')
                                    print(str(Error))
                                    arrError.append("Error: "+parcela["name"]+" fecha "+str(time.date().isoformat())+" error: "+str(Error)+"\n")
                            
                    except Exception as Error:
                        print('Error')
                        print(str(Error))
                        arrError.append("Error: "+parcela["name"]+" error: "+str(Error)+"\n")
                        #arrError.append("Error: "+parcela["name"]+" fecha "+str(time.date().isoformat())+" error: "+str(Error)+"\n")
                # Envío Mail Fin proceso
                site_shortcut_name = 'Data4SmartFarming'
                listToStr = ' '.join(map(str, arrError))
                context = {
                    'site_name': site_shortcut_name,
                    'enterprise_name': enterprise_name,
                    'capa': 'NDVI',
                    'fecha': str(finicio),
                    'fecha_fin': str(ffin),
                    'empresa' : enterprise_id,
                    'parcelas' : parcels,
                    'errors': listToStr,
                    'continent': continent
                }
                title = "=?utf-8?Q?=F0=9F=91=B7_Fin Procesado datos?="
                email_html_message_enterprise = render_to_string('Informe_solicitud_adm_fin.html', context)
                msg = EmailMultiAlternatives(
                    # title:
                    title,
                    # message:
                    email_html_message_enterprise,
                    # from:
                    "D4SmartFarming <soporte@d4smartfarming.com>",
                    # to:
                    users_to,
                    ['backups@smartbits.es'] # 'rebeca.espana@smartbits.es'
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                #msg.send()
                print("**********Fin Process***********")
        thread = Thread(target=supProcess)
        thread.start()
        
        return Response({"data": "OK"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def exportexcel(self, request):
        
        errorInReport = False
        isSendEmail = False
        message = ''
        # get data from get request
        isWithImage = request.GET.get('image',False)
        iswithGraphic = request.GET.get('IswithGraphic',False)
        # get data from post request
        dataRequest = request.data['data'] if 'data' in request.data.keys() else request.data
        emailRequest = request.data['email'] if 'email' in request.data.keys() else False
       
        try:
            if isWithImage == 'true':
                numberImages = checkNumberOfImageForReport(parcels= dataRequest)
                if numberImages > 4000:
                    message = "El volumen de información es demasiado grande. Por favor, reduzca el número de parcelas y/o días a procesar"
                    return Response({"message": message,"numberImages": numberImages,'error': errorInReport ,'isSendEmail':isSendEmail}, status=status.HTTP_200_OK)


            nombreArchivo = json2xlsx(dataRequest,isWithImage,iswithGraphic)
            return Response({"data": nombreArchivo,'error': errorInReport,'isSendEmail':isSendEmail}, status=status.HTTP_200_OK)
        except NameError:
            print("send email")
            errorInReport = True
            message = "Hemos detectado un error, procedemos a enviar un email " + NameError

        
        if(errorInReport and emailRequest):
            title = "Reporte Evolución de cultivo (Estatus)"
            email_html_message= render_to_string('Informe_error_solicitud.html')
            msg = EmailMultiAlternatives(
                # title:
                title,
                # message:
                email_html_message,
                # from:
                 "D4SmartFarming <soporte@d4smartfarming.com>",
                # to:
                [emailRequest], # 
                # BCC
                ['backups@smartbits.es']
            )
            msg.attach_alternative(email_html_message, "text/html")
            print("send email")
            isSendEmail = msg.send()
            

        return Response({'error': errorInReport,'message': message,'isSendEmail':isSendEmail}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['GET'])
    def imagenesparainforme(self, request,*args, **kwargs):
        finicio = datetime.strptime(request.data["finicio"], '%Y-%m-%d')
        ffin = datetime.strptime(request.data["ffin"], '%Y-%m-%d')
        # Establecemos los dias que hay entre las dos fechas
        arrFechas = pandas.date_range(finicio,ffin).format(formatter=lambda x: x.strftime('%Y-%m-%d'))
        data = {}
        for parcela in request.data["parcels"]:
            arrResultados = []
            for fecha in arrFechas:
                queryset = NdviMonitor.objects.filter(date = fecha, parcel=parcela).all()
                if len(queryset):
                    for result in queryset:
                        arrResultados.append(NdviMonitorModelserializer(result).data)
                    data[parcela] = {"resultado": arrResultados}
        return Response(data, status=status.HTTP_200_OK)