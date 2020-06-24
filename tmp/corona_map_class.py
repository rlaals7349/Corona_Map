# -*- coding: utf-8 -*-
import requests
import json
import os 
import pandas as pd
import folium 
from folium import plugins
from folium.plugins import MarkerCluster
import re
import random

import datetime

from stations import stations, bfs
from functions import get_arrows, get_bearing, load_subway, load_busan_geojson, load_patient, load_gu_info
stations = stations

class MAP:
  def __init__(self):
    # 맵 생성
    self.default_lat = 35.1910526
    self.default_lon = 129.0662369

    self.busan_map = folium.Map( location=[ self.default_lat, self.default_lon ], 
                            zoom_start=13, max_zoom=15, min_zoom=10 )


  # 음영 생성
  def make_choropleth(self):
    gu_info = load_gu_info()
    busan_geojson = load_busan_geojson()
    # 구청자료에 있는 확진자 데이터 가지고 오기
    for i in range(len(gu_info)):
      if gu_info['count'][i]==0:
        gu_info['count'][i]=0

    # busan_geojson와 gu_info 의 구 이름 맞춰주기
    for i in range(len(gu_info)):
      gu_info['Name'][i]=gu_info['Name'][i][:-1]

    busan_map = initailize_Map()
    # 음영생성
    folium.Choropleth(
      geo_data=busan_geojson,
        name='구별 확진자 수(음영)',
        data=gu_info,
        columns=['Name', 'count'],
        key_on='feature.properties.name',
        fill_color='Reds',
        fill_opacity=0.4,

        line_opacity=1,
        line_weight=2,
        nan_fill_opacity=0,
        legend_name='구별 확진자 수'
    ).add_to(busan_map)
    return busan_map

  # 지하철 layer 생성
  def make_subway_layer(self):
    # 부산지하철 이름 및 위도 경도 불러오기
    sub = load_subway()
    subway_layer = folium.FeatureGroup(name="지하철")
    # 지하철 간 라인 생성
    # 1호선 (0~38)
    for i in range(0,39):
      p1=[sub[sub['호선']=='1호선']['위도'][i],sub[sub['호선']=='1호선']['경도'][i]]
      p2=[sub[sub['호선']=='1호선']['위도'][i+1],sub[sub['호선']=='1호선']['경도'][i+1]]
      subway_layer.add_child(folium.PolyLine([p1,p2], color="#F6531B", weight=5, opacity=0.8))
      busan_map.add_child(subway_layer)
    # 2호선
    for i in range(40,82):
      p1=[sub[sub['호선']=='2호선']['위도'][i],sub[sub['호선']=='2호선']['경도'][i]]
      p2=[sub[sub['호선']=='2호선']['위도'][i+1],sub[sub['호선']=='2호선']['경도'][i+1]]
      subway_layer.add_child(folium.PolyLine([p1,p2], color="#47DD77", weight=5, opacity=0.8))
      busan_map.add_child(subway_layer)
    # 3호선
    for i in range(83,99):
      p1=[sub[sub['호선']=='3호선']['위도'][i],sub[sub['호선']=='3호선']['경도'][i]]
      p2=[sub[sub['호선']=='3호선']['위도'][i+1],sub[sub['호선']=='3호선']['경도'][i+1]]
      subway_layer.add_child(folium.PolyLine([p1,p2], color="#ECBC26", weight=5, opacity=0.8))
      busan_map.add_child(subway_layer)
    # 4호선
    for i in range(100,113):
      p1=[sub[sub['호선']=='4호선']['위도'][i],sub[sub['호선']=='4호선']['경도'][i]]
      p2=[sub[sub['호선']=='4호선']['위도'][i+1],sub[sub['호선']=='4호선']['경도'][i+1]]
      subway_layer.add_child(folium.PolyLine([p1,p2], color="#2683EC", weight=5, opacity=0.8))
      busan_map.add_child(subway_layer)
    # 김해경전철
    for i in range(114,134):
      p1=[sub[sub['호선']=='김해경전철']['위도'][i],sub[sub['호선']=='김해경전철']['경도'][i]]
      p2=[sub[sub['호선']=='김해경전철']['위도'][i+1],sub[sub['호선']=='김해경전철']['경도'][i+1]]
      subway_layer.add_child(folium.PolyLine([p1,p2], color="#3B1ACC", weight=5, opacity=0.8))
      busan_map.add_child(subway_layer)
    # 동해선
    for i in range(135,148):
      p1=[sub[sub['호선']=='동해선']['위도'][i],sub[sub['호선']=='동해선']['경도'][i]]
      p2=[sub[sub['호선']=='동해선']['위도'][i+1],sub[sub['호선']=='동해선']['경도'][i+1]]
      subway_layer.add_child(folium.PolyLine([p1,p2], color="#B42BA7", weight=5, opacity=0.8))
      busan_map.add_child(subway_layer)

    # 라인 간 화살표 및 마커 생성
    # 1호선 (0~39)
    for i in range(0,40):
        # 지하철 마커생성
      subway_layer.add_child(folium.CircleMarker(
      location=[sub[sub['호선']=='1호선']['위도'][i], sub[sub['호선']=='1호선']['경도'][i]],radius=3, color="#F6471B", 
      fill_color='#FFFFFF', fill=True,opacity=1,))
      busan_map.add_child(subway_layer)
    # 2호선
    for i in range(41,83):
        # 지하철 마커생성
      subway_layer.add_child(folium.CircleMarker(
      location=[sub[sub['호선']=='2호선']['위도'][i],sub[sub['호선']=='2호선']['경도'][i]], radius=3, color='#2CBF5A', 
      fill_color='white', fill=True,opacity=1))
      busan_map.add_child(subway_layer)
    # 3호선
    for i in range(83,100):
        # 지하철 마커생성
      subway_layer.add_child(folium.CircleMarker(
      location=[sub[sub['호선']=='3호선']['위도'][i],sub[sub['호선']=='3호선']['경도'][i]], radius=3, color='#E1A411', 
      fill_color='white', fill=True,opacity=1))
      busan_map.add_child(subway_layer)
    # 4호선
    for i in range(100,114):
      #지하철 마커생성
      subway_layer.add_child(folium.CircleMarker(
      location=[sub[sub['호선']=='4호선']['위도'][i],sub[sub['호선']=='4호선']['경도'][i]], radius=3,color='#2683EC', 
      fill_color='white', fill=True,opacity=1))
      busan_map.add_child(subway_layer)
    # 김해경전철
    for i in range(114,135):
      #지하철 마커생성
      subway_layer.add_child(folium.CircleMarker(
      location=[sub[sub['호선']=='김해경전철']['위도'][i],sub[sub['호선']=='김해경전철']['경도'][i]], radius=3,color='#3B1ACC', 
      fill_color='white', fill=True,opacity=1))
      busan_map.add_child(subway_layer)
    # 동해선
    for i in range(135,149):
      #지하철 마커생성
      subway_layer.add_child(folium.CircleMarker(
      location=[sub[sub['호선']=='동해선']['위도'][i], sub[sub['호선']=='동해선']['경도'][i]], radius=3,color='#B42BA7', 
      fill_color='white', fill=True,opacity=1))
      busan_map.add_child(subway_layer)
    return subway_layer

  # 구청의 위치와 구청별 확진자 MarkerCluster layer 생성
  def make_MarkerCluster_layer(self):
    gu_info = load_gu_info()
    # MarkerCluster로와 구 layer 생성
    marker_cluster = MarkerCluster(name='구별 확진자 수', overlay=True,control=True).add_to(busan_map)

    # 구청별 MarkerCluster 생성
    for Gu_name in gu_info['Name']:
      gu_count=gu_info[gu_info['Name']==Gu_name]['count']
      for i in range(int(gu_count)):
        if i<=int(gu_count):
          folium.CircleMarker(location=[ float(gu_info[gu_info['Name']==Gu_name]['Longitude']),
                                        float(gu_info[gu_info['Name']==Gu_name]['Latitude']) ],
                                        radius=0.5,color='green').add_to(marker_cluster)

  # 확진자 layer 생성
  def make_patient_layer(selfZz):
    patient = load_patient()
    sub = load_subway()
    # 함수 만들기
    Total=folium.FeatureGroup(name="전체 확진자 동선")
    # 이것도 함수
    Week2=folium.FeatureGroup(name="최근 이주일 확진자 동선")
    # 함수
    want_date=['21','22','23','24','25','26','27','28','29','1','2','3','4','5','6']

    tooltip='정보 보기'

    for Number in range(1,len(patient['No'].unique())+1):
      r = lambda: random.randint(0,255)
      color_r='#%02X%02X%02X' % (r(),r(),r())
      one=patient[patient['No']=='부산-{0}'.format(Number)]  
      one_num='부산-'+str(Number)
      one_month=list(one['SMonth'].unique())
      one_day=list(one['SDate'].unique())
      day_len=len(one['SDate'].unique())

      for i in range(day_len):
        tmp=one[one['SDate']==one_day[i]]
        check=tmp['SDate'].unique()[0]
        date1 = one_day[i]
        
        if check in want_date: # 최근 일주일 이내에 발생한 경우
          coordis_except_sub=[]
          one_coordis=[]
          place1=[]
          address1=[]

          for index in tmp['latitude'].index:
            place2= tmp['Place'][index]
            if tmp['latitude'][index]==0:
              if tmp['Place'][index] =='도시철도':#철도 탄거 어펜드해야함
                
                start_name = tmp['D_sub'][index]
                goal_name = tmp['S_sub'][index]

                if start_name=='없음':

                  sub_index=sub[sub['역명']==goal_name].index
                  sub_lat=sub[sub['역명']==goal_name]['경도'][sub_index[0]]
                  sub_lon=sub[sub['역명']==goal_name]['위도'][sub_index[0]]
                  sub_coordi=[sub_lon,sub_lat]
                  one_coordis.append(sub_coordi)
                elif goal_name=='없음':

                  sub_index=sub[sub['역명']==start_name].index
                  sub_lat=sub[sub['역명']==start_name]['경도'][sub_index[0]]
                  sub_lon=sub[sub['역명']==start_name]['위도'][sub_index[0]]
                  sub_coordi=[sub_lon,sub_lat]
                  one_coordis.append(sub_coordi)

                elif start_name!='없음' and goal_name!='없음':

                  start = stations[start_name]
                  goal = stations[goal_name]

                  path = bfs(start, goal)
                  for station in path:
                    sub_index=sub[sub['역명']==station.name].index
                    sub_lat=sub[sub['역명']==station.name]['경도'][sub_index[0]]
                    sub_lon=sub[sub['역명']==station.name]['위도'][sub_index[0]]
                    sub_coordi=[sub_lon,sub_lat]
                    one_coordis.append(sub_coordi)

            elif tmp['latitude'][index]!=0:
              coordi=[tmp['longitude'][index],tmp['latitude'][index]]
              one_coordis.append(coordi)
              place1.append(tmp['Place'][index])
              address1.append(tmp['Address'][index])
              coordis_except_sub.append(coordi)

          # 지하철 포함 모든 좌표가 찍혀있는 one_coordis를 가지고 라인생성
          Week2.add_child(folium.PolyLine(one_coordis, color=color_r, weight=3, opacity=1))
          busan_map.add_child(Week2)

          # 지하철 좌표가 담겨있지 않는 데이터를 가지고 CircleMarker 생성
          for seq,coordi_except_sub in enumerate(coordis_except_sub):
            Week2.add_child(folium.CircleMarker(coordi_except_sub,color='red',radius=2,tooltip=tooltip,popup=folium.Popup(
            '확진자:{0},날짜:{1}일, 장소:{2},주소:{3}'.format(one_num,date1,place1[seq],address1[seq]),
            parse_html=True,max_width=450)))
            busan_map.add_child(Week2)
            # 화살표 생성        
            for length in range(len(one_coordis)-1):
              p1=[one_coordis[length][0], one_coordis[length][1]]
              p2=[one_coordis[length+1][0], one_coordis[length+1][1]]
              defi_arrows = get_arrows(color='black', size=1.5,locations=[p1,p2], n_arrows=2)
              for defi_arrow in defi_arrows:
                Week2.add_child(defi_arrow)
                busan_map.add_child(Week2)
            
        else: # 최근 일주일이 아닌 경우(전체)
          coordis_except_sub=[] # 지하철좌표를 제외한 전체 좌표
          one_coordis=[] # 전체좌표
          place1=[] # 데이터프레임에 있는 장소
          address1=[] # 데이터프레임에 있는 주소

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
                  sub_lat=sub[sub['역명']==goal_name]['경도'][sub_index[0]]
                  sub_lon=sub[sub['역명']==goal_name]['위도'][sub_index[0]]
                  sub_coordi=[sub_lon,sub_lat]
                  one_coordis.append(sub_coordi)
                  a+=1
                  # print("d_sub 추가")
                elif goal_name=='없음':

                  sub_index=sub[sub['역명']==start_name].index
                  sub_lat=sub[sub['역명']==start_name]['경도'][sub_index[0]]
                  sub_lon=sub[sub['역명']==start_name]['위도'][sub_index[0]]
                  sub_coordi=[sub_lon,sub_lat]
                  one_coordis.append(sub_coordi)
                  a+=1
                  # print("s_sub추가")
                elif start_name!='없음' and goal_name!='없음':

                  start = stations[start_name]
                  goal = stations[goal_name]

                  path = bfs(start, goal)
                  for station in path:
                    sub_index=sub[sub['역명']==station.name].index
                    sub_lat=sub[sub['역명']==station.name]['경도'][sub_index[0]]
                    sub_lon=sub[sub['역명']==station.name]['위도'][sub_index[0]]
                    sub_coordi=[sub_lon,sub_lat]
                    # print(sub_coordi)
                    one_coordis.append(sub_coordi)
                    # print("지하철 추가했을때")
                    a+=1

            # 좌표가 찍혀있으면 그 좌표를 one_coordis에 추가
            elif tmp['latitude'][index]!=0:
              coordi=[tmp['longitude'][index],tmp['latitude'][index]]
              one_coordis.append(coordi)
              place1.append(tmp['Place'][index])
              address1.append(tmp['Address'][index])
              coordis_except_sub.append(coordi)
          # 지하철 포함 모든 좌표가 찍혀있는 one_coordis를 가지고 라인생성
          Total.add_child(folium.PolyLine(one_coordis, color=color_r, weight=1.5, opacity=1))
          busan_map.add_child(Total)
          # 화살표 생성
          for length in range(len(one_coordis)-1):
            p1=[one_coordis[length][0], one_coordis[length][1]]
            p2=[one_coordis[length+1][0], one_coordis[length+1][1]]
            defi_arrows = get_arrows(color='black', size=1.5,locations=[p1,p2], n_arrows=2)
            for defi_arrow in defi_arrows:
              Total.add_child(defi_arrow)
              busan_map.add_child(Total)
          
          # 지하철 좌표가 담겨있지 않는 데이터를 가지고 CircleMarker 생성
          for seq,coordi_except_sub in enumerate(coordis_except_sub):
            Total.add_child(folium.CircleMarker(coordi_except_sub,color='red',radius=2,tooltip=tooltip,popup=folium.Popup(
            '확진자:{0},날짜:{1}일, 장소:{2},주소:{3}'.format(one_num,date1,place1[seq],address1[seq]),
            parse_html=True,max_width=450)))
            busan_map.add_child(Total)

    folium.LayerControl().add_to(busan_map)




