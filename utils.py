import json

import numpy as np
import pandas as pd

f = open('macedonia_map.geojson', encoding='utf-8')
jdata = json.load(f)
mkd_pts = []  # mapa od makedonija

for feature in jdata['features']:
    if feature['geometry']['type'] == 'Polygon':
        mkd_pts.extend(feature['geometry']['coordinates'][0])
        mkd_pts.append([None, None])  # mark the end of a polygon

    elif feature['geometry']['type'] == 'MultiPolygon':
        for polyg in feature['geometry']['coordinates']:
            mkd_pts.extend(polyg[0])
            mkd_pts.append([None, None])  # end of polygon
    elif feature['geometry']['type'] == 'LineString':
        mkd_pts.extend(feature['geometry']['coordinates'])
        mkd_pts.append([None, None])
    else:
        pass
    # else: raise ValueError("geometry type irrelevant for map")

mkd_x, mkd_y = zip(*mkd_pts)


def generate_data():

    return pd.DataFrame({
        "Time": [i for i in range(0, 10) for j in range(0,100)],
        "Latitude": np.random.rand(1000) * 1.1 + 41.04,
        "Longitude": np.random.rand(1000) * 2.36 + 20.53,
        "Count": np.random.rand(1000) * 100,
    }
)