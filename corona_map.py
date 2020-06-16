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
import time

# from beautifultable import BeautifulTable
# 시작
# 지하철 좌표 구하기
def make_subway():
  # 다른 데이터로 부산 지하철역 주소를 통해 좌표 획득하기
  df=pd.read_csv('/content/Busan_subway.csv')

  # 필요한 자료만 GET
  sub_name=df['역명']
  sub_add=df['역주소']
  sub=pd.concat([sub_name,sub_add],axis=1)

  # 완료한 파일 저장
  sub.to_csv('/content/Busan_subway.csv')

  KAKAO_API_KEY='725d861358777ff504771605f8c53f68'
  url = '''https://dapi.kakao.com/v2/local/search/address.json?query={0}'''.format('부산광역시 금정구 중앙대로 1927-1')
  headers={'Authorization': 'KakaoAK {0}'.format(KAKAO_API_KEY)}
  res=requests.get(url, headers=headers)
  res=res.json()

  x = res['documents'][0]['road_address']['x']
  y = res['documents'][0]['road_address']['y']
  # 카카오 API 이용하여 주소입력 후 좌표받기
  subway_x=[]
  subway_y=[]
  i=0
  while i<len(sub):
    # 도로명 주소 가지고오기
    subway_address=sub['역주소'][i]
    # 키 요청
    KAKAO_API_KEY='725d861358777ff504771605f8c53f68'
    url = '''
    https://dapi.kakao.com/v2/local/search/address.json?query={0}
    '''.format(subway_address)
    headers={'Authorization': 'KakaoAK {0}'.format(KAKAO_API_KEY)}
    res=requests.get(url, headers=headers)
    res=res.json()
    # 주소를 좌표로 바꾸기
    try:
      x = res['documents'][0]['road_address']['x']
      y = res['documents'][0]['road_address']['y']
      subway_x.append(x)
      subway_y.append(y)
      print(i,"번째 완료")
      print("좌표는",x,y)
    except:
      print(i,"번째 에러남. 역이름:",sub_name[i], "역주소 :",sub_add[i])
      subway_x.append(0)
      subway_y.append(0)
    i = i + 1

  # 경도, 위도 합치기
  sub['경도']=subway_x
  sub['위도']=subway_y

  # 경도가 0인 것 -> 에러난 것이므로 확인
  print(sub[sub['경도']==0]['역주소'])

  print(sub.loc[36,'역주소'])

  # 에러난 주소 수정 후 다시 돌리기
  sub.loc[36,'역주소']='부산광역시 금정구 중앙대로 1927-1'
  sub.loc[37,'역주소']='부산광역시 금정구 중앙대로 2019-1'
  sub.loc[38,'역주소']='부산광역시 금정구 중앙대로 2107'
  sub.loc[106,'역주소']='부산광역시 금정구 반송로 387'
  sub.loc[107,'역주소']='부산광역시 금정구 반송로 465'

  # 확인해보니 전부 False임
  print(sub['경도']==0)

  # 저장하기
  sub.to_csv('/content/Busan_subway.csv')

##### 구청별 확진자 수 체크
def update_save_guinfo():
  gu_info=pd.read_csv('/content/Gucheong_info(20_03_06).csv',encoding='euc-kr')
  i=0
  while i<len(gu_info):
    # 구청 주소 가지고 오기
    gu_address=gu_info['Address'][i]
    # 키 요청
    KAKAO_API_KEY='725d861358777ff504771605f8c53f68'
    url = '''
    https://dapi.kakao.com/v2/local/search/address.json?query={0}
    '''.format(gu_address)
    headers={'Authorization': 'KakaoAK {0}'.format(KAKAO_API_KEY)}
    res=requests.get(url, headers=headers)
    res=res.json()
    # 주소를 좌표로 바꾸기
    gu_info['Latitude'][i]= res['documents'][0]['road_address']['x']
    gu_info['Longitude'][i] = res['documents'][0]['road_address']['y']
    i=i+1

  # 구청 정보 최신화

  gu_info['count']=0
  gu_info['Name'][6]='부산진구청'
  for i in range(1,len(definite['No'].unique())+1):
    definite_gu=definite[definite['No']=='부산-{0}'.format(i)]['Gu'].unique()
    for k in range(0,len(gu_info['Name'])):
      if definite_gu[0]==gu_info['Name'][k][:-1]:
        gu_info['count'][k]+=1

  # count가 제대로 됐는지 확인 -> 76명 중 거주지확인 불가 한명 제외하고 다 됨
  print(gu_info['count'].sum())

  # 날짜 최신화 시켜 저장하기
  gu_info.to_csv('/content/Gucheong_info(20_03_06).csv')


