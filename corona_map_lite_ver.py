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
import pandas as pd
from stations import Station, bfs
from functions import get_arrows, get_bearing

# Lite Version

# 부산지하철 이름 및 위도 경도 불러오기
sub=pd.read_csv('/content/drive/My Drive/Corona_Project/Busan_subway.csv')

# 행정구 나누는 데이터 불러오기
with open('/content/drive/My Drive/Corona_Project/Busan_gu.json',mode='rt',encoding='utf-8') as k:
  busan_gu=json.loads(k.read())

# 구청 데이터 불러오기(확진자 비율, 명수 포함되어 있음)
gu_info=pd.read_csv('/content/drive/My Drive/Corona_Project/Gucheong_info(20_03_06).csv')

# 확진자 데이터 불러오기
definite=pd.read_csv('/content/drive/My Drive/Corona_Project/patient_info(20_03_06).csv')

#----------------------------------------------------------------------------------------------

# 맵 생성
busan_div = folium.Map(location=[35.1910526,129.0662369], zoom_start=13, max_zoom=15, min_zoom=10)

# 구청자료에 있는 확진자 데이터 가지고 오기
for i in range(len(gu_info)):
  if gu_info['count'][i]==0:
    gu_info['count'][i]= 0

# busan_gu와 gu_info 의 구 이름 맞춰주기
for i in range(len(gu_info)):
  gu_info['Name'][i]=gu_info['Name'][i][:-1]

# 음영생성
folium.Choropleth(
  geo_data=busan_gu,
    name='구별 확진자 수(음영)',
    data=gu_info,
    columns=['Name', 'count'],
    key_on='feature.properties.name',
    fill_color='Reds',
    fill_opacity=0.4,
    line_opacity=1,
    line_weight=0,
    nan_fill_opacity=0,
    legend_name='구별 확진자 수',
    show=False
).add_to(busan_div)
#----------------------------------------------------------------------------------------------

# 지하철 간 라인 생성
# 1호선
for i in range(0,39):
  p1=[sub[sub['호선']=='1호선']['위도'][i],sub[sub['호선']=='1호선']['경도'][i]]
  p2=[sub[sub['호선']=='1호선']['위도'][i+1],sub[sub['호선']=='1호선']['경도'][i+1]]
  folium.PolyLine([p1,p2], color="#F6531B", weight=5, opacity=0.7).add_to(busan_div)
# 2호선
for i in range(40,82):
  p1=[sub[sub['호선']=='2호선']['위도'][i],sub[sub['호선']=='2호선']['경도'][i]]
  p2=[sub[sub['호선']=='2호선']['위도'][i+1],sub[sub['호선']=='2호선']['경도'][i+1]]
  folium.PolyLine([p1,p2], color="#47DD77", weight=5, opacity=0.7).add_to(busan_div)
# 3호선
for i in range(83,99):
  p1=[sub[sub['호선']=='3호선']['위도'][i],sub[sub['호선']=='3호선']['경도'][i]]
  p2=[sub[sub['호선']=='3호선']['위도'][i+1],sub[sub['호선']=='3호선']['경도'][i+1]]
  folium.PolyLine([p1,p2], color="#ECBC26", weight=5, opacity=0.7).add_to(busan_div)
# 4호선
for i in range(100,113):
  p1=[sub[sub['호선']=='4호선']['위도'][i],sub[sub['호선']=='4호선']['경도'][i]]
  p2=[sub[sub['호선']=='4호선']['위도'][i+1],sub[sub['호선']=='4호선']['경도'][i+1]]
  folium.PolyLine([p1,p2], color="#2683EC", weight=5, opacity=0.7).add_to(busan_div)
# 김해경전철
for i in range(114,134):
  p1=[sub[sub['호선']=='김해경전철']['위도'][i],sub[sub['호선']=='김해경전철']['경도'][i]]
  p2=[sub[sub['호선']=='김해경전철']['위도'][i+1],sub[sub['호선']=='김해경전철']['경도'][i+1]]
  folium.PolyLine([p1,p2], color="#3B1ACC", weight=5, opacity=0.7).add_to(busan_div)
# 동해선
for i in range(135,148):
  p1=[sub[sub['호선']=='동해선']['위도'][i],sub[sub['호선']=='동해선']['경도'][i]]
  p2=[sub[sub['호선']=='동해선']['위도'][i+1],sub[sub['호선']=='동해선']['경도'][i+1]]
  folium.PolyLine([p1,p2], color="#B42BA7", weight=5, opacity=0.7).add_to(busan_div)

# 라인 간 화살표 및 마커 생성
# 1호선
for i in range(0,40):
  folium.CircleMarker(
  location=[sub[sub['호선']=='1호선']['위도'][i], sub[sub['호선']=='1호선']['경도'][i]],radius=2.5, color="#F6681B").add_to(busan_div)
# 2호선
for i in range(41,83):
  folium.CircleMarker(
  location=[sub[sub['호선']=='2호선']['위도'][i],sub[sub['호선']=='2호선']['경도'][i]], radius=2.5, color='#2CBF5A').add_to(busan_div)
# 3호선
for i in range(83,100):
  folium.CircleMarker(
  location=[sub[sub['호선']=='3호선']['위도'][i],sub[sub['호선']=='3호선']['경도'][i]], radius=2.5, color='#E1A411').add_to(busan_div)
# 4호선
for i in range(100,114):
  folium.CircleMarker(
  location=[sub[sub['호선']=='4호선']['위도'][i],sub[sub['호선']=='4호선']['경도'][i]], radius=2.5,color='#2683EC').add_to(busan_div)
# 김해경전철
for i in range(114,135):
  folium.CircleMarker(
  location=[sub[sub['호선']=='김해경전철']['위도'][i],sub[sub['호선']=='김해경전철']['경도'][i]], radius=2.5, color='#3B1ACC').add_to(busan_div)
