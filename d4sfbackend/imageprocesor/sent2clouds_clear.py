from sentinelhub import SHConfig
import numpy as np
from matplotlib import cm
import pandas as pd
import cv2
from matplotlib import pyplot as plt
from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox, DataCollection, SentinelHubRequest, \
    bbox_to_dimensions, CustomUrlParam, FisRequest, Geometry
from s2cloudless import S2PixelCloudDetector, CloudMaskRequest, get_s2_evalscript
import uuid
import json

import pyproj

from sentinelhub.time_utils import parse_time

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

def plot_image(image=None, mask=None, ax=None, factor=3.5/255, clip_range=(0, 1), nombreArchivo='pruebas', **kwargs):
    """ Utility function for plotting RGB images and masks.
    """
    if ax is None:
        _, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))

    mask_color = [255, 255, 255, 255] if image is None else [255, 255, 0, 100]

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
    plt.savefig('media/cloud_mix_' + nombreArchivo, bbox_inches='tight')


# Establecemos la configuración con sentinel
config = SHConfig()
if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET
    config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'

if config.instance_id == '':
    print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")

#Objeto Polygono + BBOX + tiempo
full_geometry = Geometry({"type": "Polygon", "coordinates": [[[-3.790454864501953, 40.263153641723562], [-3.790798187255859, 40.260206255942158], [-3.788223266601563, 40.259878760706755], [-3.789596557617187, 40.262236691018451], [-3.790454864501953, 40.263153641723562]]]}, crs=CRS.WGS84)
geometry_string = 'POLYGON ((-3.790454864501953 40.26315364172356, -3.790798187255859 40.26020625594216, -3.788223266601563 40.25987876070675, -3.789596557617187 40.26223669101845, -3.790454864501953 40.26315364172356))'
bbox = BBox(bbox=[-3.7907981872558594, 40.259878760706755, -3.788223266601563, 40.26315364172356], crs=CRS.WGS84)
time_interval = ('2021-05-15', '2021-05-31')

