import os
from datetime import datetime
from django.conf import settings
from sentinelhub import SHConfig
import numpy as np
from matplotlib import cm
import pandas as pd
import cv2
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox, DataCollection, SentinelHubRequest, \
    bbox_to_dimensions, CustomUrlParam, FisRequest, Geometry, WebFeatureService

import uuid
import json
from threading import Thread
from parcelas.models import Parcel
from django.contrib.gis.geos import GEOSGeometry, polygon
import decimal
import pandas as pd
from .jsontoexcel import json2xlsx
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .json2plot import plotMoisture
import base64
from trazas.utils import savelog
import inspect

# Configuracion Sentinel
CLIENT_ID = '33467c23-fada-4405-8a5b-33ee38169273'
CLIENT_SECRET = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'
CLIENT_INSTANCE = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'

# Configuración de colores NDVI
azul_altos = [np.array([255,255,51]), np.array([256,256,51])]
azul_medios = [np.array([204,204,51]), np.array([205,205,51])]
azul_bajos = [np.array([102,102,0]), np.array([103,103,0])]

amarillo_altos = [np.array([51,255,255]), np.array([51,256,256])]
amarillo_medios = [np.array([51,204,204]), np.array([51,205,205])]
amarillo_bajos = [np.array([0,102, 102]), np.array([0,103,103])]

rojo_altos = [np.array([0,0,254]), np.array([0,0,255])]
rojo_medios = [np.array([0,0,154]), np.array([0,0,155])]
rojo_bajos = [np.array([0,0,102]), np.array([0,0,103])]

verde_altos = [np.array([51,255,51]), np.array([52,255,52])]
verde_medios = [np.array([51,204,51]), np.array([52,204,52])]

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
        return float(round(100 * float(part)/float(whole), 2))
    else:
        return 0

def registro_log(texto):
    global NOMBRE_ARCHIVO_GLOBAL
    
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    linea_actual = inspect.currentframe().f_back.f_lineno
    
    if(texto == "separador"):
        texto = "----------------------------------------------------------------"
    
    file = open(NOMBRE_ARCHIVO_GLOBAL, 'a') #Abrimos el archivo en modo anexado
    file.write(ahora + " -- Linea " + str(linea_actual) + " -- " + str(texto) + "\n")
    file.close()
    
    file = open(NOMBRE_ARCHIVO_GLOBAL_OUT, 'a') #Abrimos el archivo en modo anexado
    file.write(ahora + " -- Linea " + str(linea_actual) + " -- " + str(texto) + "\n")
    file.close()
    #print(texto)

NOMBRE_ARCHIVO_GLOBAL = ""
NOMBRE_LOG = ""
NOMBRE_ARCHIVO_GLOBAL_OUT = ""

