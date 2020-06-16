from collections import namedtuple
import os 
import deque

# 1- station 클래스를 만듭시다.
class Station:
    # 초기값 설정 생성자를 통해 인스턴스 변수들을 생성, 설정해 줍니다.
    def __init__(self, name):
        self.name = name
        # 이웃 역들을 담고 있는 리스트
        self.neighbor = []

    def add_connection(self, another_station):
        self.neighbor.append(another_station)
        another_station.neighbor.append(self)

# 2- 파일 읽기

# station 사전 만들기 - station 사전을 만드는 이유는 각각의 역 이름과 각 역에 담긴 정보들(Station 클래스의 인스턴스)을 key - value 값으로 입력하기 위함입니다.
stations = {}

# station 파일을 읽어봅시다.
in_file = open(os.path.split(os.path.realpath(__file__))+"/datas/busan_jiha.txt",encoding="utf-8")

# add_connection 메소드를 활용하기 위해 이전 역과 현재 역으로 구분 시켜줄 필요가 있습니다.
# 물론, 현재 이전역은 없는 상태이므로 None으로 지정해줍니다.
previous_station = None

for line in in_file:
    temporary_line = line.strip().split("-")

    # 리스트를 각각의 역으로 변환시키고, 공백을 없애주기 위해 이중 반복문을 활용합시다.
    for line in temporary_line:
        station_line = line.strip()

        # current_station을 현재역의 정보를 담고있는 인스턴스 값으로 지정해줍니다.
        current_station = Station(station_line)

        # 각각의 역의 이름을 stations 사전의 key값으로 입력하는게 목적이었으므로
        # 아래와 같이 코드를 작성합니다.
        if station_line not in stations.keys():
        
            # 현재 역의 이름을 key값으로, 그 역의 정보(인스턴스)를 value로 저장합니다.
            stations[station_line] = current_station

        # 각 호선당 중복되는 역(환승 역)일 경우 에러가 발생하므로 경우를 나눠줘야 합니다.
        # 현재역은 이전에 정해줬던 역의 value값임을 선언해줘야
        # 자동 환승을 합니다. station[station_line] = current_station 으로 지정 할 경우
        # 환승하지 않습니다!
        elif station_line in stations.keys():
            current_station = stations[station_line]


        # 이전 역과 현재 역을 이웃역으로 엮어줘야 하나, 현재 이전 역은 None 이므로, 아래와 같이 조건문을 활용합니다.
        if previous_station != None:
            current_station.add_connection(previous_station)

        # 반복문을 돌면서 모든 역을 사전에입력시켜줘야 하므로 아래와 같이 코드를 작성합니다.
        previous_station = current_station

in_file.close()

# 3 - bfs 알고리즘 생성
def bfs(start, goal):
    # previous 사전의 역할은 각각의 역을 key - value 관계로 이어주는 것입니다.
    previous = {}
    queue = deque()
    # 현재 확인하고 있는 역은 없으니 None값으로 지정합니다.
    current = None

    # 현재 시작역과 연결된 역은 없다는 뜻입니다.
    previous[start] = None

    # 목표 역에 도달할때까지 queue를 통해 확인해야 하므로 시작역을
    # 확인열에 집어넣습니다.
    queue.append(start)

    while len(queue) > 0 and current != goal:
        # 여기서 current는 목표 역이 아니라고 판명된(queue 확인열을 통해) 역으로 지정됩니다.
        # 여기서 None값을 탈출하는 것이죠!
        current = queue.popleft()

        for neighbor in current.neighbor:
            # previous 사전을 만든 이유를 다시 봐야 합니다.
            # 각각의 역을 이웃지어 주는 역할이므로, 이웃역이 사전에 없을 경우 아래와 같은 식으로 코드를 작성합니다.
            if neighbor not in previous.keys():
                # 아직 확인을 하지 않은 역이므로 확인열에 넣고,
                queue.append(neighbor)

                # 사전에 추가합니다.
                previous[neighbor] = current

    if current == goal:
    # 경로를 만들어야 하는데 여기서 가장 적합한 툴은 리스트입니다.
    # 그러므로 리스트를 통해 경로를 작성해봅시다.
        path = [goal]

    # 다시 한 번, previous 사전의 역할을 생각해봅시다.
    # previous 사전은 각각의 역을 K - V 관계로 엮어주는 것이죠?
    # 고로 아래와 같이 목표역(goal)에 해당하는 value(이웃 역)이 있을 경우 경로를 만들 수 있기 떄문에
    # 아래와 같이 코드를 작성합니다. 다만 역 순서가 역순(reverse)으로 출력되니
    # 필요할 경우 reverse 메소드를 활용할 수 있겠네요!
        while previous[goal] != None:
            # goal을 목표역과 이웃된 역으로 재지정해줍니다.
            goal = previous[goal]
            path.append(goal)
        return path

    # 사전에 있는 모든 역을 확인했음에도 목표역을 찾지 못한 경우입니다.
    if current != goal:
        return None