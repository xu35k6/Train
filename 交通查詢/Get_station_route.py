from cmath import nan
from re import A
import pandas as pd


bus_station_Name = pd.read_csv(r'C:\python\交通查詢\bus_station.csv')

bus_Route_Name = pd.read_csv(r'C:\python\交通查詢\bus_Route_station 1.csv')
with open( r"C:\python\交通查詢\station_route.csv", mode = "w",encoding = "utf-8" ) as file:
        file.write('站名\n') 

for j in range(len(bus_station_Name['站名'])):
    with open( r"C:\python\交通查詢\station_route.csv", mode = "a",encoding = "utf-8" ) as file:
        file.write(str(bus_station_Name['站名'][j])) 
    for k in range(len(bus_Route_Name['車次'])):
        i = 1
        while(i<158):
            if bus_Route_Name['站點'+str(i)][k] == bus_station_Name['站名'][j]:
                if str(bus_Route_Name['站點'+str(i)][k]) == 'nan':
                    break
                with open( r"C:\python\交通查詢\station_route.csv", mode = "a",encoding = "utf-8" ) as file:
                    file.write(','+bus_Route_Name['車次'][k])
            i+=1
    with open( r"C:\python\交通查詢\station_route.csv", mode = "a",encoding = "utf-8" ) as file:
                file.write('\n')




