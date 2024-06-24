
from sentinelhub import SHConfig

import datetime
import base64
import numpy as np
from matplotlib import cm
import pandas as pd
import cv2
import os

from PIL import Image, ImageDraw


#import geopandas as gpd

from matplotlib import pyplot as plt

from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox, DataCollection, SentinelHubRequest, bbox_to_dimensions, CustomUrlParam, FisRequest, Geometry

from s2cloudless import S2PixelCloudDetector, CloudMaskRequest, get_s2_evalscript

import pyproj

from sentinelhub.time_utils import parse_time


rojo_altos = [np.array([0,0,254]), np.array([0,0,255])]
rojo_medios = [np.array([0,0,154]), np.array([0,0,155])]
rojo_bajos = [np.array([0,0,102]), np.array([0,0,103])]
def plot_image(image=None, mask=None, ax=None, factor=3.5/255, clip_range=(0, 1), **kwargs):
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
    plt.show()

def getPixeles(arr_mask):
    if len(arr_mask) == 2:
        return arr_mask[1][1]
    else:
        return 0

CLIENT_ID = '33467c23-fada-4405-8a5b-33ee38169273'
CLIENT_SECRET = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'

config = SHConfig()

if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET
    config.instance_id = '5c9f425a-f830-4164-8a6c-6059bcf1b7d3'
    #13e7a2a7-2e3e-489e-8a65-eb971dab81af

if config.instance_id == '':
    print("Warning! To use OGC functionality of Sentinel Hub, please configure the `instance_id`.")

#SHAPE_PATH = os.path.join('.', 'media', '1152.json')
#area_gdf = gpd.read_file(SHAPE_PATH)

# Geometry of an entire area
full_geometry = Geometry({ "type": "Polygon", "coordinates": [ [ [ -3.790454864501953, 40.263153641723562 ], [ -3.790798187255859, 40.260206255942158 ], [ -3.788223266601563, 40.259878760706755 ], [ -3.789596557617187, 40.262236691018451 ], [ -3.790454864501953, 40.263153641723562 ] ] ] }, crs=CRS.WGS84)
bbox = BBox([-3.7907981872558594, 40.259878760706755, -3.788223266601563, 40.26315364172356], crs=CRS.WGS84)
print(full_geometry)

evalscript_true_color = """
    //VERSION=3
    let index = (B8A - B11)/(B8A + B11);

    let val = colorBlend(index, [-0.8, -0.24, -0.032, 0.032, 0.24, 0.8], [[0.5,0,0], [1,0,0], [1,1,0], [0,1,1], [0,0,1], [0,0,0.5]]);
    val.push(dataMask);
    return val;
"""

request = SentinelHubRequest(
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval='2021-05-11'
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.PNG)
    ],
    geometry=full_geometry,
    size=bbox_to_dimensions(bbox, 10),
    config=config
)

image = request.get_data()[0]

#plot_image(image, factor=3.5/255, clip_range=(0,1))




#-738687.4413479418%2C4709132.438593138%2C-738075.9451216604%2C4709743.93481942
wgs84 = pyproj.Proj(projparams='epsg:4326')
InputGrid = pyproj.Proj(projparams='epsg:3857')

x1, y1 = -738687.4413479418, 4709132.438593138
x2, y2 = -738075.9451216604, 4709743.93481942
#print(pyproj.partial(InputGrid, wgs84, x1, y1))
transformer = pyproj.Transformer.from_crs("epsg:3857", "epsg:4326")
print(transformer.transform(x1, y1))
print(transformer.transform(x2, y2))

