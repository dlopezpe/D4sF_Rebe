import json

import numpy as np


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

    @staticmethod
    def get_pixeles(arr_mask):
        if len(arr_mask) == 2:
            return arr_mask[1][1]
        else:
            return 0

    @staticmethod
    def percentage(part, whole):
        if part > 0:
            return float(round(100 * float(part) / float(whole), 2))
        else:
            return 0
