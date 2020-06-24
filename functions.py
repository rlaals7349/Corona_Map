import requests
import os 
import numpy as np 
import folium 
from folium import plugins
import re
import pandas as pd
import json
from collections import namedtuple
import datetime

today = datetime.datetime.today()
# 화살표 방향 설정
def get_bearing(p1, p2):

    long_diff = np.radians(p2.lon - p1.lon)
    
    lat1 = np.radians(p1.lat)
    lat2 = np.radians(p2.lat)
    
    x = np.sin(long_diff) * np.cos(lat2)
    y = (np.cos(lat1) * np.sin(lat2) 
        - (np.sin(lat1) * np.cos(lat2) 
        * np.cos(long_diff)))
    bearing = np.degrees(np.arctan2(x, y))
    
    if bearing < 0:
        return bearing + 360
    return bearing

# 화살표 만드는 함수 생성
def get_arrows(locations, color="#000000", size=6, n_arrows=3):
    
    Point = namedtuple('Point', field_names=['lat', 'lon'])
    
    p1 = Point(locations[0][0], locations[0][1])
    p2 = Point(locations[1][0], locations[1][1])
    
    rotation = get_bearing(p1, p2) - 90

    arrow_lats = np.linspace(p1.lat, p2.lat, n_arrows + 2)[1:n_arrows+1]
    arrow_lons = np.linspace(p1.lon, p2.lon, n_arrows + 2)[1:n_arrows+1]
    
    arrows = []

    for points in zip(arrow_lats, arrow_lons):
        arrows.append(folium.RegularPolygonMarker(location=points, 
                      fill_color=color, number_of_sides=3, 
                      radius=size, rotation=rotation))
    return arrows

def load_subway():
    subway = pd.read_csv(os.path.split(os.path.realpath(__file__))[0]+"\\datas\\Busan_subway.csv")
    return subway

def load_busan_geojson():
    # 행정구 나누는 데이터 불러오기
    with open(os.path.split(os.path.realpath(__file__))[0]+'\\datas\\Busan_gu.json',mode='rt',encoding='utf-8') as infile:
        busan_geojson=json.loads(infile.read())
    return busan_geojson

def load_gu_info():
    # 구청 데이터 불러오기(확진자 비율, 명수 포함되어 있음)
    gu_info=pd.read_csv(os.path.split(os.path.realpath(__file__))[0]+'\\datas\\Gucheong_info(20_03_06).csv')
    return gu_info

def load_patient():
    # 확진자 데이터 불러오기
    patient=pd.read_csv(os.path.split(os.path.realpath(__file__))[0]+'\\datas\\patient_info(20_03_06).csv')
    return patient

# 지하철 좌표 구하기
def make_subway_coordi():
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
def update_guinfo():
    gu_info = load_gu_info()
    patient = load_patient()
    idx=0
    while idx<len(gu_info):
        # 구청 주소 가지고 오기
        gu_address=gu_info['Address'][idx]
        # 키 요청
        KAKAO_API_KEY='725d861358777ff504771605f8c53f68'
        url = '''
        https://dapi.kakao.com/v2/local/search/address.json?query={0}
        '''.format(gu_address)
        headers={'Authorization': 'KakaoAK {0}'.format(KAKAO_API_KEY)}
        res=requests.get(url, headers=headers)
        res=res.json()
        # 주소를 좌표로 바꾸기
        gu_info['Latitude'][idx]  = res['documents'][0]['road_address']['x']
        gu_info['Longitude'][idx] = res['documents'][0]['road_address']['y']
        idx=idx+1
    print("updated {} info".format(idx))

    # 구청 정보 최신화

    gu_info['count']=0
    gu_info['Name'][6]='부산진구청'
    for i in range(1,len(patient['No'].unique())+1):
        patient_gu=patient[patient['No']=='부산-{0}'.format(i)]['Gu'].unique()
        for k in range(0,len(gu_info['Name'])):
            if patient_gu[0]==gu_info['Name'][k][:-1]:
                gu_info['count'][k]+=1

    # count가 제대로 됐는지 확인 -> 76명 중 거주지확인 불가 한명 제외하고 다 됨
    print(gu_info['count'].sum())

    # 날짜 최신화 시켜 저장하기
    date = datetime.datetime.today()
    gu_info.to_csv('/content/Gucheong_info({}-{}-{}).csv'.format(date.year,date.month,date.day))

##### 전체 확진자 데이터 가져온 후 위도 경도 입력하기
def add_patient_coordi_to_patient_data():
    patient = pd.read_csv('/content/patient_info(20_03_01).csv',encoding='utf-8')
    # 확진자들의 동선 주소를 입력-> 위도 경도를 GET-> 데이터프레임에 추가하기
    # 카카오 API 이용 -> 주소입력 후 좌표받기
    idx=0
    while idx<len(patient):
        # 도로명 주소 가지고오기
        address=patient['Address'][idx]
        if patient['Address'][idx] != '없음':
            # 키 요청
            KAKAO_API_KEY='725d861358777ff504771605f8c53f68'
            url = '''https://dapi.kakao.com/v2/local/search/address.json?query={0}'''.format(address)
            headers={'Authorization': 'KakaoAK {0}'.format(KAKAO_API_KEY)}
            res=requests.get(url, headers=headers)
            res=res.json()
            # 주소를 좌표로 바꾸기
            try:
                patient['latitude'][idx] = res['documents'][0]['road_address']['x']
                patient['longitude'][idx] = res['documents'][0]['road_address']['y']
                print(i,"번째 완료")
            except:
                print("{} index Error, Address : {} Place : {} ".format(idx,\
                                                                patient['Address'][idx],\
                                                                patient['Place'][idx]))
        else :
            patient['latitude'][idx] == 0
            patient['longitude'][idx] == 0
            idx = idx + 1

    patient.to_csv('/content/patient_info({}-{}-{}).csv'.format(today.year, today.month, today.day))