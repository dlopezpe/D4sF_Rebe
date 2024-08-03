import matplotlib
import numpy as np
from sentinelhub import SHConfig

from sentinelhub import CRS, BBox, DataCollection, WebFeatureService
import json
from modulos.parcelas.models import Parcel
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon

matplotlib.use('Agg')
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


def get_bbox(serializer):
    # Establecemos la configuración con sentinel
    config = SHConfig()
    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET
        config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
    if config.instance_id == '':
        print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")
    id_parcelas = serializer.validated_data['id_parcelas']
    fecha_inicio = serializer.validated_data['fecha_inicio']
    fecha_fin = serializer.validated_data['fecha_fin']
    time_interval = (fecha_inicio, fecha_fin)
    parcelas = Parcel.objects.filter(pk__in=id_parcelas)
    arr_parcelas_polygon = []
    for parcela in parcelas:
        arr_parcelas_polygon.append(parcela.polygon)
    # print(arr_parcelas_polygon)
    mp = MultiPolygon(arr_parcelas_polygon)
    bbox_mp = BBox(bbox=mp.extent, crs=CRS.WGS84)
    wfs_iterator = WebFeatureService(
        bbox_mp,
        time_interval,
        data_collection=DataCollection.SENTINEL2_L1C,
        maxcc=100,
        config=config
    )
    results = list(wfs_iterator)
    # print(results)
    return results


def ndvi_img_fechas(serializer):
    id_parcelas = serializer.validated_data['id_parcelas']
    fecha_inicio = serializer.validated_data['fecha_inicio']
    fecha_fin = serializer.validated_data['fecha_fin']
    time_interval = (fecha_inicio, fecha_fin)
    # Establecemos la configuración con sentinel
    config = SHConfig()
    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret = CLIENT_SECRET
        config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
    if config.instance_id == '':
        print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")

    arr_respuesta = {}
    arr_parcelas_polygon = []
    parcelas = Parcel.objects.filter(pk__in=id_parcelas)
    for parcela in parcelas:
        # print(parcela.name)
        arr_parcelas_polygon.append(parcela.polygon)
    # print(arr_parcelas_polygon)
    mp = MultiPolygon(arr_parcelas_polygon)

    for id_parcela in id_parcelas:
        parcel = Parcel.objects.get(pk=int(id_parcela))
        nombre_parcela = parcel.name
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
        arr_result = {id_parcela: {"nombre": nombre_parcela, "resultados": results}}
        arr_respuesta.update(arr_result)
    return arr_respuesta
