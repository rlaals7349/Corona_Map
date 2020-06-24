# -*- coding: utf-8 -*-
import os 
import folium 
from corona_map import *

busan_map = make_default_Map()
busan_map = make_choropleth(busan_map)
busan_map = make_subway_layer(busan_map)
# busan_map = make_MarkerCluster_layer(busan_map)
busan_map = make_patient_layer(busan_map)

busan_map.save(os.path.dirname(os.path.realpath(__file__))+"\\test4.html")

# busan_map.save('C:\\Users\\rlaal\\Desktop')