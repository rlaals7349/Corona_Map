# -*- coding: utf-8 -*-
import requests
import json
import folium 
from folium.plugins import MarkerCluster
import re
import random
import pandas as pd
import datetime
from stations import stations, bfs
from functions import get_arrows, get_bearing
from functions import load_subway, load_busan_geojson, load_patient, load_gu_info
stations = stations
# 맵 만들기
def make_default_Map():

  # build map
  default_lat, default_lon = 35.1910526,129.0662369
  busan_map = folium.Map(location=[default_lat, default_lon], zoom_start=13, max_zoom=15, min_zoom=8)

  return busan_map

# 음영 생성
def make_choropleth(Map):
  # 데이터 로드
  gu_info = load_gu_info()
  busan_geojson = load_busan_geojson()

  # # 구청자료에 있는 확진자 데이터 가지고 오기
  # for i in range(len(gu_info)):
  #   if gu_info['count'][i]==0:
  #     gu_info['count'][i]=0

  # busan_geojson와 gu_info 의 구 이름 맞춰주기
  # for i in range(len(gu_info)):
  #   gu_info['Name'][i]=gu_info['Name'][i][:-1]

  # 맵 생성
  busan_map = Map

  # 음영생성
  folium.Choropleth(
    geo_data=busan_geojson,
      name='구별 확진자 수(음영)',
      data=gu_info,
      columns=['gu', 'count'],
      key_on='feature.properties.name',
      fill_color='Reds',
      fill_opacity=0.4,
      line_opacity=1,
      line_weight=0,
      nan_fill_opacity=0,
      legend_name='구별 확진자 수'
  ).add_to(busan_map)
  return busan_map

