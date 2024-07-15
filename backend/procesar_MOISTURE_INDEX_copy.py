from django.conf import settings
from datetime import datetime
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
#from s2cloudless import S2PixelCloudDetector, CloudMaskRequest, get_s2_evalscript
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

evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""




def procesarMOISTURE(serializer, email_user, name_user, uid):
    def supProcess(serializer, email_user, name_user, uid):

        now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') 
        #nombreArchivoErrores = str(uuid.uuid1().int) + '.log'
        nombreArchivoErrores = serializer.validated_data['nombre']+"__"+str(now)+'.log'
        fileErr = open(settings.PARCEL_FOLDER + nombreArchivoErrores, 'w')

        print(email_user)
        print(name_user)
        print(uid)
        
        fileErr.write(str(email_user)+'\n')
        fileErr.write(str(name_user)+'\n')
        fileErr.write(str(uid)+'\n')
        fileErr.close()

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
        db_informe=serializer
        db_informe.save(nombre=nombre, capa=capa, fechaInicio=fechaInicio, fechaFin=fechaFin,
                           enterprise_id=enterprise_id, esCooperative=esCooperative, id_parcelas='', includeClouds=includeClouds, user_created=uid, estado=1)
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
        try:
            # Establecemos la configuración con sentinel
            config = SHConfig()
            if CLIENT_ID and CLIENT_SECRET:
                config.sh_client_id = CLIENT_ID
                config.sh_client_secret = CLIENT_SECRET
                config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
            if config.instance_id == '':
                print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")

                fileErr = open(settings.PARCEL_FOLDER + nombreArchivoErrores, 'a')
                fileErr.write("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.\n")
                fileErr.close()

            def plot_image(image=None, mask=None, ax=None, factor=3.5 / 255, clip_range=(0, 1), nombreArchivo='pruebas',
                        **kwargs):
                """ Utility function for plotting RGB images and masks.
                """
                if ax is None:
                    _, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))

                mask_color = [255, 255, 255, 255] if image is None else [255, 0, 0, 100]

                if image is None:
                    if mask is None:
                        raise ValueError('image or mask should be given')
                    image = np.zeros(mask.shape + (3,), dtype=np.uint8)

                ax.imshow(np.clip(image * factor, *clip_range), **kwargs)

                if mask is not None:
                    cloud_image = np.zeros((mask.shape[0], mask.shape[1], 4), dtype=np.uint8)

                    cloud_image[mask == 1] = np.asarray(mask_color, dtype=np.uint8)

                    ax.imshow(cloud_image)
                plt.axis('off')
                plt.savefig(settings.PARCEL_FOLDER+'cloud_mix_' + nombreArchivo, bbox_inches='tight')
                plt.close()

            arrRespuesta = {}
            arrError = []
            for id_parcela in id_parcelas:
                parcel = Parcel.objects.get(pk=int(id_parcela))
                nombreParcela = parcel.name
                polygon = GEOSGeometry(parcel.polygon)
                nombreJson = str(id_parcela) + '.json'
                file = open(settings.PARCEL_FOLDER + nombreJson, 'w')
                file.write(polygon.geojson)
                file.close()
                f = open(settings.PARCEL_FOLDER + nombreJson, )
                full_geometry = Geometry(json.load(f), crs=CRS.WGS84)
                fallidas=""


                geometry_string = str(polygon.wkt)
                areaCrud = polygon.area
                #area = float(decimal.Context(prec=3).create_decimal(float(str(areaCrud)[:10])))
                area = parcel.area
                bbox = BBox(polygon.extent, crs=CRS.WGS84)

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
                except Exception as Error:
                    fileErr = open(settings.PARCEL_FOLDER +"catch_"+nombreArchivoErrores, 'a')
                    fileErr.write(id_parcela+"\n")
                    fileErr.close()
                    fallidas+=str(id_parcela)+" "
                    errores=True
                """
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
                    image_format=MimeType.TIFF
                )
                """
                if includeClouds:
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
                    except Exception as Error:
                        fileErr = open(settings.PARCEL_FOLDER +"catch_"+nombreArchivoErrores, 'a')
                        fileErr.write(id_parcela+"\n")
                        fileErr.close()
                        fallidas+=str(id_parcela)+" "
                        errores=True

                #True Color
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
                except Exception as Error:
                    fileErr = open(settings.PARCEL_FOLDER +"catch_"+nombreArchivoErrores, 'a')
                    fileErr.write(id_parcela+"\n")
                    fileErr.close()
                    fallidas+=str(id_parcela)+" "
                    errores=True
                #images_true_color = wms_true_color_request.get_data()
                """
                evalscript = get_s2_evalscript(
                    all_bands=False,
                    reflectance=True
                )

                def get_true_color_request(time_interval_separate):
                    return SentinelHubRequest(
                        evalscript=evalscript,
                        input_data=[
                            SentinelHubRequest.input_data(
                                data_collection=DataCollection.SENTINEL2_L1C,
                                time_interval=time_interval_separate
                            )
                        ],
                        responses=[
                            SentinelHubRequest.output_response('default', MimeType.TIFF)
                        ],
                        bbox=bbox,
                        size=bbox_to_dimensions(bbox, 2),
                        geometry=full_geometry,
                        config=config
                    )

                def get_true_color_image_request(time_interval_separate):
                    return SentinelHubRequest(
                        evalscript=evalscript_true_color,
                        input_data=[
                            SentinelHubRequest.input_data(
                                data_collection=DataCollection.SENTINEL2_L1C,
                                time_interval=time_interval_separate,
                            )
                        ],
                        responses=[
                            SentinelHubRequest.output_response('default', MimeType.PNG)
                        ],
                        bbox=bbox,
                        size=bbox_to_dimensions(bbox, 2),
                        geometry=full_geometry,
                        config=config
                    )
                """
                fechaAnterior = "0"
                validImage = False
                for idx, (image, time) in enumerate(zip(images, wms_ndvi_request.get_dates())):

                    fileErr = open(settings.PARCEL_FOLDER + nombreArchivoErrores, 'a')
                    fileErr.write("----------------------\n")
                    fileErr.write(str(nombreParcela)+'\n')
                    fileErr.write(str(time.date().isoformat())+'\n')
                    fileErr.write(str(idx)+'\n')
                    fileErr.write("----------------------\n")
                    fileErr.close()

                    if str(time.date().isoformat()) != fechaAnterior:
                        try:
                            nombreArchivo = str(uuid.uuid1().int) + '_' + str(idx) + '_' + id_parcela + '.png'
                            trans_mask = image[:, :, 3] == 0
                            image[trans_mask] = [255, 255, 255, 255]
                            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            cv2.imwrite(settings.PARCEL_FOLDER + nombreArchivo, img)
                            cv2.imwrite(settings.PARCEL_FOLDER + 'trueColor_' + nombreArchivo, cv2.cvtColor(images_true_color[idx], cv2.COLOR_BGR2RGB))
                            #cv2.imwrite(settings.PARCEL_FOLDER + 'natural_img_' + nombreArchivo, images_true_color[idx])

                            if includeClouds:
                                cv2.imwrite(settings.PARCEL_FOLDER + 'cloud_' + nombreArchivo, cv2.cvtColor(images_true_color_cloud[idx], cv2.COLOR_BGR2RGB))
                                """
                                request_true_color = get_true_color_image_request(time.date().isoformat())
                                data_true_color_img = request_true_color.get_data()[0]
                                cv2.imwrite('media/natural_img_' + nombreArchivo, cv2.cvtColor(data_true_color_img, cv2.COLOR_BGR2RGB))

                                request = get_true_color_request(time.date().isoformat())
                                data = request.get_data()[0]

                                bands = data[..., :-1]
                                mask = data[..., -1]
                                cloud_detector = S2PixelCloudDetector(
                                    threshold=0.6,
                                    average_over=4,
                                    dilation_size=2,
                                    all_bands=False
                                )
                                cloud_prob = cloud_detector.get_cloud_probability_maps(bands)
                                cloud_mask = cloud_detector.get_cloud_masks(bands)
                                # Imagen Cloud solo
                                mask_color = [255, 255, 255, 255]
                                cloud_image = np.zeros((cloud_mask.shape[0], cloud_mask.shape[1], 4), dtype=np.uint8)
                                cloud_image[cloud_mask == 1] = np.asarray(mask_color, dtype=np.uint8)
                                unique, counts = np.unique(cloud_image, return_counts=True)
                                pixeles_nubes = getPixeles(np.asarray((unique, counts)).T)
                                cv2.imwrite(settings.PARCEL_FOLDER + 'cloud_' + nombreArchivo, cloud_image)

                                # Cloud plus true
                                plot_image(image=data_true_color_img, mask=cloud_mask, nombreArchivo=nombreArchivo)
                                """

                            # CALCULOS /*******************************************************************
                            image2 = cv2.imread(settings.PARCEL_FOLDER + nombreArchivo, cv2.IMREAD_UNCHANGED)
                            img = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
                            #img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
                            total_pixeles = arr_total[1][1]
                            print(total_pixeles)
                            # FIN CALCULOS /*******************************************************************

                            totalPixDetectados = sum(
                                [pixeles_naranjas, pixeles_amarillos, pixeles_verdes, pixeles_a_claro, pixeles_a_medio,
                                pixeles_a_oscuro])
                            total_pixeles_naranja = {"total": pixeles_naranjas,
                                                    "porcent": percentage(pixeles_naranjas, totalPixDetectados), "area_porcent": (
                                            percentage(pixeles_naranjas, totalPixDetectados) * area / 100)}
                            total_pixeles_amarillo = {"total": pixeles_amarillos,
                                                    "porcent": percentage(pixeles_amarillos, totalPixDetectados),
                                                    "area_porcent": (
                                                                percentage(pixeles_amarillos, totalPixDetectados) * area / 100)}
                            total_pixeles_verde = {"total": pixeles_verdes,
                                                "porcent": percentage(pixeles_verdes, totalPixDetectados),
                                                "area_porcent": (percentage(pixeles_verdes, totalPixDetectados) * area / 100)}
                            total_pixeles_a_claro = {"total": pixeles_a_claro,
                                                    "porcent": percentage(pixeles_a_claro, totalPixDetectados),
                                                    "area_porcent": (percentage(pixeles_a_claro, totalPixDetectados) * area / 100)}
                            total_pixeles_a_medio = {"total": pixeles_a_medio,
                                                    "porcent": percentage(pixeles_a_medio, totalPixDetectados),
                                                    "area_porcent": (percentage(pixeles_a_medio, totalPixDetectados) * area / 100)}
                            total_pixeles_a_oscuro = {"total": pixeles_a_oscuro,
                                                    "porcent": percentage(pixeles_a_oscuro, totalPixDetectados), "area_porcent": (
                                            percentage(pixeles_a_oscuro, totalPixDetectados) * area / 100)}
                            # UNION TOTALES
                            """
                            if includeClouds:
                                if totalPixDetectados == 0:
                                    total_pixeles_nubes = {"total": pixeles_nubes,
                                                        "porcent": 100}
                                else:
                                    if(percentage(pixeles_nubes, totalPixDetectados) > 100):
                                        total_pixeles_nubes = {"total": pixeles_nubes,
                                                            "porcent": 100}
                                    else:
                                        total_pixeles_nubes = {"total": pixeles_nubes,
                                                            "porcent": percentage(pixeles_nubes, totalPixDetectados)}
                            else:
                                total_pixeles_nubes = {"total": "n/a",
                                                    "porcent": "n/a"}
                            """
                            if includeClouds:
                                results_cloud_wfs_invertido = results_cloud_wfs[::-1]
                                total_pixeles_nubes = {"total": "yes", "porcent": str(results_cloud_wfs_invertido[idx]['properties']['cloudCoverPercentage'])}
                            else:
                                total_pixeles_nubes = {"total": "n/a",
                                                    "porcent": "n/a"}
                            # ESTABLECEMOS EL RESULTADO
                            idJson= id_parcela+'_'+str(idx)
                            arrResult = {
                                idJson: {"img": nombreArchivo, "totalPixeles": totalPixDetectados, "fecha": time.date().isoformat(),
                                        "nombre": nombreParcela, "area": area, "naranja": total_pixeles_naranja,
                                        "amarillo": total_pixeles_amarillo, "verdes": total_pixeles_verde,
                                        "azul_claro": total_pixeles_a_claro, "azul_medio": total_pixeles_a_medio,
                                        "azul_oscuro": total_pixeles_a_oscuro, "nubes": total_pixeles_nubes}}
                            arrRespuesta.update(arrResult)
                            fechaAnterior = str(time.date().isoformat())
                            validImage = True
                        except Exception as Error:
                            print(Error)
                            arrError.append({"nombre_parcela": nombreParcela, "fecha": time.date().isoformat(), "error": str(Error)})
                # Termina el for de las imagenes / Eliminado de los errores si se ha llegado a procesar la imagen
                for error in arrError:
                    print(nombreParcela)
                    print(validImage)
                    print(error)

                    fileErr = open(settings.PARCEL_FOLDER + nombreArchivoErrores, 'a')
                    fileErr.write('------------ERROR---------\n')
                    fileErr.write(str(nombreParcela)+'\n')
                    fileErr.write(str(validImage)+'\n')
                    fileErr.write(str(error)+'\n')
                    fileErr.write('---------------------------\n')
                    fileErr.close()

                    if validImage:
                        key = arrError.index(error)
                        arrError.pop(key)
            #Termina el for de las parcelas
            db_informe.save(nombre=nombre, capa=capa, fechaInicio=fechaInicio, fechaFin=fechaFin,
                            enterprise_id=enterprise_id, esCooperative=esCooperative, id_parcelas='', includeClouds=includeClouds, user_created=uid, estado=2)
            app_json = json.dumps(arrRespuesta, cls=NpEncoder)
            #Creación del Json
            nombreJson = str(uuid.uuid1().int) + '.json'
            file = open(settings.PARCEL_FOLDER + nombreJson, 'w')
            file.write(app_json)
            file.close()
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
                dfSort = df.sort_values('fecha', ascending=True)
                dfSort.index = range(len(dfSort.index))
                dfSort.transpose().to_json(settings.PARCEL_FOLDER + 'order_' + nombreJson)

                # HACEMOS EL FICHERO xls
                nombreXlsx = str(uuid.uuid1().int) + '.xlsx'
                json2xlsx('order_'+nombreJson, nombreXlsx, capa)
            except Exception as Error:
                print(Error)
                fileErr = open(settings.PARCEL_FOLDER + nombreArchivoErrores, 'a')
                fileErr.write(str(Error)+'\n')
                fileErr.close()
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
                msg.send()

                exit()

            #Hacemos la imagen plot para el mail
            #plotImgName = 'plot_' + nombreArchivo
            #plotMoisture('order_'+nombreJson, plotImgName)
            #my_string = ''
            #with open(settings.PARCEL_FOLDER+ plotImgName, "rb") as img_file:
                #my_string = base64.b64encode(img_file.read()).decode('ascii')

            if serializer.save(nombre=nombre, capa=capa, fechaInicio=fechaInicio, fechaFin=fechaFin,
                            enterprise_id=enterprise_id, esCooperative=esCooperative, jsonFile=nombreJson,
                            xlsxFile=nombreXlsx, id_parcelas='', includeClouds=includeClouds, user_created=uid, estado=3, error=errores, parcelas_fallidas=fallidas):
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
        except Exception as Error:
            db_informe.save(nombre=nombre, capa=capa, fechaInicio=fechaInicio, fechaFin=fechaFin,
                            enterprise_id=enterprise_id, esCooperative=esCooperative, id_parcelas='', includeClouds=includeClouds, user_created=uid, estado=4)
    thread = Thread(target=supProcess, kwargs=dict(serializer=serializer, email_user=email_user, name_user=name_user, uid=uid))
    thread.start()