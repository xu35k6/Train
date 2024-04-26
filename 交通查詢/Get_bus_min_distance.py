from asyncio.windows_events import NULL
from cmath import nan
from math import cos
from turtle import distance
from datetime import datetime
from pprint import pprint
import pandas as pd
import requests
from math import cos, sin, radians, asin, sqrt
import time

from Get_log_lat import Get_log_lat
from bus import Get_bus
from Transfer import tranfer
#用google_map_api找出步行距離最近的10個站點
google_api_key = ''
def google_api(origins_Longitude,origins_Latitude,min_25):
    destinations = min_25[0][0]
    origins = str(origins_Latitude) + '+' + str(origins_Longitude)
    i = 1
    while(i<len(min_25)-1):
        destinations += '%7C'
        destinations += min_25[i][0]
        i+=1
    
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?mode=walking&origins="+origins+"&destinations="+destinations+"&units=METRIC&key={google_api_key}"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    min_10 = []
    #response.json()['rows'][0]['elements'][i]['duration']['value']是步行時間
    for i in range(24):
        min_10.append([(response.json()['rows'][0]['elements'][i]['duration']['value']),min_25[i][1]])
    min_10.sort()
    return min_10[:25]

#找出直線距離最近的25個站點
def min_distance_25(origins_Longitude,origins_Latitude):
    station = pd.read_csv(r'C:\python\交通查詢\公車座標.csv')
    min_25 = []
    for i in range(3361):
        dlat = origins_Latitude - station['緯度'][i]
        dlon = origins_Longitude - station['經度'][i]
        distance = ( 6371 * 2 * asin(sqrt((sin(dlat/2)**2 + cos(origins_Latitude) * cos(station['緯度'][i]) * sin(dlon/2)**2 ))))
        min_25.append([distance,station['站名'][i],station['座標'][i],station['緯度'][i],station['經度'][i]])

    min_25.sort()
    temp = []
    temp_station = []
    for i in range(25):
        temp_station.append(min_25[i][1])
        temp.append([min_25[i][2],min_25[i][1]])
    return temp_station,temp   
    
#找出該站所經過的所有公車
def has_bus(bus_station):
    all_bus = pd.read_csv(r"C:\python\交通查詢\公車站行駛路線.csv")
    bus_now = []
    bus_total = {}
    for k in range(len(bus_station)):
        bus_now = []
        for i in range(len(all_bus['站名'])):
            j = 1
            while(str(all_bus['路線'+str(j)][i]) != 'nan' and j < 44):
                if ( bus_station[k][1] == all_bus['站名'][i]):
                    if all_bus['路線'+str(j)][i] not in bus_now:
                        bus_total[str(bus_station[k][1])] = bus_now
                        bus_now.append(all_bus['路線'+str(j)][i])
                j+=1
    return bus_total

#不含步行資訊
def min_distance(o_bus,o_min_10,d_bus,d_min_10,d_name):
    temp = list(o_bus.keys()) #起點的所有站名
    bus_temp = []
    bus_time = ''
    min_distance_final = []

    for i in range(len(temp)):
        for j in range( len( o_bus[temp[i]] ) ):
            for k in range( len(list(d_bus.values()))):
                if o_bus[temp[i]][j] in bus_temp:
                    None
                #如果起終點公車路線重疊，將起點站存於bus_temp
                elif ( o_bus[temp[i]][j] in list(d_bus.values())[k] ):
                    bus_temp.append(o_bus[temp[i]][j])
                    #獲取公車即時時間
                    #bus1和bus0分別代表一個方向，若是單一方向僅會有bus0有資料
                    bus1,bus0  = Get_bus(o_bus[temp[i]][j])
                    
                    #用兩個for迴圈判斷起點至終點屬於哪個方向
                    #如果先讀到起點就存下來，然後break，若是先讀到終點就換讀下一個方向
                    has_a = False
                    has = False
                    num = 0
                    for a in range(len(bus1.name)):
                        if bus1.name[a] == temp[i]:
                            bus_time = bus1.time[a]
                            has = True
                            num = bus1.num[a]
                        elif bus1.name[a] == list(d_bus.keys())[k]:
                            if has :
                                has_a = True
                                num = bus1.num[a] - num
                            break
                    if not has_a:
                        for b in range(len(bus0.name)):
                            if bus0.name[b] == temp[i]:
                                bus_time = bus0.time[b]
                                num = bus0.num[b]
                            elif bus0.name[b] == list(d_bus.keys())[k]:
                                num = bus0.num[b] - num
                                break

                    #如果該班車能從起點到終點，則存於final，有些公車路線會經過起終點，但是是從終點往起點行駛。
                    if str(bus_time) != '休息' and bus_time != '':
                        min_distance_final.append('前往'+temp[i]+'搭乘:'+str(o_bus[temp[i]][j])+'號公車'+str(bus_time)+'，抵達'+list(d_bus.keys())[k]+'下車，後步行抵達'+d_name)
                    break
    return min_distance_final