# 지하철 layer 생성
def make_subway_layer(Map):
  # 부산지하철 이름 및 longitude latitude 불러오기
  sub = load_subway()

  line1         =   sub[ sub['호선'] == '1호선' ]
  line2         =   sub[ sub['호선'] == '2호선' ]
  line3         =   sub[ sub['호선'] == '3호선' ]
  line4         =   sub[ sub['호선'] == '4호선' ]
  line_kimhae   =   sub[ sub['호선'] == '김해경전철' ]
  line_donghae  =   sub[ sub['호선'] == '동해선' ]

  busan_map = Map
  subway_layer = folium.FeatureGroup(name="지하철")
  opacity = 0.5

  # 1호선
  for i in range(0,40):
    subway_layer.add_child(folium.CircleMarker(
              location=[ line1['latitude'][i], line1['longitude'][i] ],
              radius=3, color="#F6471B", 
              fill_color='#FFFFFF', fill=True,opacity=opacity))

    try:
      p1=[ line1['latitude'][i]   ,  line1['longitude'][i] ]
      p2=[ line1['latitude'][i+1] ,  line1['longitude'][i+1] ]
      subway_layer.add_child(folium.PolyLine([ p1, p2 ], color="#F6531B", weight=5, opacity=opacity))
    except:
      pass
    busan_map.add_child(subway_layer)
  # 2호선
  for i in range(41,83):
    subway_layer.add_child(folium.CircleMarker(
              location=[ line2['latitude'][i], line2['longitude'][i] ], 
              radius=3, color='#47DD77', 
              fill_color='white', fill=True, opacity=opacity))
    busan_map.add_child(subway_layer)

    try:
      p1=[ line2['latitude'][i]   , line2['longitude'][i] ]
      p2=[ line2['latitude'][i+1] , line2['longitude'][i+1] ]
      subway_layer.add_child(folium.PolyLine([ p1, p2 ], color="#47DD77", weight=5, opacity=opacity))
    except:
      pass
  # 3호선
  for i in range(84,100):
    subway_layer.add_child(folium.CircleMarker(
              location=[ line3['latitude'][i], line3['longitude'][i] ], radius=3, color='#ECBC26', 
              fill_color='white', fill=True, opacity=opacity))

    try:
      p1=[ line3['latitude'][i]   , line3['longitude'][i] ]
      p2=[ line3['latitude'][i+1] , line3['longitude'][i+1] ]
      subway_layer.add_child(folium.PolyLine([ p1, p2 ], color="#ECBC26", weight=5, opacity=opacity))
    except:
      pass
  # 4호선
  for i in range(101,114):
    subway_layer.add_child(folium.CircleMarker(
              location=[ line4['latitude'][i],line4['longitude'][i] ], 
              radius=3, color='#2683EC', 
              fill_color='white', fill=True, opacity=opacity))

    try:
      p1=[ line4['latitude'][i]   ,  line4['longitude'][i] ]
      p2=[ line4['latitude'][i+1] ,  line4['longitude'][i+1] ]
      subway_layer.add_child(folium.PolyLine([ p1, p2 ], color="#2683EC", weight=5, opacity=opacity))
    except:
      pass
  # 김해경전철
  for i in range(115,135):
    subway_layer.add_child(folium.CircleMarker(
              location=[ line_kimhae['latitude'][i], line_kimhae['longitude'][i] ], 
              radius=3, color='#3B1ACC', 
              fill_color='white', fill=True, opacity=opacity))
    busan_map.add_child(subway_layer)
    
    try:
      p1=[ line_kimhae['latitude'][i]   ,  line_kimhae['longitude'][i] ]
      p2=[ line_kimhae['latitude'][i+1] ,  line_kimhae['longitude'][i+1] ]
      subway_layer.add_child(folium.PolyLine([p1,p2], color="#3B1ACC", weight=5, opacity=opacity))
    except:
      pass
  # 동해선
  for i in range(136,149):
    subway_layer.add_child(folium.CircleMarker(
              location=[ line_donghae['latitude'][i], line_donghae['longitude'][i] ], 
              radius=3, color='#B42BA7', 
              fill_color='white', fill=True, opacity=opacity))

    try:
      p1=[ line_donghae['latitude'][i]   ,  line_donghae['longitude'][i] ]
      p2=[ line_donghae['latitude'][i+1] ,  line_donghae['longitude'][i+1] ]
      subway_layer.add_child(folium.PolyLine([ p1, p2 ], color="#B42BA7", weight=5, opacity=opacity))
    except:
      pass
  busan_map.add_child(subway_layer)
  return busan_map

# 구청의 위치와 구청별 확진자 MarkerCluster layer 생성
def make_MarkerCluster_layer(Map):
  gu_info = load_gu_info()
  # MarkerCluster로와 구 layer 생성
  busan_map = Map
  marker_cluster = MarkerCluster(name='구별 확진자 수', overlay=True, control=True).add_to(busan_map)

  # 구청별 MarkerCluster 생성
  for Gu_name in gu_info['Name']:
    gu_count=gu_info[gu_info['Name']==Gu_name]['count']
    for i in range(int(gu_count)):
      if i<=int(gu_count):
        folium.CircleMarker(location=[ float(gu_info[gu_info['Name']==Gu_name]['latitude']),
                                       float(gu_info[gu_info['Name']==Gu_name]['longitude']) ],
                                       radius=0.5,color='green').add_to(marker_cluster)
  return busan_map

