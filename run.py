# -*- coding: utf-8 -*-
import os 
import folium 
from corona_map import *

SAVE_FILE_NAME = 'corona_map'

# make defualt map
busan_map = make_default_Map()

# make choropleth
busan_map = make_choropleth(busan_map)

# make subway layer
busan_map = make_subway_layer(busan_map)

# make patient layer(have LayerControl)
busan_map = make_patient_layer(busan_map)

# -------------- optional --------------

# make markercluster layer
# busan_map = make_MarkerCluster_layer(busan_map)

busan_map.save(os.path.dirname(os.path.realpath(__file__))+"\\{}.html".format(SAVE_FILE_NAME))