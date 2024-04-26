import hmac
import base64
from re import A
from unicodedata import name
import requests
from datetime import datetime
from hashlib import sha1
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import random


client_id = 's10811245-06dd52d5-3521-4239'
client_secret = '88ab73bb-bb40-4117-bf56-877c8030ad75'


class TDX():
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self):
        token_url = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(token_url, headers=headers, data=data)
        # print(response.status_code)
        # print(response.json())
        return response.json()['access_token']

    def get_response(self, url):
        headers = {'authorization': f'Bearer {self.get_token()}'}
        response = requests.get(url, headers=headers)
        return response.json()


def Get_bus(num):
    # bus0/1 代表順逆向
    tdx = TDX(client_id, client_secret)

    base_url = "https://tdx.transportdata.tw/api"
    endpoint = "/basic/v2/Bus/EstimatedTimeOfArrival/City/Taoyuan/"
    OriginStationID = num
    #https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/City/Taoyuan/156?%24top=30&%24format=JSON
    
    url = f"{base_url}{endpoint}{OriginStationID}?$24format=JSON"
    response = tdx.get_response(url)

    if len(response) == 0:
        print('查無此班次資料')
        quit()

    class Bus1:
        num = []
        time = [] 
        name = []
    class Bus0:
        num = []
        time = [] 
        name = []
    

    bus_1 = Bus1()
    for i in range(len(response)):
        for j in range(len(response)):
            if response[j]['Direction'] == 1 and response[j]['StopSequence'] == i and response[j]['StopSequence'] not in bus_1.num:
                bus_1.num.append(response[j]['StopSequence'])
                bus_1.name.append(response[j]['StopName']['Zh_tw'])
                try:
                    bus_1.time.append('預計再過'+str(round(response[j]['Estimates'][0]['EstimateTime']/60))+'分進站')
                except:
                    try:
                        bus_1.time.append('下一班次預計'+response[j]['NextBusTime'][11:16]+'進站')
                    except:
                        bus_1.time.append( '休息')
    bus_0 = Bus0()
    for i in range(len(response)):
        for j in range(len(response)):
            if response[j]['Direction'] == 0 and response[j]['StopSequence'] == i and response[j]['StopSequence'] not in bus_0.num :
                bus_0.num.append(response[j]['StopSequence'])
                bus_0.name.append(response[j]['StopName']['Zh_tw'])
                try:
                    bus_0.time.append('預計再過'+str(round(response[j]['Estimates'][0]['EstimateTime']/60))+'分進站')
                except:
                    try:
                        bus_0.time.append('下一班次預計'+response[j]['NextBusTime'][11:16]+'進站')
                    except:
                       bus_0.time.append( '休息')
    return [bus_0,bus_1]

if __name__ == '__main__':
    num = '301'
    bus_0,bus_1 = Get_bus(num)
    for i in range(len(bus_1.name)):
        try:
            print(bus_1.num[i],bus_1.name[i],bus_1.time[i])
        except:
            print(bus_1.name[i])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    for i in range(len(bus_0.name)):
        try:
            print(bus_0.num[i],bus_0.name[i],bus_0.time[i])
        except:
            print(bus_0.num[i],bus_0.name[i])

    



   
