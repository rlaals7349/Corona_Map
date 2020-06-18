from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
#################################
from django.http import JsonResponse
import urllib.request as ul
from urllib import parse
import json
import requests


@csrf_exempt
def phar(request):
    return render(request, "BS/phar.html")

@csrf_exempt
def phar2(request):
    return render(request, "BS/phar2.html")

@csrf_exempt
def pharmacy_data(request):
    
    addr = request.POST['addr']
    print(addr)
    lat = make_coordi(addr)[1]
    lng = make_coordi(addr)[0]
    meter = '2000'
    url="https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json?lat={}&lng={}&m={}".format(lat, lng, meter)
    # 요청
    request = ul.Request(url)
    # 응답
    response= ul.urlopen(request)
    # rescode = response.getcode()
    # 읽기
    responseData = response.read()
    # json 로드
    rDD = json.loads(responseData,encoding='utf-8')
    # print(rDD)
    
    test= list()
    
    for tmp in rDD['stores']:
        test1=dict()
        try:
            test1['set_lat'] = lat
            test1['set_lng'] = lng
            test1['name'] = tmp['name']
            test1['addr'] = tmp['addr']
            test1['lat'] = tmp['lat']
            test1['lng'] = tmp['lng']
            test1['stock_at'] = tmp['stock_at']
            chk=tmp['remain_stat']
            remain=''
            if chk =='plenty':
                remain='100개이상'
            elif chk =='some':
                remain='30개 이상 100개 미만'
            elif chk == 'few':
                remain='2개 이상 30개 미만'
            elif chk == 'empty':
                remain = '1개 이하'
            else:
                remain='판매중지'
            test1['remain_stat'] = remain
            test1['created_at'] = tmp['created_at']
            test.append(test1)
        except:
            pass
    # test = list(test)
    # print(test)
    print(test1['lat'])
    return JsonResponse({"data":test})        


def make_coordi(address):
    # address='부산광역시 부산진구 동평로'
    KAKAO_API_KEY='5f402e891888ce17295be347caa6a9d4'
    url = '''https://dapi.kakao.com/v2/local/search/keyword.json?query={0}'''.format(address)
    headers={'Authorization': 'KakaoAK {0}'.format(KAKAO_API_KEY)}

    res=requests.get(url, headers=headers)
    res=res.json()

    # print(res)

    x = res['documents'][0]['x']
    y = res['documents'][0]['y']
    # print(x, y)
    return x, y



@csrf_exempt
def index(request):
    return render(request, "BS/index.html")

@csrf_exempt
def More(request):
    return render(request, "BS/More.html")