# 동해선
for i in range(135,149):
  folium.CircleMarker(
  location=[sub[sub['호선']=='동해선']['위도'][i], sub[sub['호선']=='동해선']['경도'][i]], radius=2.5,color='#B42BA7').add_to(busan_div)


# 구청의 위치와 구청별 확진자 MarkerCluster로 보여주기
marker_cluster = MarkerCluster(name='구별 확진자 수').add_to(busan_div)

# 구청별 MarkerCluster 생성
for Gu_name in gu_info['Name']:
  gu_count=gu_info[gu_info['Name']==Gu_name]['count']
  for i in range(int(gu_count)):
    if i<=int(gu_count):
      folium.CircleMarker(location=[ float(gu_info[gu_info['Name']==Gu_name]['Longitude']),
                                     float(gu_info[gu_info['Name']==Gu_name]['Latitude']) ],
                                     radius=0.5,color='red').add_to(marker_cluster)

#----------------------------------------------------------------------------------------------

# 확진자 지도
want_date=['23','24','25','26','27','28','29','1','2','3','4','5','6']
Total=folium.FeatureGroup(name="전체 확진자 동선",show=False)
tooltip='정보 보기'

for Number in range(1,len(definite['No'].unique())+1):
  r = lambda: random.randint(0,255)
  color_r='#%02X%02X%02X' % (r(),r(),r())
  one=definite[definite['No']=='부산-{0}'.format(Number)]  
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
      folium.PolyLine(one_coordis, color=color_r, weight=1.5, opacity=1).add_to(busan_div)

      # 지하철 좌표가 담겨있지 않는 데이터를 가지고 CircleMarker 생성
      for seq,coordi_except_sub in enumerate(coordis_except_sub):
        folium.CircleMarker(coordi_except_sub,color='red',
                            radius=1.5,tooltip=tooltip,popup=folium.Popup(
        '확진자:{0},날짜:{1}일, 장소:{2},주소:{3}'.format(
            one_num,date1,place1[seq],address1[seq]), 
            parse_html=True,max_width=450)).add_to(busan_div)

        # 화살표 생성
        for length in range(len(one_coordis)-1):
          p1=[one_coordis[length][0], one_coordis[length][1]]
          p2=[one_coordis[length+1][0], one_coordis[length+1][1]]
          defi_arrows = get_arrows(color='black', size=1.5,locations=[p1,p2], n_arrows=2)
          for defi_arrow in defi_arrows:
            defi_arrow.add_to(busan_div)
    else:
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

        # 좌표가 찍혀있으면 그 좌표를 one_coordis에 추가
        elif tmp['latitude'][index]!=0:
          coordi=[tmp['longitude'][index],tmp['latitude'][index]]
          one_coordis.append(coordi)
          place1.append(tmp['Place'][index])
          address1.append(tmp['Address'][index])
          coordis_except_sub.append(coordi)
      # 지하철 포함 모든 좌표가 찍혀있는 one_coordis를 가지고 라인생성
      Total.add_child(folium.PolyLine(one_coordis, color=color_r, weight=1.5, opacity=1))
      busan_div.add_child(Total)
      # 화살표 생성
      for length in range(len(one_coordis)-1):
        p1=[one_coordis[length][0], one_coordis[length][1]]  
        p2=[one_coordis[length+1][0], one_coordis[length+1][1]]
        defi_arrows = get_arrows(color='black', size=1.5,locations=[p1,p2], n_arrows=2)
        for defi_arrow in defi_arrows:
          Total.add_child(defi_arrow)
          busan_div.add_child(Total)
      
      # 지하철 좌표가 담겨있지 않는 데이터를 가지고 CircleMarker 생성
      for seq,coordi_except_sub in enumerate(coordis_except_sub):
        Total.add_child(folium.CircleMarker(coordi_except_sub,color='red',radius=2,tooltip=tooltip,popup=folium.Popup(
        '확진자:{0},날짜:{1}일, 장소:{2},주소:{3}'.format(one_num,date1,place1[seq],address1[seq]),
        parse_html=True,max_width=450)))
        busan_div.add_child(Total)

folium.LayerControl().add_to(busan_div)

busan_div.save('/content/Busan_TEST.html')
# busan_div



definite = pd.read_csv('/Users/rlaal/Dropbox/corona_project/develop/Workplace/patient_info(20_03_06)_.csv',encoding='utf-8')

print(datetime.datetime.year)
# definite['Datetime']=datetime.datetime()
# print(definite)
for Number in range(1,len(definite['No'].unique())+1):
  want_date=[]

  one=definite[definite['No']=='부산-{}'.format(Number)][['SMonth','SDate']]
  one_date=list(one['SDate'])
  one_month=list(one['SMonth'])

  defi_date=one_date
  defi_month=one_month

  # 현재 날짜
  d=datetime.date.today()

  for month, day in zip(defi_month,defi_date):

    try:
      d2=datetime.datetime(2020,int(month),int(day))
    except:
      print("확인중")
      continue

    if d2.month ==2:
      if d.toordinal()-d2.toordinal()<14:
        # print(d.toordinal()-d2.toordinal(),'일 전')
        want_date.append(one['SDate'].unique())
        
    elif d2.month ==3:
      if d.toordinal()-d2.toordinal()<14:
        # print(d.toordinal()-d2.toordinal(),'일 전')
        want_date.append(one['SDate'].unique())
  # print(Number,'번째 환자 끝')
  # print('*'*40)
# print(want_date)

# definite.to_csv('/Users/rlaal/Dropbox/corona_project/develop/Workplace/patient_info(20_03_06)_.csv')