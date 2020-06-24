# -*- coding: utf-8 -*-
import requests
import json
import os 
import folium 
from folium import plugins
from folium.plugins import MarkerCluster

import re
import random
import pandas as pd

import datetime

from stations import stations, bfs
from functions import get_arrows, get_bearing
from functions import load_subway, load_busan_geojson, load_patient, load_gu_info

sub = load_subway()
line1 = sub[sub['호선']=='1호선']
print( line1 )