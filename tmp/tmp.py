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
# from tabulate import tabulate
import prettytable


# sub = load_subway()
# sub.rename(columns={'위도':'latitude', '경도':'longitude'}, inplace=True)
# sub = sub[['역명','역주소','latitude','longitude','호선']] 
# sub.to_csv('Busan_subway1.csv')

#No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,비고,
# S_sub,D_sub,Address,Routing,longitude,latitude,
# Unnamed: 20,Unnamed: 21,Unnamed: 22,Unnamed: 23,Unnamed: 24,Unnamed: 25
Gucheong_info = load_gu_info()
Gucheong_info.rename(columns={'Latitude':'longitude', 'Longitude':'latitude'}, inplace=True)
# Gucheong_info.drop(['Unnamed: 20','Unnamed: 21','Unnamed: 22','Unnamed: 23','Unnamed: 24','Unnamed: 25'], \
#                 axis=1, inplace=True)
Gucheong_info = Gucheong_info[['Name', 'Address', 'latitude', 'longitude', 'count']]

# print(Gucheong_info.info())
# print(Gucheong_info['latitude'].sample(10))
Gucheong_info.to_csv('Gucheong_info.csv')