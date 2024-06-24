from sentinelhub import SHConfig
import datetime
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as imageesport
from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox
from shapely.geometry import Polygon

INSTANCE_ID = '98c6d822-edb7-4a78-b7da-96b1a2bdefb4'  # In case you put instance ID into configuration file you can leave this unchanged

if INSTANCE_ID:
    config = SHConfig()
    config.instance_id = INSTANCE_ID
else:
    config = None

def plot_image(image, factor=1):
    """
    Utility function for plotting RGB images.
    """
    fig = plt.subplots(nrows=1, ncols=1, figsize=(15, 7))

    if np.issubdtype(image.dtype, np.floating):
        plt.imshow(np.minimum(image * factor, 1))
    else:
        plt.imshow(image)
        imageesport.imsave('name.png', image)

#betsiboka_coords_wgs84 = [46.16, -16.15, 46.51, -15.58]
betsiboka_coords_wgs84 = [-3.827278, 40.289793, -3.802327, 40.272505]
betsiboka_bbox = BBox(((499980.0, 2290200.0), (609780.0, 2400000.0)), crs=CRS('32604'))

wms_true_color_request = WmsRequest(
    layer='AGRICULTURE',
    bbox=betsiboka_bbox,
    time='2020-05-28',
    width=5000,
    config=config
)

wms_true_color_img = wms_true_color_request.get_data()
print('Returned data is of type = %s and length %d.' % (type(wms_true_color_img), len(wms_true_color_img)))
print('Single element in the list is of type {} and has shape {}'.format(type(wms_true_color_img[-1]), wms_true_color_img[-1].shape))
plot_image(wms_true_color_img[-1])
