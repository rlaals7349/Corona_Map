```python
  # # 라인 간 화살표 및 마커 생성
  # # 1호선 (0~39)
  # for i in range(0,40):
  #     # 지하철 마커생성
  #   subway_layer.add_child(folium.CircleMarker(
  #   location=[sub[sub['호선']=='1호선']['위도'][i], sub[sub['호선']=='1호선']['경도'][i]],radius=2.5, color="#F6471B", 
  #   fill_color='#FFFFFF', fill=True,opacity=0.6))
  #   busan_map.add_child(subway_layer)
  # # 2호선
  # for i in range(41,83):
  #     # 지하철 마커생성
  #   subway_layer.add_child(folium.CircleMarker(
  #   location=[sub[sub['호선']=='2호선']['위도'][i],sub[sub['호선']=='2호선']['경도'][i]], radius=2.5, color='#2CBF5A', 
  #   fill_color='white', fill=True, opacity=0.6))
  #   busan_map.add_child(subway_layer)
  # # 3호선
  # for i in range(83,100):
  #     # 지하철 마커생성
  #   subway_layer.add_child(folium.CircleMarker(
  #   location=[sub[sub['호선']=='3호선']['위도'][i],sub[sub['호선']=='3호선']['경도'][i]], radius=2.5, color='#E1A411', 
  #   fill_color='white', fill=True,opacity=0.6))
  #   busan_map.add_child(subway_layer)
  # # 4호선
  # for i in range(100,114):
  #   #지하철 마커생성
  #   subway_layer.add_child(folium.CircleMarker(
  #   location=[sub[sub['호선']=='4호선']['위도'][i],sub[sub['호선']=='4호선']['경도'][i]], radius=2.5,color='#2683EC', 
  #   fill_color='white', fill=True,opacity=0.6))
  #   busan_map.add_child(subway_layer)
  # # 김해경전철
  # for i in range(114,135):
  #   #지하철 마커생성
  #   subway_layer.add_child(folium.CircleMarker(
  #   location=[sub[sub['호선']=='김해경전철']['위도'][i],sub[sub['호선']=='김해경전철']['경도'][i]], radius=2.5,color='#3B1ACC', 
  #   fill_color='white', fill=True,opacity=0.6))
  #   busan_map.add_child(subway_layer)
  # # 동해선
  # for i in range(135,149):
  #   #지하철 마커생성
  #   subway_layer.add_child(folium.CircleMarker(
  #   location=[sub[sub['호선']=='동해선']['위도'][i], sub[sub['호선']=='동해선']['경도'][i]], radius=2.5,color='#B42BA7', 
  #   fill_color='white', fill=True,opacity=0.6))
  #   busan_map.add_child(subway_layer)
```