##### 전체 확진자 데이터 가져온 후 위도 경도 입력하기

definite = pd.read_csv('/content/patient_info(20_03_01).csv',encoding='utf-8')

# 확진자들의 동선 주소를 입력하여 위도 경도를 GET하여 데이터프레임에 추가하기
# 카카오 API 이용하여 주소입력 후 좌표받기
i=0
while i<len(definite):
  # 도로명 주소 가지고오기
  address=definite['Address'][i]
  if definite['Address'][i] != '없음':
    # 키 요청
    KAKAO_API_KEY='725d861358777ff504771605f8c53f68'
    url = '''https://dapi.kakao.com/v2/local/search/address.json?query={0}'''.format(address)
    headers={'Authorization': 'KakaoAK {0}'.format(KAKAO_API_KEY)}
    res=requests.get(url, headers=headers)
    res=res.json()
    # 주소를 좌표로 바꾸기
    try:
      definite['latitude'][i] = res['documents'][0]['road_address']['x']
      definite['longitude'][i] = res['documents'][0]['road_address']['y']
      
      print(i,"번째 완료")
      print("좌표는",lat,lon)
    except:
      print(i,"번째 에러남. 주소:",definite['Address'][i], 'Place : ',definite['Place'][i])
  else :
    definite['latitude'][i] == 0
    definite['longitude'][i] == 0
  i = i + 1

# 초기맵 만들기
def make_foliumMap():
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
      line_weight=2,
      nan_fill_opacity=0,
      legend_name='구별 확진자 수'
  ).add_to(busan_div)
  return sub, busan_gu, gu_info, definite, busan_div
sub, busan_gu, gu_info, definite, busan_div = make_foliumMap()

# 지하철 layer 생성
def make_subway_layer():
  subway = folium.FeatureGroup(name="지하철")
  # 지하철 간 라인 생성
  # 1호선
  for i in range(0,39):
    p1=[sub[sub['호선']=='1호선']['위도'][i],sub[sub['호선']=='1호선']['경도'][i]]
    p2=[sub[sub['호선']=='1호선']['위도'][i+1],sub[sub['호선']=='1호선']['경도'][i+1]]
    subway.add_child(folium.PolyLine([p1,p2], color="#F6531B", weight=5, opacity=0.8))
    busan_div.add_child(subway)
  # 2호선
  for i in range(40,82):
    p1=[sub[sub['호선']=='2호선']['위도'][i],sub[sub['호선']=='2호선']['경도'][i]]
    p2=[sub[sub['호선']=='2호선']['위도'][i+1],sub[sub['호선']=='2호선']['경도'][i+1]]
    subway.add_child(folium.PolyLine([p1,p2], color="#47DD77", weight=5, opacity=0.8))
    busan_div.add_child(subway)
  # 3호선
  for i in range(83,99):
    p1=[sub[sub['호선']=='3호선']['위도'][i],sub[sub['호선']=='3호선']['경도'][i]]
    p2=[sub[sub['호선']=='3호선']['위도'][i+1],sub[sub['호선']=='3호선']['경도'][i+1]]
    subway.add_child(folium.PolyLine([p1,p2], color="#ECBC26", weight=5, opacity=0.8))
    busan_div.add_child(subway)
  # 4호선
  for i in range(100,113):
    p1=[sub[sub['호선']=='4호선']['위도'][i],sub[sub['호선']=='4호선']['경도'][i]]
    p2=[sub[sub['호선']=='4호선']['위도'][i+1],sub[sub['호선']=='4호선']['경도'][i+1]]
    subway.add_child(folium.PolyLine([p1,p2], color="#2683EC", weight=5, opacity=0.8))
    busan_div.add_child(subway)
  # 김해경전철
  for i in range(114,134):
    p1=[sub[sub['호선']=='김해경전철']['위도'][i],sub[sub['호선']=='김해경전철']['경도'][i]]
    p2=[sub[sub['호선']=='김해경전철']['위도'][i+1],sub[sub['호선']=='김해경전철']['경도'][i+1]]
    subway.add_child(folium.PolyLine([p1,p2], color="#3B1ACC", weight=5, opacity=0.8))
    busan_div.add_child(subway)
  # 동해선
  for i in range(135,148):
    p1=[sub[sub['호선']=='동해선']['위도'][i],sub[sub['호선']=='동해선']['경도'][i]]
    p2=[sub[sub['호선']=='동해선']['위도'][i+1],sub[sub['호선']=='동해선']['경도'][i+1]]
    subway.add_child(folium.PolyLine([p1,p2], color="#B42BA7", weight=5, opacity=0.8))
    busan_div.add_child(subway)

  # 라인 간 화살표 및 마커 생성
  # 1호선
  for i in range(0,40):
      # 지하철 마커생성
    subway.add_child(folium.CircleMarker(
    location=[sub[sub['호선']=='1호선']['위도'][i], sub[sub['호선']=='1호선']['경도'][i]],radius=3, color="#F6471B", 
    fill_color='#FFFFFF', fill=True,opacity=1,))
    busan_div.add_child(subway)
  # 2호선
  for i in range(41,83):
      # 지하철 마커생성
    subway.add_child(folium.CircleMarker(
    location=[sub[sub['호선']=='2호선']['위도'][i],sub[sub['호선']=='2호선']['경도'][i]], radius=3, color='#2CBF5A', 
    fill_color='white', fill=True,opacity=1))
    busan_div.add_child(subway)
  # 3호선
  for i in range(83,100):
      # 지하철 마커생성
    subway.add_child(folium.CircleMarker(
    location=[sub[sub['호선']=='3호선']['위도'][i],sub[sub['호선']=='3호선']['경도'][i]], radius=3, color='#E1A411', 
    fill_color='white', fill=True,opacity=1))
    busan_div.add_child(subway)
  # 4호선
  for i in range(100,114):
    #지하철 마커생성
    subway.add_child(folium.CircleMarker(
    location=[sub[sub['호선']=='4호선']['위도'][i],sub[sub['호선']=='4호선']['경도'][i]], radius=3,color='#2683EC', 
    fill_color='white', fill=True,opacity=1))
    busan_div.add_child(subway)
  # 김해경전철
  for i in range(114,135):
    #지하철 마커생성
    subway.add_child(folium.CircleMarker(
    location=[sub[sub['호선']=='김해경전철']['위도'][i],sub[sub['호선']=='김해경전철']['경도'][i]], radius=3,color='#3B1ACC', 
    fill_color='white', fill=True,opacity=1))
    busan_div.add_child(subway)
  # 동해선
  for i in range(135,149):
    #지하철 마커생성
    subway.add_child(folium.CircleMarker(
    location=[sub[sub['호선']=='동해선']['위도'][i], sub[sub['호선']=='동해선']['경도'][i]], radius=3,color='#B42BA7', 
    fill_color='white', fill=True,opacity=1))
    busan_div.add_child(subway)
  return subway

