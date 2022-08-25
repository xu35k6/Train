from asyncio.windows_events import NULL
from pickle import FALSE
from typing import final
import pandas as pd
from bus import Get_bus
import time
station = pd.read_csv(r"C:\python\交通查詢\公車能直達的站.csv",low_memory=False)
route = pd.read_csv(r"C:\python\交通查詢\公車站行駛路線.csv",low_memory=False)
all_bus = pd.read_csv(r"C:\python\交通查詢\公車站行駛路線.csv")

def has_bus(bus_station):
    bus_now = []
    bus_total = {}
    for k in range(len(bus_station)):
        bus_now = []
        for i in range(len(all_bus['站名'])):
            j = 1
            while(str(all_bus['路線'+str(j)][i]) != 'nan' and j < 44):
                if ( bus_station[k] == all_bus['站名'][i]):
                    if all_bus['路線'+str(j)][i] not in bus_now:
                        bus_total[str(bus_station[k])] = bus_now
                        bus_now.append(all_bus['路線'+str(j)][i])
                j+=1
    return bus_total

def bus_now(origin,origin_to_relay_route,relay_to_destination_route,destination):
    bus_temp = [] #存爬過的路線
    bus_time1 = ''
    bus_time = ''
    bus_name = ''
    bus_name1 = ''
    station_temp = []
    min_distance_final = []
    min_distance_final1 = []
    for i in origin_to_relay_route.keys():
        for j in origin_to_relay_route[i]:
            if j in bus_temp:
                None
            #如果起終點公車路線重疊，將起點站存於bus_temp
            else:
                #獲取公車即時時間
                #bus1和bus0分別代表一個方向，若是單一方向僅會有bus0有資料
                bus1,bus0  = Get_bus(j)
                #用兩個for迴圈判斷起點至終點屬於哪個方向
                #如果先讀到起點就存下來，然後break，若是先讀到終點就換讀下一個方向
                num = 0
                has = False
                a_has = False
                #FIXME 有可能存在其中一個路線方向有到起點但沒到終點 會影響判斷
                #FIXME 編號的判斷要修正
                for a in range(len(bus1.name)):
                    if bus1.name[a] in origin:
                        has = True
                        bus_time1 = bus1.time[a]
                        bus_name1 = bus1.name[a]
                        num = bus1.num[a]  
                    elif bus1.name[a] == i:
                        num = bus1.num[a] - num
                        if has :
                            a_has = True
                        break
                has = False
                if not a_has:
                    num = 0
                    for b in range(len(bus0.name)):
                        if bus0.name[b] in origin:
                            num = bus0.num[b]
                            bus_time1 = bus0.time[b]
                            bus_name1 = bus0.name[b]  
                        elif bus0.name[b] == i:
                            num = bus0.num[b] - num
                            break

                #如果該班車能從起點到終點，則存於final，有些公車路線會經過起終點，但是是從終點往起點行駛。
                if bus_time1 != '' and bus_time1 != '休息':
                    if i not in station_temp:
                        # bus_temp.append(j)
                        station_temp.append(i)
                    min_distance_final1.append(['前往 '+bus_name1+' 搭乘: '+str(j)+' 號公車: '+str(bus_time1)+'經過'+str(num-1)+'站，抵達 '+i,i])
                    bus_time1 = ''
                    num = 0
                    bus_name1 = ''
    end = ''
    for k in relay_to_destination_route.keys():
        if k in station_temp:
            for l in relay_to_destination_route[k]:
                if l in bus_temp:
                    None
                #如果起終點公車路線重疊，將起點站存於bus_temp
                else:
                    #獲取公車即時時間
                    #bus1和bus0分別代表一個方向，若是單一方向僅會有bus0有資料
                    bus1,bus0  = Get_bus(l)
                    #用兩個for迴圈判斷起點至終點屬於哪個方向
                    #如果先讀到起點就存下來，然後break，若是先讀到終點就換讀下一個方向
                    num = 0
                    has = False
                    a_has = False
                    for a in range(len(bus1.name)):
                        if bus1.name[a] in station_temp:
                            bus_time = bus1.time[a]
                            bus_name = bus1.name[a] 
                            num = bus1.num[a]
                            has = True 
                        elif bus1.name[a] in destination:
                            if has :
                                a_has = True
                            end = bus1.name[a]
                            break
                    if not a_has:
                        for b in range(len(bus0.name)):
                            if bus0.name[b] in station_temp:
                                bus_time = bus0.time[b]
                                bus_name = bus0.name[b]
                                num = bus0.num[b]       
                            elif bus0.name[b] in destination:
                                end =bus0.name[b]
                                num = bus0.num[b] - num
                                break

                    #如果該班車能從起點到終點，則存於final，有些公車路線會經過起終點，但是是從終點往起點行駛。
                    if bus_time != ''and str(bus_time) != '休息':
                        bus_temp.append(l)
                        min_distance_final.append([' 轉乘: '+str(l)+' 號公車: '+str(bus_time)+'經過'+str(num)+'站，抵達 '+end,bus_name])
                        bus_time = ''
                        end = ''
                        bus_name = ''
    min_distance_final_total = []
    for i in min_distance_final1:
        for j in min_distance_final:
            if i[1] == j[1]:
                min_distance_final_total.append(i[0]+j[0])
    return min_distance_final_total