wms_ndvi_request = WcsRequest(
    data_collection=DataCollection.SENTINEL2_L1C,
    layer='NDVI',
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
request_true_color = SentinelHubRequest(
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=time_interval,
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

true_color_imgs = request_true_color.get_data()
images = wms_ndvi_request.get_data()
images_true_color = wms_true_color_request.get_data()
fig, axs = plt.subplots((len(images) + 2) // 3, 3, figsize=(10, 20))
fig, axs2 = plt.subplots((len(images_true_color) + 2) // 3, 3, figsize=(10, 20))
fig, axs3 = plt.subplots((len(images_true_color) + 2) // 3, 3, figsize=(10, 20))

evalscript_clouds = get_s2_evalscript(
    all_bands=False,
    reflectance=True
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

def get_true_color_request(time_interval_separate):
    return SentinelHubRequest(
        evalscript=evalscript_clouds,
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
evalscript_clm = """
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04", "CLM"],
    output: { bands: 3 }
  }
}

function evaluatePixel(sample) {
  if (sample.CLM == 1) {
    return [0.75 + sample.B04, sample.B03, sample.B02]
  }
  return [3.5*sample.B04, 3.5*sample.B03, 3.5*sample.B02];
}
"""
def get_true_color_request_plus_clouds(time_interval_separate):
    return SentinelHubRequest(
        evalscript=evalscript_clm,
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
arrRespuesta = {}
for idx, (image, time) in enumerate(zip(images, wms_ndvi_request.get_dates())):
    nombreArchivo = str(uuid.uuid1().int) + '_'+str(idx)+ '.png'
    trans_mask = image[:, :, 3] == 0
    image[trans_mask] = [255, 255, 255, 255]
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('media/'+nombreArchivo, img)
    #cv2.imwrite('media/natural_img_'+nombreArchivo, true_color_imgs[idx])
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
    #Imagen Cloud solo
    mask_color = [255, 255, 255, 255]
    cloud_image = np.zeros((cloud_mask.shape[0], cloud_mask.shape[1], 4), dtype=np.uint8)
    cloud_image[cloud_mask == 1] = np.asarray(mask_color, dtype=np.uint8)
    unique, counts = np.unique(cloud_image, return_counts=True)
    pixeles_nubes = getPixeles(np.asarray((unique, counts)).T)
    axs3.flat[idx].imshow(cloud_image)
    cv2.imwrite('media/cloud_' + nombreArchivo, cloud_image)

    #Cloud plus true
    plot_image(image=data_true_color_img, mask=cloud_mask, nombreArchivo=nombreArchivo)
    """
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    # create empty matrix
    vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
    # combine 2 images
    vis[:h1, :w1, :3] = img1
    vis[:h2, w1:w1 + w2, :3] = img2
    #vis = np.concatenate((img1, img2), axis=0)
    cv2.imwrite('media/cloud_mix_' + nombreArchivo, vis)
    """

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
    area = 0
    total_pixeles = arr_total[1][1]
    total_pixeles_azul = {"total": pixeles_azules, "porcent": percentage(pixeles_azules, arr_total[1][1]),
                          "altos": {"total": pixeles_azules_altos, "porcent": percentage(pixeles_azules_altos, total_pixeles), "area_porcent": (percentage(pixeles_azules_altos, total_pixeles) * area / 100)},
                          "medios": {"total": pixeles_azules_medios,
                                     "porcent": percentage(pixeles_azules_medios, total_pixeles),
                                     "area_porcent": (percentage(pixeles_azules_medios, total_pixeles) * area / 100)},
                          "bajos": {"total": pixeles_azules_bajos,
                                    "porcent": percentage(pixeles_azules_bajos, total_pixeles),
                                    "area_porcent": (percentage(pixeles_azules_bajos, total_pixeles) * area / 100)}}
    total_pixeles_amarillo = {"total": pixeles_amarillos, "porcent": percentage(pixeles_amarillos, arr_total[1][1]),
                              "altos": {"total": pixeles_amarillos_altos,
                                        "porcent": percentage(pixeles_amarillos_altos, total_pixeles), "area_porcent": (
                                              percentage(pixeles_amarillos_altos, total_pixeles) * area / 100)},
                              "medios": {"total": pixeles_amarillos_medios,
                                         "porcent": percentage(pixeles_amarillos_medios, total_pixeles),
                                         "area_porcent": (
                                                     percentage(pixeles_amarillos_medios, total_pixeles) * area / 100)},
                              "bajos": {"total": pixeles_amarillos_bajos,
                                        "porcent": percentage(pixeles_amarillos_bajos, total_pixeles), "area_porcent": (
                                              percentage(pixeles_amarillos_bajos, total_pixeles) * area / 100)}}
    total_pixeles_rojo = {"total": pixeles_rojos, "porcent": percentage(pixeles_rojos, arr_total[1][1]),
                          "altos": {"total": pixeles_rojos_altos,
                                    "porcent": percentage(pixeles_rojos_altos, total_pixeles),
                                    "area_porcent": (percentage(pixeles_rojos_altos, total_pixeles) * area / 100)},
                          "medios": {"total": pixeles_rojos_medios,
                                     "porcent": percentage(pixeles_rojos_medios, total_pixeles),
                                     "area_porcent": (percentage(pixeles_rojos_medios, total_pixeles) * area / 100)},
                          "bajos": {"total": pixeles_rojos_bajos,
                                    "porcent": percentage(pixeles_rojos_bajos, total_pixeles),
                                    "area_porcent": (percentage(pixeles_rojos_bajos, total_pixeles) * area / 100)}}
    total_pixeles_verde = {"total": pixeles_verdes, "porcent": percentage(pixeles_verdes, arr_total[1][1]),
                           "altos": {"total": pixeles_verdes_altos,
                                     "porcent": percentage(pixeles_verdes_altos, total_pixeles),
                                     "area_porcent": (percentage(pixeles_verdes_altos, total_pixeles) * area / 100)},
                           "medios": {"total": pixeles_verdes_altos,
                                      "porcent": percentage(pixeles_verdes_medios, total_pixeles),
                                      "area_porcent": (percentage(pixeles_verdes_medios, total_pixeles) * area / 100)}}
    total_pixeles_nubes = {"total": pixeles_nubes, "porcent": percentage(pixeles_nubes, arr_total[1][1])}
    # ESTABLECEMOS EL RESULTADO
    arrResult = {
        idx: {"img": nombreArchivo, "totalPixeles": arr_total[0][1], "fecha": time.date().isoformat(), 'nombre:': 'Pruebas', "area": area,
                              "azules": total_pixeles_azul, "amarillos": total_pixeles_amarillo,
                              "rojos": total_pixeles_rojo, "verdes": total_pixeles_verde, "nubes": total_pixeles_nubes}}
    arrRespuesta.update(arrResult)

    axs2.flat[idx].imshow(images_true_color[idx])
    axs2.flat[idx].set_title(time.date().isoformat())

    axs.flat[idx].imshow(image)
    axs.flat[idx].set_title(time.date().isoformat()+' '+str(idx)+' Rojo ' +str(pixeles_rojos)+' Nubes ' +str(pixeles_nubes))

fig.tight_layout()
app_json = json.dumps(arrRespuesta, cls=NpEncoder)
nombreJson = str(uuid.uuid1().int)+'.json'
file = open('media/'+nombreJson, 'w')
file.write(app_json)
file.close()
plt.show()



