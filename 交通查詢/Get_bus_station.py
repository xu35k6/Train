from decimal import ROUND_DOWN
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
import math


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


def bus_station():
    tdx = TDX(client_id, client_secret)
    base_url = "https://tdx.transportdata.tw/api/basic/v2/Bus"
    endpoint = "/Station/City/Taoyuan"
    #station 有3361站
    #經過各站
    #https://tdx.transportdata.tw/api/basic/v2/Bus/DisplayStopOfRoute/City/Taoyuan/155?%24top=30&%24format=JSON
    
    url = f"{base_url}{endpoint}?$24format=JSON"
    response = tdx.get_response(url)
    return response

if __name__ == '__main__':
    result = bus_station()
    j = 0
    with open( r"C:\python\交通查詢\bus_station.csv", mode = "w",encoding = "utf-8" ) as file:
        file.write("站名,座標,緯度,經度\n")
    for i in range(len(result)):
        if i > 0 :
            p = True
            for k in range(i):
                if result[i]['StationName']['Zh_tw'] == result[i - 1 - k]['StationName']['Zh_tw']:
                    p = False
            if p:
                j+=1
                with open( r"C:\python\交通查詢\bus_station.csv", mode = "a",encoding = "utf-8" ) as file:
                    file.write(result[i]['StationName']['Zh_tw']+',')
                    file.write(str(result[i]['StationPosition']['PositionLat']))
                    file.write('+'+str(result[i]['StationPosition']['PositionLon'])+',')
                    file.write(str(result[i]['StationPosition']['PositionLat']))
                    file.write(','+str(result[i]['StationPosition']['PositionLon'])+"\n")            
    print(j)