def procesarMOISTURE(serializer, email_user, name_user, uid,request={}):
    def supProcess(serializer, email_user, name_user, uid,request={}):

        global NOMBRE_ARCHIVO_GLOBAL
        global NOMBRE_ARCHIVO_GLOBAL_OUT
        global NOMBRE_LOG
        
        #Variables que nos llegan en la solicitud
        now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') 
        NOMBRE_LOG = serializer.validated_data['nombre']+"__"+str(now)+'.log'
        NOMBRE_ARCHIVO_GLOBAL = settings.PARCEL_FOLDER + NOMBRE_LOG
        NOMBRE_ARCHIVO_GLOBAL_OUT = settings.RESULTADOS_FLODER + NOMBRE_LOG
        
        cadenaParcelas = ''
        nombre = serializer.validated_data['nombre']
        capa = serializer.validated_data['capa']
        id_parcelas = serializer.validated_data['id_parcelas']
        fechaInicio = serializer.validated_data['fechaInicio']
        fechaFin = serializer.validated_data['fechaFin']
        enterprise_id = serializer.validated_data['enterprise_id']
        esCooperative = serializer.validated_data['esCooperative']
        includeClouds = serializer.validated_data['includeClouds']
        time_interval = (fechaInicio, fechaFin)
        errores=False
        fallidas=""
        
        for id_parcela in id_parcelas:
            parcel = Parcel.objects.get(pk=int(id_parcela))
            cadenaParcelas += str(parcel) + ' -> ' + parcel.name + '\n'
               
        registro_log("Usuario que solicita el informe: " + str(email_user))
        registro_log("Nombre del informe: " + str(nombre))
        registro_log("Enterprise ID: " + str(enterprise_id))
        registro_log("Parcelas: " + str(cadenaParcelas))
        registro_log("Capa: " + str(capa))
        registro_log("Incluir nubes: " + str(includeClouds))
        registro_log("Fecha de inicio: " + str(fechaInicio))
        registro_log("Fecha de fin: " + str(fechaFin))

        
        # flag var to check if file exists
        fileExists = False

       

        #INFORME
        db_informe=serializer
        db_informe.save(
            nombre=nombre, 
            capa=capa, 
            fechaInicio=fechaInicio, 
            fechaFin=fechaFin, 
            enterprise_id=enterprise_id, 
            esCooperative=esCooperative, 
            id_parcelas=cadenaParcelas, 
            includeClouds=includeClouds, 
            user_created=uid, 
            estado=1
        )

        try:
            # Envio de mail PRE (solo para nosotros)
            # CONFIG EMAIL
            site_shortcut_name = 'Data4SmartFarming'
            context = {
                'site_name': site_shortcut_name,
                'nombre_informe': nombre,
                'nombre_user': name_user,
                'email_user': email_user,
                'parcelas': id_parcelas,
                'capa': capa,
                'fecha_inicio': fechaInicio,
                'fecha_fin': fechaFin
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
            msg.send()
            registro_log("Correo enviado a soporte indicando que se ha solicitado un informe")

        except Exception as Error:
            registro_log("{Error} " + str(Error))

        try:
            # Establecemos la configuración con sentinel
            config = SHConfig()
            if CLIENT_ID and CLIENT_SECRET:
                config.sh_client_id = CLIENT_ID
                config.sh_client_secret = CLIENT_SECRET
                config.instance_id = CLIENT_INSTANCE
            if config.instance_id == '':
                registro_log("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")
            else:
                registro_log("config="+str(config))   
           
            registro_log("separador")
            registro_log("separador")
            registro_log("Inicio del proceso de generación de imágenes")
            arrRespuesta = {}
            arrError = []
            for id_parcela in id_parcelas:
                
                # Para almacenar los resultados de cada parcela
                arrResultadoParcela = {}
                
                #Obtenemos los datos de la parcela en base de datos
                parcel = Parcel.objects.get(pk=int(id_parcela))
                nombreParcela = parcel.name
                polygon = GEOSGeometry(parcel.polygon)
                nombreJson = str(id_parcela) + '.json'
                file = open(settings.PARCEL_FOLDER + nombreJson, 'w')
                file.write(polygon.geojson)
                file.close()
                fallidas=""


                geometry_string = str(polygon.wkt)
                #areaCrud = polygon.area
                #area = float(decimal.Context(prec=3).create_decimal(float(str(areaCrud)[:10])))
                area = parcel.area
                bbox = BBox(polygon.extent, crs=CRS.WGS84)
                
                registro_log("separador")
                registro_log("separador")
                registro_log("Parcela: " + nombreParcela)
                registro_log("bbox="+str(bbox))
                registro_log("geometry_string="+str(geometry_string))
                

                # ------------------------- MOISTURE ------------------------
                registro_log("-------- MOISTURE -------")
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
                    registro_log("MOISTURE URLs = "+str(wms_ndvi_request.get_url_list()))
                    
                except Exception as Error:
                    registro_log("{Error} " + str(Error))
                    fallidas+=str(id_parcela)+" "
                    errores=True
                    pass

                # ------------------------- NUBES -------------------------
                if includeClouds:
                    registro_log("--------- NUBES ----------")
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
                    except Exception as Error:
                        registro_log("{Error} " + str(Error))
                        fallidas+=str(id_parcela)+" "
                        errores=True
                        pass

                    try:
                        images_true_color_cloud = wms_true_color_clouds_request.get_data()
                        #registro_log("NUBES request="+str(images_true_color_cloud))
                        registro_log("NUBES URLs = "+str(wms_true_color_clouds_request.get_url_list()))
                            
                    except Exception as Error:
                        registro_log("{Error} " + str(Error))
                        fallidas+=str(id_parcela)+" "
                        errores=True
                        pass
                


                    try:
                        wfs_iterator = WebFeatureService(
                            bbox,
                            time_interval,
                            data_collection=DataCollection.SENTINEL2_L1C,
                            maxcc=100,
                            config=config
                        )

                        results_cloud_wfs = list(wfs_iterator)
                        registro_log("NUBES WFS = "+str(results_cloud_wfs))
                        
                    except Exception as Error:
                        registro_log("{Error} " + str(Error))
                        fallidas+=str(id_parcela)+" "
                        errores=True
                        pass

                # ------------------------- TRUE COLOR -------------------------
                registro_log("-------- TRUE COLOR -------")                                 
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
                    #registro_log("TRUE COLOR request="+str(images_true_color))
                    registro_log("TRUE COLOR URLs = "+str(wms_true_color_request.get_url_list()))
                    
                except Exception as Error:
                    registro_log("{Error} " + str(Error))
                    fallidas+=str(id_parcela)+" "
                    errores=True
                    pass                


                fechaAnterior = "0"
                validImage = False
                registro_log("Recorrinedo imagenes...")
                for idx, (image, time) in enumerate(zip(images, wms_ndvi_request.get_dates())):
                    fechaImagen = str(time.date().isoformat())
                      
                    registro_log("Fecha de la imagen: "+fechaImagen)
                    registro_log("Contador imagenes: "+str(idx))
                  
                    try:
                        nombreArchivo = str(uuid.uuid1().int) + '_' + str(idx) + '_' + id_parcela + '.png'
                        registro_log("Nombre del archivo: "+nombreArchivo)
                        trans_mask = image[:, :, 3] == 0
                        image[trans_mask] = [255, 255, 255, 255]
                        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        cv2.imwrite(settings.PARCEL_FOLDER + nombreArchivo, img)
                        cv2.imwrite(settings.PARCEL_FOLDER + 'trueColor_' + nombreArchivo, cv2.cvtColor(images_true_color[idx], cv2.COLOR_BGR2RGB))

                        if includeClouds:
                            cv2.imwrite(settings.PARCEL_FOLDER + 'cloud_' + nombreArchivo, cv2.cvtColor(images_true_color_cloud[idx], cv2.COLOR_BGR2RGB))
                            
                        registro_log("Calculos...")
                        # CALCULOS /*******************************************************************
                        image2 = cv2.imread(settings.PARCEL_FOLDER + nombreArchivo, cv2.IMREAD_UNCHANGED)
                        img = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
                        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
                        registro_log("Rojo/Naranjas")
                        #ROJO/NARANJAS
                        ligth_green = (1, 255, 0)
                        dark_green = (25, 255, 255)
                        mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                        mask_rojo = cv2.inRange(img_hsv, ligth_green, dark_green)
                        unique, counts = np.unique(mask, return_counts=True)
                        pixeles_naranjas = getPixeles(np.asarray((unique, counts)).T)
                        #AMARILLOS
                        registro_log("Amarillos")
                        ligth_green = (26, 255, 0)
                        dark_green = (50, 255, 255)
                        mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                        mask_amarillos = cv2.inRange(img_hsv, ligth_green, dark_green)
                        unique, counts = np.unique(mask, return_counts=True)
                        pixeles_amarillos = getPixeles(np.asarray((unique, counts)).T)
                        #VERDES
                        registro_log("Verdes")
                        ligth_green = (31, 0, 0)
                        dark_green = (50, 255, 255)
                        mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                        mask_verdes = cv2.inRange(img_hsv, ligth_green, dark_green)
                        unique, counts = np.unique(mask, return_counts=True)
                        pixeles_verdes = getPixeles(np.asarray((unique, counts)).T)
                        #AZULES CLARITOS
                        registro_log("Azules claros")
                        ligth_green = (51, 255, 0)
                        dark_green = (100, 255, 255)
                        mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                        mask_azules_claro = cv2.inRange(img_hsv, ligth_green, dark_green)
                        unique, counts = np.unique(mask, return_counts=True)
                        pixeles_a_claro = getPixeles(np.asarray((unique, counts)).T)
                        #AZULES MEDIOS
                        registro_log("Azules medios")
                        ligth_green = (101, 255, 0)
                        dark_green = (115, 255, 255)
                        mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                        mask_azules_medios = cv2.inRange(img_hsv, ligth_green, dark_green)
                        unique, counts = np.unique(mask, return_counts=True)
                        pixeles_a_medio = getPixeles(np.asarray((unique, counts)).T)
                        #AZULES OSCURO
                        registro_log("Azules oscuros")
                        ligth_green = (116, 255, 0)
                        dark_green = (200, 255, 255)
                        mask = cv2.inRange(img_hsv, ligth_green, dark_green)
                        mask_azules_oscuros = cv2.inRange(img_hsv, ligth_green, dark_green)
                        unique, counts = np.unique(mask, return_counts=True)
                        pixeles_a_oscuro = getPixeles(np.asarray((unique, counts)).T)

                        # UNIONES DE MASCARAS
                        registro_log("Uniones mascaras totales")   
                        mask_union = cv2.bitwise_or(mask_rojo, mask_amarillos)
                        mask_union2 = cv2.bitwise_or(mask_union, mask_verdes)
                        mask_union3 = cv2.bitwise_or(mask_union2, mask_azules_claro)
                        mask_union4 = cv2.bitwise_or(mask_union3, mask_azules_medios)
                        mask_union5 = cv2.bitwise_or(mask_union4, mask_azules_oscuros)
                        unique, counts = np.unique(mask_union5, return_counts=True)
                        arr_total = np.asarray((unique, counts)).T
                        #si existe arr_total[1][1] es que hay pixeles
                        # if len(arr_total) > 1:
                        #     total_pixeles = arr_total[1][1]
                        # else:
                        #     total_pixeles = 0
                        # FIN CALCULOS /*******************************************************************

                        totalPixDetectados = sum(
                            [pixeles_naranjas, pixeles_amarillos, pixeles_verdes, pixeles_a_claro, pixeles_a_medio,
                            pixeles_a_oscuro])
                        total_pixeles_naranja = {"total": pixeles_naranjas,
                                                "porcent": percentage(pixeles_naranjas, totalPixDetectados), "area_porcent": (
                                        percentage(pixeles_naranjas, totalPixDetectados) * area / 100)}
                        registro_log("Uniones mascaras totales nanaranja")
                        total_pixeles_amarillo = {"total": pixeles_amarillos,
                                                "porcent": percentage(pixeles_amarillos, totalPixDetectados),
                                                "area_porcent": (
                                                            percentage(pixeles_amarillos, totalPixDetectados) * area / 100)}
                        registro_log("Uniones mascaras totales amarillo")
                        total_pixeles_verde = {"total": pixeles_verdes,
                                            "porcent": percentage(pixeles_verdes, totalPixDetectados),
                                            "area_porcent": (percentage(pixeles_verdes, totalPixDetectados) * area / 100)}
                        registro_log("Uniones mascaras totales verde")
                        total_pixeles_a_claro = {"total": pixeles_a_claro,
                                                "porcent": percentage(pixeles_a_claro, totalPixDetectados),
                                                "area_porcent": (percentage(pixeles_a_claro, totalPixDetectados) * area / 100)}
                        registro_log("Uniones mascaras totales azul claro")
                        total_pixeles_a_medio = {"total": pixeles_a_medio,
                                                "porcent": percentage(pixeles_a_medio, totalPixDetectados),
                                                "area_porcent": (percentage(pixeles_a_medio, totalPixDetectados) * area / 100)}
                        registro_log("Uniones mascaras totales azul medio")
                        total_pixeles_a_oscuro = {"total": pixeles_a_oscuro,
                                                "porcent": percentage(pixeles_a_oscuro, totalPixDetectados), "area_porcent": (
                                        percentage(pixeles_a_oscuro, totalPixDetectados) * area / 100)}
                        registro_log("Uniones mascaras totales azul oscuro")
                        
                        # UNION TOTALES
                        if includeClouds:
                            results_cloud_wfs_invertido = results_cloud_wfs[::-1]
                            # D4SF-86
                            total_pixeles_nubes = {"total": "yes", "porcent": results_cloud_wfs_invertido[idx]['properties']['cloudCoverPercentage']}
                        else:
                            total_pixeles_nubes = {"total": "n/a",
                                                "porcent": "n/a"}
                        # ESTABLECEMOS EL RESULTADO
                        idJson = id_parcela+'_'+str(idx)
                        arrResult = {
                            idJson: {"img": nombreArchivo, "totalPixeles": totalPixDetectados, "fecha": fechaImagen,
                                    "nombre": nombreParcela, "area": area, "naranja": total_pixeles_naranja,
                                    "amarillo": total_pixeles_amarillo, "verdes": total_pixeles_verde,
                                    "azul_claro": total_pixeles_a_claro, "azul_medio": total_pixeles_a_medio,
                                    "azul_oscuro": total_pixeles_a_oscuro, "nubes": total_pixeles_nubes}}
                        registro_log("Resultado: "+str(arrResult))
                        fechaAnterior = fechaImagen
                        validImage = True
                        
                    except Exception as Error:
                            registro_log("{Error} " + str(Error))
                            arrError.append({"nombre_parcela": nombreParcela, "fecha": fechaImagen, "error": str(Error)})
                            
                    actualizaResultado = False
                    fechaTexto = str(fechaImagen)
                    if fechaTexto in arrResultadoParcela:
                        if int(totalPixDetectados) > int(arrResultadoParcela[fechaTexto]["totalPixeles"]):
                            actualizaResultado = True
                    else:
                        actualizaResultado = True
                    

                    if actualizaResultado:
                        arrResultadoParcela[fechaTexto] = {"resultado": arrResult, "totalPixeles": totalPixDetectados}
                    else:
                        registro_log("Hay otra imagen para el mismo día con más pixeles")
                                    
                # Termina el for de las imagenes / Eliminado de los errores si se ha llegado a procesar la imagen
                for error in arrError:
                    if validImage:
                        key = arrError.index(error)
                        arrError.pop(key)
                        
                registro_log(arrResultadoParcela)

                #Registramos el resultado de la parcela en el arry de respuesta
                for fechaTexto, resultadosParcela in arrResultadoParcela.items():
                    arrRespuesta.update(resultadosParcela["resultado"])

                #Limpiamos arrResultadoParcela para la siguiente parcela
                registro_log("separador")
                registro_log("separador")
                del arrResultadoParcela   
                #siguiente parcela....             
            #Termina el for de las parcelas
            db_informe.save(
                nombre=nombre, 
                capa=capa, 
                fechaInicio=fechaInicio, 
                fechaFin=fechaFin,
                enterprise_id=enterprise_id, 
                esCooperative=esCooperative, 
                id_parcelas=cadenaParcelas, 
                includeClouds=includeClouds, 
                user_created=uid, 
                estado=2
            )
            app_json = json.dumps(arrRespuesta, cls=NpEncoder)
            
            #Creación del Json
            nombreJson = str(uuid.uuid1().int) + '.json'
            file = open(settings.PARCEL_FOLDER + nombreJson, 'w')
            file.write(app_json)
            file.close()
            registro_log("Json creado: "+nombreJson)
            
            #Odenacion del Json por fechas por si tiene varias parcelas
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
                    json2xlsx('order_'+nombreJson, nombreXlsx, capa)
                    
                    # check if file exists
                    if os.path.isfile(settings.PARCEL_FOLDER + nombreXlsx):
                        fileExists = True
                        registro_log("Xlsx creado: "+nombreXlsx)
                
            except Exception as Error:
                fileExists = False
                registro_log("{Error} " + str(Error))
                
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
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
                    [email_user],  # ['soported4sf@smartbits.es']
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                msg.send()
                registro_log("Correo enviado a usuario indicando que ha habido un error al generar el informe")
                
                #MAIL PARA NOSOTROS CON DETALLE DEL ERROR
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': name_user,
                    'email_user': email_user,
                    'parcelas': id_parcelas,
                    'capa': capa,
                    'fecha_inicio': fechaInicio,
                    'fecha_fin': fechaFin,
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
                #adjuntamos el log
                msg.attach_file(settings.PARCEL_FOLDER + NOMBRE_LOG)
                msg.send()
                registro_log("Correo enviado a soporte indicando que ha habido un error al generar el informe") 
                exit()

            registro_log("separador")
            registro_log("separador")
            registro_log("Ultima parcela: "+fallidas)

            if serializer.save(
                nombre=nombre, 
                capa=capa, 
                fechaInicio=fechaInicio, 
                fechaFin=fechaFin,
                enterprise_id=enterprise_id, 
                esCooperative=esCooperative, 
                jsonFile=nombreJson,
                xlsxFile=nombreXlsx, 
                id_parcelas='', 
                includeClouds=includeClouds, 
                user_created=uid, 
                estado=3, 
                error= not fileExists, #TODO: check not fileExists
                parcelas_fallidas=fallidas) and fileExists: 
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': name_user,
                    #'img_plot': my_string,
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
                    [email_user],  # ['soported4sf@smartbits.es']
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_file(settings.PARCEL_FOLDER+nombreXlsx)
                #msg.attach(str(nombre) + '.xlsx', archivo_adjunto, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                msg.send()
                registro_log("Correo enviado a usuario indicando que el informe ha sido generado correctamente")
                
                # MAIL PARA NOSOTROS CON DETALLE DEL INFORME
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': name_user,
                    'email_user': email_user,
                    'parcelas': id_parcelas,
                    'capa': capa,
                    'fecha_inicio': fechaInicio,
                    'fecha_fin': fechaFin,
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
                msg.send()
                registro_log("Correo enviado a soporte indicando que el informe ha sido generado correctamente")

                
            else:
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
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
                    [email_user],  # ['soported4sf@smartbits.es']
                    # BCC
                    ['backups@smartbits.es']
                )
                msg.attach_alternative(email_html_message_enterprise, "text/html")
                msg.send()
                registro_log("Correo enviado a usuario indicando que ha habido un error al generar el informe")
                
                # MAIL PARA NOSOTROS CON DETALLE DEL ERROR
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': name_user,
                    'email_user': email_user,
                    'parcelas': id_parcelas,
                    'capa': capa,
                    'fecha_inicio': fechaInicio,
                    'fecha_fin': fechaFin,
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
                msg.send()
                registro_log("Correo enviado a soporte indicando que ha habido un error al generar el informe")       
                

        except Exception as Error:
            registro_log("{Error} " + str(Error))
           

            # if fileExists is false
            if not fileExists:
                db_informe.save(
                    nombre=nombre, 
                    capa=capa, 
                    fechaInicio=fechaInicio, 
                    fechaFin=fechaFin,
                    enterprise_id=enterprise_id, 
                    esCooperative=esCooperative, 
                    id_parcelas=cadenaParcelas, 
                    includeClouds=includeClouds, 
                    user_created=uid, 
                    estado=4
                )

                # MAIL PARA NOSOTROS CON DETALLE DEL ERROR
                # CONFIG EMAIL
                site_shortcut_name = 'Data4SmartFarming'
                context = {
                    'site_name': site_shortcut_name,
                    'nombre_informe': nombre,
                    'nombre_user': name_user,
                    'email_user': email_user,
                    'parcelas': id_parcelas,
                    'capa': capa,
                    'fecha_inicio': fechaInicio,
                    'fecha_fin': fechaFin,
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
                msg.send()
                registro_log("Correo enviado a soporte indicando que ha habido un error al generar el informe")
                
    thread = Thread(target=supProcess, kwargs=dict(serializer=serializer, email_user=email_user, name_user=name_user, uid=uid,request=request))
    thread.start()