subway = make_subway_layer()
# 구청의 위치와 구청별 확진자 MarkerCluster layer 생성
def make_MarkerCluster_layer():

  # MarkerCluster로와 구 layer 생성
  marker_cluster = MarkerCluster(name='구별 확진자 수', overlay=True,control=True).add_to(busan_div)

  # 구청별 MarkerCluster 생성
  for Gu_name in gu_info['Name']:
    gu_count=gu_info[gu_info['Name']==Gu_name]['count']
    for i in range(int(gu_count)):
      if i<=int(gu_count):
        folium.CircleMarker(location=[ float(gu_info[gu_info['Name']==Gu_name]['Longitude']),
                                      float(gu_info[gu_info['Name']==Gu_name]['Latitude']) ],
                                      radius=0.5,color='green').add_to(marker_cluster)

# 확진자 layer 생성

def patient_layer():
  Total=folium.FeatureGroup(name="전체 확진자 동선")
  Week2=folium.FeatureGroup(name="최근 이주일 확진자 동선")
  want_date=['21','22','23','24','25','26','27','28','29','1','2','3','4','5','6']
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
        Week2.add_child(folium.PolyLine(one_coordis, color=color_r, weight=3, opacity=1))
        busan_div.add_child(Week2)

        # 지하철 좌표가 담겨있지 않는 데이터를 가지고 CircleMarker 생성
        for seq,coordi_except_sub in enumerate(coordis_except_sub):
          Week2.add_child(folium.CircleMarker(coordi_except_sub,color='red',radius=2,tooltip=tooltip,popup=folium.Popup(
          '확진자:{0},날짜:{1}일, 장소:{2},주소:{3}'.format(one_num,date1,place1[seq],address1[seq]),
          parse_html=True,max_width=450)))
          busan_div.add_child(Week2)
          # 화살표 생성        
          for length in range(len(one_coordis)-1):
            p1=[one_coordis[length][0], one_coordis[length][1]]
            p2=[one_coordis[length+1][0], one_coordis[length+1][1]]
            defi_arrows = get_arrows(color='black', size=1.5,locations=[p1,p2], n_arrows=2)
            for defi_arrow in defi_arrows:
              Week2.add_child(defi_arrow)
              busan_div.add_child(Week2)
          
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

                start = Station[start_name]
                goal = Station[goal_name]

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