def tranfer( origin_list,destination_list ):
    origin_station = []#起點能到的站
    destination_station = []#終點能到的站
    relay_station = [] #中繼站

    #算出起點終點能到的站
    for i in range(len(station)):
        if station['站點'][i] in origin_list:
            for j in range(725):
                if str(station['站點'+str(j+1)][i]) != 'nan' and str(station['站點'+str(j+1)][i]) not in origin_list:
                    origin_station.append(station['站點'+str(j+1)][i])
                    
        elif station['站點'][i] in destination_list:
            for j in range(725):
                if str(station['站點'+str(j+1)][i]) != 'nan'and str(station['站點'+str(j+1)][i]) not in destination_list:
                    destination_station.append(station['站點'+str(j+1)][i])
    #算出中繼站
    for i in range(len(origin_station)):
        if origin_station[i] in destination_station:
            relay_station.append(origin_station[i])

    if relay_station == []:
        print(origin_list,'無法轉乘',destination_list)
        return []

    #算出起點能到中繼站的路線和中繼站能到終點的路線
    relay_dir = {}
    relay_dir = has_bus(relay_station)
    origin_route = []
    destination_route = []
    for i in range(len(all_bus['站名'])):
        j = 1
        while(str(all_bus['路線'+str(j)][i]) != 'nan' and j < 44):
            if ( all_bus['站名'][i] in origin_list ):
                if all_bus['路線'+str(j)][i] not in origin_route:
                    origin_route.append(all_bus['路線'+str(j)][i])
            if all_bus['站名'][i] in destination_list :
                if all_bus['路線'+str(j)][i] not in destination_route:
                    destination_route.append(all_bus['路線'+str(j)][i])
            j+=1
    
    #算出那些路線能到哪些站
    min_distance_final = []
    origin_to_relay_route = {}
    relay_to_destination_route = {}
    temp = []
    for j in relay_dir.keys():
        temp = []
        for i in origin_route:
            if i in relay_dir[j]:
                origin_to_relay_route[j] = temp
                if i not in temp:
                    temp.append(i)

    temp = []
    for j in relay_dir.keys():
        temp = []
        for i in destination_route:
            if i in relay_dir[j]:
                relay_to_destination_route[j] = temp
                if i not in temp:
                    temp.append(i)
    min_distance_final = bus_now(origin_list,origin_to_relay_route,relay_to_destination_route,destination_list)

    return min_distance_final

from pprint import pprint
if __name__ == '__main__':
    start = time.time()
    origin = ['中原','老莊路739巷']
    destination = ['中原大學','中原大學']
    min_distance_final = tranfer(origin,destination)
    pprint(min_distance_final)
    end = time.time()
    print(end-start)