# 확진자 layer 생성
def make_patient_layer(Map):
  # stations  =  stations
  patient     =  load_patient()
  patient_num =  len(patient['No'].unique())
  sub         =  load_subway()
  busan_map   =  Map
  
  Total     =  folium.FeatureGroup(name="전체 확진자 동선", show=False)
  Week2     =  folium.FeatureGroup(name="최근 이주일 확진자 동선")
  # 함수
  want_date=['21','22','23','24','25','26','27','28','29','1','2','3','4','5','6']

  tooltip='정보 보기'

  for Number in range(1,patient_num+1):
    # r = lambda: random.randint(0,255)
    # color='#%02X%02X%02X' % (r(),r(),r())
    color = "#000000"

    one       =   patient[patient['No']=='부산-{0}'.format(Number)]  
    one_num   =   '부산-'+str(Number)
    one_month =   list(one['SMonth'].unique())
    one_day   =   list(one['SDate'].unique())
    day_len   =   len(one['SDate'].unique())

    for i in range(day_len):
      tmp=one[one['SDate']==one_day[i]]
      check=tmp['SDate'].unique()[0]
      date = one_day[i]
      
      if check in want_date: # 최근 일주일 이내에 발생한 경우
        coordis_except_sub  = []
        one_coordis         = []
        place_name          = []
        address             = []

        for index in tmp['longitude'].index:
          place2= tmp['Place'][index]
          if tmp['longitude'][index]==0:
            if tmp['Place'][index] =='도시철도':#철도 탄거 어펜드해야함
              
              start_name = tmp['D_sub'][index]
              goal_name = tmp['S_sub'][index]

              if start_name=='없음':

                sub_index=sub[sub['역명']==goal_name].index
                sub_lat=sub[sub['역명']==goal_name]['latitude'][sub_index[0]]
                sub_lon=sub[sub['역명']==goal_name]['longitude'][sub_index[0]]
                sub_coordi=[sub_lat,sub_lon]
                one_coordis.append(sub_coordi)
              elif goal_name=='없음':

                sub_index=sub[sub['역명']==start_name].index
                sub_lat=sub[sub['역명']==start_name]['latitude'][sub_index[0]]
                sub_lon=sub[sub['역명']==start_name]['longitude'][sub_index[0]]
                sub_coordi=[sub_lat,sub_lon]
                one_coordis.append(sub_coordi)

              elif start_name!='없음' and goal_name!='없음':

                start = stations[start_name]
                goal = stations[goal_name]

                path = bfs(start, goal)
                for station in path:
                  sub_index=sub[sub['역명']==station.name].index
                  sub_lat=sub[sub['역명']==station.name]['latitude'][sub_index[0]]
                  sub_lon=sub[sub['역명']==station.name]['longitude'][sub_index[0]]
                  sub_coordi=[sub_lat, sub_lon]
                  one_coordis.append(sub_coordi)

          elif tmp['latitude'][index]!=0:
            coordi=[tmp['latitude'][index],tmp['longitude'][index]]
            one_coordis.append(coordi)
            place_name.append(tmp['Place'][index])
            address.append(tmp['Address'][index])
            coordis_except_sub.append(coordi)

        # 지하철 포함 모든 좌표가 찍혀있는 one_coordis를 가지고 라인생성
        try:
          Week2.add_child(folium.PolyLine(one_coordis, color=color, weight=1, opacity=1))
        except:
          print("empty coordi in Week2 {}".format(one_num))
        busan_map.add_child(Week2)

        # 지하철 좌표가 담겨있지 않는 데이터를 가지고 CircleMarker 생성
        for seq,coordi_except_sub in enumerate(coordis_except_sub):
          Week2.add_child(folium.CircleMarker(coordi_except_sub,color='red', 
                                              radius=2,tooltip=tooltip,
                                              popup=folium.Popup(
          '확진자:{0},날짜:{1}일, 장소:{2},주소:{3}'.format(one_num,date,place_name[seq],address[seq]),
          parse_html=True,max_width=450)))
          busan_map.add_child(Week2)
          # 화살표 생성        
          # for length in range(len(one_coordis)-1):
          #   p1=[one_coordis[length][0], one_coordis[length][1]]
          #   p2=[one_coordis[length+1][0], one_coordis[length+1][1]]
          #   defi_arrows = get_arrows(locations=[p1,p2], color=color, size=1.4, n_arrows=2)
          #   for defi_arrow in defi_arrows:
          #     Week2.add_child(defi_arrow)
          #     busan_map.add_child(Week2)
          
      else: # 최근 일주일이 아닌 경우(전체)
        coordis_except_sub  = [] # 지하철좌표를 제외한 전체 좌표
        one_coordis         = [] # 전체좌표
        place_name          = [] # 데이터프레임에 있는 장소
        address             = [] # 데이터프레임에 있는 주소

        ## 확진자 한명의 하루 데이터에 좌표가 찍혀있는지 아닌지 확인

        # 좌표가 찍혀있지 않으면 S_sub, D_sub의 데이터 one_coordis에 추가
        for index in tmp['latitude'].index:
          place2= tmp['Place'][index]
          if tmp['latitude'][index]==0:
            if tmp['Place'][index] =='도시철도':#철도 탄거 어펜드해야함
              
              start_name = tmp['D_sub'][index]
              goal_name = tmp['S_sub'][index]

              if start_name=='없음':

                sub_index=sub[sub['역명']==goal_name].index
                sub_lat=sub[sub['역명']==goal_name]['latitude'][sub_index[0]]
                sub_lon=sub[sub['역명']==goal_name]['longitude'][sub_index[0]]
                sub_coordi=[sub_lat, sub_lon]
                one_coordis.append(sub_coordi)
                # a+=1
                # print("d_sub 추가")
              elif goal_name=='없음':

                sub_index=sub[sub['역명']==start_name].index
                sub_lat=sub[sub['역명']==start_name]['latitude'][sub_index[0]]
                sub_lon=sub[sub['역명']==start_name]['longitude'][sub_index[0]]
                sub_coordi=[sub_lat, sub_lon]
                one_coordis.append(sub_coordi)
                # a+=1
                # print("s_sub추가")
              elif start_name!='없음' and goal_name!='없음':

                start = stations[start_name]
                goal = stations[goal_name]

                path = bfs(start, goal)
                for station in path:
                  sub_index=sub[sub['역명']==station.name].index
                  sub_lat=sub[sub['역명']==station.name]['latitude'][sub_index[0]]
                  sub_lon=sub[sub['역명']==station.name]['longitude'][sub_index[0]]
                  sub_coordi=[sub_lat, sub_lon]
                  # print(sub_coordi)
                  one_coordis.append(sub_coordi)
                  # print("지하철 추가했을때")
                  # a+=1

          # 좌표가 찍혀있으면 그 좌표를 one_coordis에 추가
          elif tmp['latitude'][index]!=0:
            coordi=[tmp['latitude'][index],tmp['longitude'][index]]
            one_coordis.append(coordi)
            place_name.append(tmp['Place'][index])
            address.append(tmp['Address'][index])
            coordis_except_sub.append(coordi)
        # 지하철 포함 모든 좌표가 찍혀있는 one_coordis를 가지고 라인생성
        try:
          Total.add_child(folium.PolyLine(one_coordis, color=color, weight=1, opacity=1))
        except:
          print("empty coordi in Total {}".format(one_num))
        busan_map.add_child(Total)
        # 화살표 생성
        # for length in range(len(one_coordis)-1):
        #   p1=[one_coordis[length][0], one_coordis[length][1]]
        #   p2=[one_coordis[length+1][0], one_coordis[length+1][1]]
        #   defi_arrows = get_arrows(locations=[p1,p2], color=color, size=1.4, n_arrows=2)
        #   for defi_arrow in defi_arrows:
        #     Total.add_child(defi_arrow)
        #     busan_map.add_child(Total)
        
        # 지하철 좌표가 담겨있지 않는 데이터를 가지고 CircleMarker 생성
        for seq,coordi_except_sub in enumerate(coordis_except_sub):
          Total.add_child(folium.CircleMarker(coordi_except_sub,color='red',radius=2,tooltip=tooltip,popup=folium.Popup(
          '확진자:{0},날짜:{1}일, 장소:{2},주소:{3}'.format(one_num,date,place_name[seq],address[seq]),
          parse_html=True,max_width=450)))
          busan_map.add_child(Total)

  folium.LayerControl().add_to(busan_map)

  return busan_map