#含及時公車資訊
def now_min_distance(o_bus,o_min_10,d_bus,d_min_10,d_name):
    temp = list(o_bus.keys())
    bus_temp = []
    bus_time = ''
    min_distance_final = []
    from bus import Get_bus
    for i in range(len(temp)):
        for j in range( len( o_bus[temp[i]] ) ):
            for k in range( len(list(d_bus.values()))):
                if o_bus[temp[i]][j] in bus_temp:
                    None
                #如果起終點公車路線重疊，將起點站存於bus_temp
                elif ( o_bus[temp[i]][j] in list(d_bus.values())[k] ):
                    bus_temp.append(o_bus[temp[i]][j])
                    #獲取公車即時時間
                    #bus1和bus0分別代表一個方向，若是單一方向僅會有bus0有資料
                    bus1,bus0  = Get_bus(o_bus[temp[i]][j])
                    
                    #用兩個for迴圈判斷起點至終點屬於哪個方向
                    #如果先讀到起點就存下來，然後break，若是先讀到終點就換讀下一個方向
                    for a in range(len(bus1.name)):
                        if bus1.name[a] == temp[i]:
                            bus_time = bus1.time[a]
                            break
                        elif bus1.name[a] == list(d_bus.keys())[k]:
                            break

                    for b in range(len(bus0.name)):
                        if bus0.name[b] == temp[i]:
                            bus_time = bus0.time[b]
                            break
                        elif bus0.name[b] == list(d_bus.keys())[k]:
                            break
                    
                    #如果該班車能從起點到終點，則存於final，有些公車路線會經過起終點，但是是從終點往起點行駛。
                    if bus_time != '' and bus_time != '休息':
                        min_distance_final.append('步行'+str(round(o_min_10[i][0] / 60))+'分'+str(o_min_10[i][0] % 60)+'秒前往'+temp[i]+'搭乘:'+str(o_bus[temp[i]][j])+'號公車'+str(bus_time)+'，前往'+list(d_bus.keys())[k]+'後步行'+str(round(d_min_10[k][0] / 60))+'分'+str(d_min_10[k][0] % 60)+'秒後抵達'+d_name)
                        bus_time = ''
                    break
    return min_distance_final

def Get_min_distance(destinations,d_name):
    start = time.time()
    #未來用line抓位置，現用中原大學的位置
    origins_Longitude = 121.24097447017819
    origins_Latitude = 24.95806922699817

    #設定終點經緯度
    destinations_Longitude = destinations[1]
    destinations_Latitude = destinations[0]

    #先算出當前直線距離最近的25個站點
    o_min_line = []
    d_min_line = []
    o_temp_station = []
    d_temp_station = []
    (o_temp_station,o_min_line) = min_distance_25(origins_Longitude,origins_Latitude)
    (d_temp_station,d_min_line) = min_distance_25(destinations_Longitude,destinations_Latitude)
    
    # #計算行程
  
    # #無即時公車資訊的行程計算
    min_distance_final = []
    # #找出這25個站點有的公車路線
    o_bus = has_bus(o_min_line)
    d_bus = has_bus(d_min_line)
    min_distance_final = min_distance(o_bus,o_min_line,d_bus,d_min_line,d_name)

    #即時公車資訊的行程計算

    #用google_map_api找出步行距離最近的25個站點
    # o_min_walk = google_api(origins_Longitude,origins_Latitude,o_min_line)
    # d_min_walk = google_api(destinations_Longitude,destinations_Latitude,d_min_line)
    # o_bus = has_bus(o_min_walk)
    # d_bus = has_bus(d_min_walk)
    # min_distance_final = now_min_distance(o_bus,o_min_walk,d_bus,d_min_walk,d_name)


    end1 = time.time()
    # if min_distance_final == []:
    #     for i in range(len(o_min_line)):
    #         for j in range(len(d_min_line)):
    #                 min_distance_final = tranfer(o_min_line[i][1],d_min_line[j][1])
    #                 pprint(min_distance_final)
    #                 break
    #         if min_distance_final != []:
    #             break
    # else:
    #     None
    if min_distance_final == []:
        min_distance_final = tranfer(o_temp_station,d_temp_station) 
    pprint(min_distance_final)

    end = time.time()
    print( 'min_distance:', format(end1-start),'\n'+'tranfer:',end-end1) 


if __name__ == '__main__':
    destinations = input('請輸入目的地:')

    LogandLat = Get_log_lat(destinations)
    Get_min_distance(LogandLat[0],destinations)
    time.sleep(100)



