import os
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from moisturemonitor.jsontoexcel import json2xlsx
from moisturemonitor.serializer import MoistureMonitor
from moisturemonitor.serializer import MoistureMonitorModelserializer, MoistureMonitorSerializer
from monitor.utils import checkNumberOfImageForReport
from django.conf import settings


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

# Create your views here.
class NdviMonitorViewSet(viewsets.GenericViewSet):

    queryset = MoistureMonitor.objects.all()
    serializer_class = MoistureMonitorModelserializer

    @action(detail=False, methods=['post'])
    def data(self, request):
        finicio = datetime.strptime(request.data["finicio"], '%Y-%m-%d')
        ffin = datetime.strptime(request.data["ffin"], '%Y-%m-%d')
        # Establecemos los dias que hay entre las dos fechas
        arrFechas = pandas.date_range(finicio,ffin).format(formatter=lambda x: x.strftime('%Y-%m-%d'))
        data = {}
        for fecha in arrFechas:
            # D4SF-87
            queryset = MoistureMonitor.objects.filter(date = fecha, parcel__in=request.data["parcels"]).order_by('-modified').all()
            arrResultados = []
            if len(queryset):
                # D4SF-85
                parcel_group = []
                for result in queryset:
                    # D4SF-85
                    #arrResultados.append(MoistureMonitorModelserializer(result).data)
                    if result.parcel not in parcel_group:
                        arrResultados.append(MoistureMonitorModelserializer(result).data)
                        parcel_group.append(result.parcel)
                data[fecha] = {"resultado": arrResultados}

        return Response(data, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get', 'post'])
    def parcelas(self, request):
        
        def supProcess():
            master_url = "http://127.0.0.1:8000" # https://api-d4sf.smartbits-es.com
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
                    'capa': 'MOISTURE',
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
                    users_to, # soported4sf@smartbits.es
                    # BCC
                    ['backups@smartbits.es'] # 'rebeca.espana@smartbits.es'
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                msg.send() # todo: uncomment in prod
                
                
                config = SHConfig()
                if settings.CLIENT_ID and settings.CLIENT_SECRET:
                    config.sh_client_id = settings.CLIENT_ID
                    config.sh_client_secret = settings.CLIENT_SECRET
                    config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
                arrError = []
                for parcela in parcelas["data"]:
                    try:
                        if config.instance_id == '':
                            print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")
                        
                        bbox = BBox(bbox=parcela["polygon.extent"], crs=CRS.WGS84)
                        # Capa Ndvi
                        wms_ndvi_request = WcsRequest(
                            data_collection=DataCollection.SENTINEL2_L1C,
                            layer='MOISTURE_INDEX',
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

                        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        print("id de la Parcela: "+str(parcela["id"]))
                        print("Nombre de la Parcela: "+str(parcela["name"]))
                        print("wms_ndvi_request.get_dates: ",wms_ndvi_request.get_dates())
                        print("images: ",len(images))
                        print("fecha: ",str(finicio))
                        print("fecha_fin: ",str(ffin))
                        print("fechaAnterior",str(fechaAnterior))
                        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                        for idx, (image, time) in enumerate(zip(images, wms_ndvi_request.get_dates())):
                            print("----------------------")
                            print("Nombre de la Parcela: "+parcela["name"])
                            print(time.date())
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
                                    image2 = cv2.imread("media/parcels/" + nombreArchivo, cv2.IMREAD_UNCHANGED)
                                    img = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
                                    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
                                    #ROJO/NARANJAS
                                    ligth_green = (1, 255, 0)
                                    dark_green = (25, 255, 255)
                                    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    mask_rojo = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    unique, counts = np.unique(mask, return_counts=True)
                                    pixeles_naranjas = getPixeles(np.asarray((unique, counts)).T)
                                    #AMARILLOS
                                    ligth_green = (26, 255, 0)
                                    dark_green = (50, 255, 255)
                                    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    mask_amarillos = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    unique, counts = np.unique(mask, return_counts=True)
                                    pixeles_amarillos = getPixeles(np.asarray((unique, counts)).T)
                                    #VERDES
                                    ligth_green = (31, 0, 0)
                                    dark_green = (50, 255, 255)
                                    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    mask_verdes = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    unique, counts = np.unique(mask, return_counts=True)
                                    pixeles_verdes = getPixeles(np.asarray((unique, counts)).T)
                                    #AZULES CLARITOS
                                    ligth_green = (51, 255, 0)
                                    dark_green = (100, 255, 255)
                                    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    mask_azules_claro = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    unique, counts = np.unique(mask, return_counts=True)
                                    pixeles_a_claro = getPixeles(np.asarray((unique, counts)).T)
                                    #AZULES MEDIOS
                                    ligth_green = (101, 255, 0)
                                    dark_green = (115, 255, 255)
                                    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    mask_azules_medios = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    unique, counts = np.unique(mask, return_counts=True)
                                    pixeles_a_medio = getPixeles(np.asarray((unique, counts)).T)
                                    #AZULES OSCURO
                                    ligth_green = (116, 255, 0)
                                    dark_green = (200, 255, 255)
                                    mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    mask_azules_oscuros = cv2.inRange(img_hsv, ligth_green, dark_green)
                                    unique, counts = np.unique(mask, return_counts=True)
                                    pixeles_a_oscuro = getPixeles(np.asarray((unique, counts)).T)

                                    # UNIONES DE MASCARAS
                                    mask_union = cv2.bitwise_or(mask_rojo, mask_amarillos)
                                    mask_union2 = cv2.bitwise_or(mask_union, mask_verdes)
                                    mask_union3 = cv2.bitwise_or(mask_union2, mask_azules_claro)
                                    mask_union4 = cv2.bitwise_or(mask_union3, mask_azules_medios)
                                    mask_union5 = cv2.bitwise_or(mask_union4, mask_azules_oscuros)
                                    unique, counts = np.unique(mask_union5, return_counts=True)
                                    arr_total = np.asarray((unique, counts)).T
                                    # UNION TOTALES
                                    # warning: si no hay pixeles en la imagen, no se puede calcular el porcentaje
                                    print("UNION TOTALES: arr_total: ",arr_total)
                                    total_pixeles = 0
                                    # D4SF-87
                                    ifvalidImage = False
                                    if len(arr_total) >= 2:
                                        total_pixeles = arr_total[1][1]
                                        ifvalidImage = True
                                    else:
                                        ifvalidImage = False   
                                        
                                    print("UNION TOTALES: total_pixeles: ",total_pixeles)   
                                    # FIN CALCULOS /*******************************************************************
                                    totalPixDetectados = sum([pixeles_naranjas, pixeles_amarillos, pixeles_verdes, pixeles_a_claro, pixeles_a_medio, pixeles_a_oscuro])
                                    # Nubes
                                    results_cloud_wfs_invertido = results_cloud_wfs[::-1]
                                    data = {
                                        'parcel': parcela["id"],
                                        'name': parcela["name"],

                                        # Naranja
                                        'pix_naranja_total': pixeles_naranjas,
                                        'pix_naranja_porcent': percentage(pixeles_naranjas, totalPixDetectados),
                                        'pix_naranja_area_porcent': (percentage(pixeles_naranjas, totalPixDetectados) * parcela["area"] / 100),

                                        # Amarillo
                                        'pix_amarillo_total': pixeles_amarillos,
                                        'pix_amarillo_porcent': percentage(pixeles_amarillos, totalPixDetectados),
                                        'pix_amarillo_area_porcent': (percentage(pixeles_amarillos, totalPixDetectados) * parcela["area"] / 100),

                                        # Verde
                                        'pix_verde_total': pixeles_verdes,
                                        'pix_verde_porcent': percentage(pixeles_verdes, totalPixDetectados),
                                        'pix_verde_area_porcent': (percentage(pixeles_verdes, totalPixDetectados) * parcela["area"] / 100),

                                        # Azul Claro
                                        'pix_azul_claro_total': pixeles_a_claro,
                                        'pix_azul_claro_porcent': percentage(pixeles_a_claro, totalPixDetectados),
                                        'pix_azul_claro_area_porcent': (percentage(pixeles_a_claro, totalPixDetectados) * parcela["area"] / 100),

                                        # Azul medio
                                        'pix_azul_medio_total': pixeles_a_medio,
                                        'pix_azul_medio_porcent': percentage(pixeles_a_medio, totalPixDetectados),
                                        'pix_azul_medio_area_porcent': (percentage(pixeles_a_medio, totalPixDetectados) * parcela["area"] / 100),

                                        # Azul oscuro
                                        'pix_azul_oscuro_total': pixeles_a_oscuro,
                                        'pix_azul_oscuro_porcent': percentage(pixeles_a_oscuro, totalPixDetectados),
                                        'pix_azul_oscuro_area_porcent': (percentage(pixeles_a_oscuro, totalPixDetectados) * parcela["area"] / 100),

                                        #NUBES

                                        'nubes_porcent': results_cloud_wfs_invertido[idx]['properties']['cloudCoverPercentage'],

                                        'image': 'media/parcels/' + nombreArchivo,
                                        'nubesImage': 'media/parcels/cloud_' + nombreArchivo,
                                        'trueColorImage': 'media/parcels/trueColor_' + nombreArchivo,
                                        'date': time.date().isoformat()
                                    }

                                    # D4SF-85 si no existe el registro se crea 
                                    isMoistureMonitorRecord = MoistureMonitor.objects.filter(
                                        parcel=parcela["id"], 
                                        image= 'media/parcels/' + nombreArchivo,
                                        nubesImage= 'media/parcels/cloud_' + nombreArchivo,
                                        trueColorImage= 'media/parcels/trueColor_' + nombreArchivo,
                                        date=time.date().isoformat(),
                                        ).count()
                                    print("isMoistureMonitorRecord: "+str(isMoistureMonitorRecord))
                                    if isMoistureMonitorRecord == 0:
                                        serializer = MoistureMonitorSerializer(data=data)
                                        serializer.is_valid(raise_exception=True)
                                        # D4SF-87
                                        if ifvalidImage:
                                            print("**********Registro creado***********")
                                            print('media/parcels/' + nombreArchivo)
                                            serializer.save()
                                        else:
                                            print("**********Eliminando image***********")
                                            print('media/parcels/' + nombreArchivo)
                                            # delete image
                                            os.remove('media/parcels/' + nombreArchivo) 
                                            os.remove('media/parcels/cloud_' + nombreArchivo)
                                            os.remove('media/parcels/trueColor_' + nombreArchivo) 
                                    else:
                                        print("**********Registro ya existe***********")
                                    
                                    # D4SF-87
                                    if ifvalidImage:
                                        fechaAnterior = str(time.date().isoformat())
                                    else:
                                        fechaAnterior = "0"
                                    """
                                    serializer = MoistureMonitorSerializer(data=data)
                                    serializer.is_valid(raise_exception=True)
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
                        arrError.append("Error: "+parcela["name"]+" fecha "+str(time.date().isoformat())+" error: "+str(Error)+"\n")
                # Envío Mail Fin proceso
                site_shortcut_name = 'Data4SmartFarming'
                listToStr = ' '.join(map(str, arrError))
                context = {
                    'site_name': site_shortcut_name,
                     'enterprise_name': enterprise_name,
                    'capa': 'MOISTURE',
                    'fecha': str(finicio),
                    'fecha_fin': str(ffin),
                    'empresa' : enterprise_id,
                    'parcelas' : parcels,
                    'errors': listToStr
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
                    users_to, # soported4sf@smartbits.es
                    # TODO:change in prod BCC 
                    ['backups@smartbits.es'] # 'rebeca.espana@smartbits.es'
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                msg.send() # todo: uncomment in prod
                print("**********Fin del proceso***********")
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
            return Response({"data": nombreArchivo,'error': emailRequest,'isSendEmail':isSendEmail}, status=status.HTTP_200_OK)
        except NameError:
            print("send email")
            errorInReport = True
            message = "Hemos detectado un error, procedemos a enviar un email" + NameError

        
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
            #isSendEmail = msg.send()
            

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
                queryset = MoistureMonitor.objects.filter(date = fecha, parcel=parcela).all()
                if len(queryset):
                    for result in queryset:
                        arrResultados.append(MoistureMonitorModelserializer(result).data)
                    data[parcela] = {"resultado": arrResultados}
        return Response(data, status=status.HTTP_200_OK)