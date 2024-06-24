from django.conf import settings
from sentinelhub import SHConfig
import numpy as np
import matplotlib
matplotlib.use('Agg')
from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox, DataCollection, SentinelHubRequest, \
    bbox_to_dimensions, CustomUrlParam, FisRequest, Geometry, WebFeatureService
import json
from parcelas.models import Parcel
from django.contrib.gis.geos import GEOSGeometry, polygon, MultiPolygon
import decimal

# Configuracion Sentinel
CLIENT_ID = '33467c23-fada-4405-8a5b-33ee38169273'
CLIENT_SECRET = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'
CLIENT_INSTANCE = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'

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
def getBBOX(serializer):
    # Establecemos la configuración con sentinel
    config = SHConfig()
    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET
        config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
    if config.instance_id == '':
        print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")
    id_parcelas = serializer.validated_data['id_parcelas']
    fechaInicio = serializer.validated_data['fechaInicio']
    fechaFin = serializer.validated_data['fechaFin']
    time_interval = (fechaInicio, fechaFin)
    parcelas = Parcel.objects.filter(pk__in=id_parcelas)
    arrParcelasPolygon = []
    for parcela in parcelas:
        arrParcelasPolygon.append(parcela.polygon)
    # print(arrParcelasPolygon)
    mp = MultiPolygon(arrParcelasPolygon)
    bbox_mp = BBox(bbox=mp.extent, crs=CRS.WGS84)
    wfs_iterator = WebFeatureService(
        bbox_mp,
        time_interval,
        data_collection=DataCollection.SENTINEL2_L1C,
        maxcc=100,
        config=config
    )
    results = list(wfs_iterator)
    #print(results)
    return results

def ndviImgFechas(serializer):
    id_parcelas = serializer.validated_data['id_parcelas']
    fechaInicio = serializer.validated_data['fechaInicio']
    fechaFin = serializer.validated_data['fechaFin']
    time_interval = (fechaInicio, fechaFin)
    # Establecemos la configuración con sentinel
    config = SHConfig()
    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET
        config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
    if config.instance_id == '':
        print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")


    arrRespuesta = {}
    arrParcelasPolygon = []
    parcelas = Parcel.objects.filter(pk__in=id_parcelas)
    for parcela in parcelas:
        #print(parcela.name)
        arrParcelasPolygon.append(parcela.polygon)
    #print(arrParcelasPolygon)
    mp = MultiPolygon(arrParcelasPolygon)


    for id_parcela in id_parcelas:
        parcel = Parcel.objects.get(pk=int(id_parcela))
        nombreParcela = parcel.name
        polygon = GEOSGeometry(parcel.polygon)
        bbox = BBox(bbox=polygon.extent, crs=CRS.WGS84)

        wfs_iterator = WebFeatureService(
            bbox,
            time_interval,
            data_collection=DataCollection.SENTINEL2_L1C,
            maxcc=100,
            config=config
        )
        results = list(wfs_iterator)
        # print(results)
        arrResult = {id_parcela: {"nombre": nombreParcela, "resultados": results}}
        arrRespuesta.update(arrResult)
    return arrRespuesta


    """
    id_parcelas = serializer.validated_data['id_parcelas']
    fechaInicio = serializer.validated_data['fechaInicio']
    fechaFin = serializer.validated_data['fechaFin']
    time_interval = (fechaInicio, fechaFin)
    # Establecemos la configuración con sentinel
    config = SHConfig()
    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET
        config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
    if config.instance_id == '':
        print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")


    arrRespuesta = {}
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


        geometry_string = polygon.wkt
        areaCrud = polygon.area
        area = float(decimal.Context(prec=3).create_decimal(float(str(areaCrud)[:10])))
        bbox = BBox(bbox=polygon.extent, crs=CRS.WGS84)

        wms_ndvi_request = WcsRequest(
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
        images = wms_ndvi_request.get_data()

        fechaAnterior = "0"
        fechas_gen = []
        for idx, (image, time) in enumerate(zip(images, wms_ndvi_request.get_dates())):
            if str(time.date().isoformat()) != fechaAnterior:
                fechaAnterior = time.date().isoformat()
                fechas_gen.append(time.date().isoformat())

        arrResult = {
            id_parcela: {"nombre": nombreParcela, "fechas": fechas_gen}}
        arrRespuesta.update(arrResult)
    return arrRespuesta
    """