#betsiboka_coords_wgs84 = [46.16, -16.15, 46.51, -15.58]
betsiboka_coords_wgs84 = [-3.7907981872558594, 40.259878760706755, -3.788223266601563, 40.26315364172356]
betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
time_interval = ('2021-05-01', '2021-05-31')
wms_true_color_request = WcsRequest(
    data_collection=DataCollection.SENTINEL2_L1C,
    layer='NDVI',
    bbox=betsiboka_bbox,
    time=time_interval,
    resx='1m',
    resy='1m',
    custom_url_params={
        CustomUrlParam.SHOWLOGO: False,
        CustomUrlParam.GEOMETRY: 'POLYGON ((-3.790454864501953 40.26315364172356, -3.790798187255859 40.26020625594216, -3.788223266601563 40.25987876070675, -3.789596557617187 40.26223669101845, -3.790454864501953 40.26315364172356))'
    },
    config=config,
    image_format=MimeType.PNG
)
wms_true_color_request_TUE_COLOR = WcsRequest(
    data_collection=DataCollection.SENTINEL2_L1C,
    layer='TRUE_COLOR',
    bbox=betsiboka_bbox,
    time=time_interval,
    resx='1m',
    resy='1m',
    custom_url_params={
        CustomUrlParam.SHOWLOGO: False,
        CustomUrlParam.GEOMETRY: 'POLYGON ((-3.790454864501953 40.26315364172356, -3.790798187255859 40.26020625594216, -3.788223266601563 40.25987876070675, -3.789596557617187 40.26223669101845, -3.790454864501953 40.26315364172356))'
    },
    config=config,
    image_format=MimeType.PNG
)
#wms_true_color_img = wms_true_color_request.get_data()
#print('Returned data is of type = %s and length %d.' % (type(wms_true_color_img), len(wms_true_color_img)))
#print('Single element in the list is of type {} and has shape {}'.format(type(wms_true_color_img[-1]), wms_true_color_img[-1].shape))
#plt.imshow(wms_true_color_img[-1])
#plt.show()
images = wms_true_color_request.get_data()
images2 = wms_true_color_request_TUE_COLOR.get_data()
fig, axs = plt.subplots((len(images) + 2) // 3, 3, figsize=(10, 20))
#fig, axs2 = plt.subplots((len(images) + 2) // 3, 3, figsize=(10, 20))
print()

for idx, (image, time) in enumerate(zip(images, wms_true_color_request.get_dates())):
    trans_mask = image[:, :, 3] == 0
    image[trans_mask] = [255, 255, 255, 255]
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    # ROJO/NARANJAS
    mask_rojo = cv2.inRange(img, rojo_bajos[0], rojo_altos[0])
    unique, counts = np.unique(mask_rojo, return_counts=True)
    pixeles_rojos = getPixeles(np.asarray((unique, counts)).T)


    #axs2.flat[idx].imshow(mask_rojo)
    #axs2.flat[idx].set_title(time.date().isoformat() + '\n' + str(idx)+ '\n' +str(pixeles_rojos))

    axs.flat[idx].imshow(image)
    axs.flat[idx].set_title(time.date().isoformat()+'\n'+str(idx)+'\n Rojo' +str(pixeles_rojos))

fig.tight_layout()
#plt.show()
plt.savefig('media/books_read.png', bbox_inches='tight')


fis_request = FisRequest(
    data_collection=DataCollection.SENTINEL2_L1C,
    layer='S2REP',
    geometry_list=[betsiboka_bbox],
    time=time_interval,
    resolution='2m',
    data_folder='./media',
    config=config
)

fis_data = fis_request.get_data(save_data=True)  # Takes about 30s, to avoid redownloading we are saving results

def fis_data_to_dataframe(fis_data):
    """ Creates a DataFrame from list of FIS responses
    """
    COLUMNS = ['channel', 'date', 'min', 'max', 'mean', 'stDev']
    data = []

    for fis_response in fis_data:
        for channel, channel_stats in fis_response.items():
            for stat in channel_stats:
                row = [int(channel[1:]), parse_time(stat['date'], force_datetime=True)]

                for column in COLUMNS[2:]:
                    row.append(stat['basicStats'][column])

                data.append(row)

    return pd.DataFrame(data, columns=COLUMNS).sort_values(['channel', 'date'])


df = fis_data_to_dataframe(fis_data)

df.head()



BANDS = 'B01,B02,B03,B04,B05,B06,B07,B08,B8A,B09,B10,B11,B12'.split(',')

plt.figure(figsize=(12, 8))
for channel, (band, color) in enumerate(zip(BANDS, cm.jet(np.linspace(0, 1, 13)))):
    channel_df = df[df.channel == channel]
    plt.plot(channel_df.date, channel_df['mean'], '-o', markeredgewidth=1,
             color=color, markerfacecolor='None', label=band)
    plt.fill_between(list(channel_df.date),  channel_df['mean'] - channel_df['stDev'],
                     channel_df['mean'] + channel_df['stDev'], alpha=0.2, color=color)

plt.legend(loc='upper right');
plt.show()


















exit()
#bbox = BBox([-90.9217, 14.4191, -90.8187, 14.5520], crs=CRS.WGS84)
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
request = SentinelHubRequest(
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval='2017-12-01'
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.PNG)
    ],
    bbox=bbox,
    size=bbox_to_dimensions(bbox, 10),
    config=config
)

true_color_image = request.get_data()[0]
print(true_color_image)
print(type(true_color_image))
"""
true_color_image.shape
plt.imshow(true_color_image)
plt.show()
evalscript = get_s2_evalscript(
    all_bands=False,
    reflectance=True
)
request = SentinelHubRequest(
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval='2017-12-01'
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF)
    ],
    bbox=bbox,
    size=bbox_to_dimensions(bbox, 10),
    config=config
)

data = request.get_data()[0]

bands = data[..., :-1]
mask = data[..., -1]
cloud_detector = S2PixelCloudDetector(
    threshold=0.4,
    average_over=4,
    dilation_size=2,
    all_bands=False
)
cloud_prob = cloud_detector.get_cloud_probability_maps(bands)
cloud_mask = cloud_detector.get_cloud_masks(bands)
print(cloud_prob)
print(cloud_mask)
plot_image(mask=cloud_mask)
"""""
"""
betsiboka_coords_wgs84 = [34.27350018735774, -119.11801036162888, 34.26594769880744, -119.12604911490116]

betsiboka_bbox = BBox([46.16, -16.15, 46.51, -15.58], crs=CRS.WGS84)

wms_true_color_request = WmsRequest(
    data_collection=DataCollection.SENTINEL2_L1C,
    layer='TRUE_COLOR',
    bbox=betsiboka_bbox,
    time='2021-02-27',
    width=512,
    height=856,
    config=config
)

wms_true_color_img = wms_true_color_request.get_data()

print('Returned data is of type = %s and length %d.' % (type(wms_true_color_img), len(wms_true_color_img)))
print('Single element in the list is of type {} and has shape {}'.format(type(wms_true_color_img[-1]), wms_true_color_img[-1].shape))
plt.imshow(wms_true_color_img[-1])

evalscript = get_s2_evalscript(
    all_bands=False,
    reflectance=True
)

print(evalscript)
request = SentinelHubRequest(
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval='2021-02-27'
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF)
    ],
    bbox=betsiboka_bbox,
    size=[512, 856],
    config=config
)

data = request.get_data()[0]

bands = data[..., :-1]
mask = data[..., -1]

print(bands.shape, mask.shape)
cloud_detector = S2PixelCloudDetector(
    threshold=0.4,
    average_over=4,
    dilation_size=2,
    all_bands=False
)
cloud_prob = cloud_detector.get_cloud_probability_maps(bands)
cloud_mask = cloud_detector.get_cloud_masks(bands)

plt.show()
plt.imshow(mask)
plt.show()
"""

