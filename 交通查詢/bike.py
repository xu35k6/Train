import hmac
import base64
from re import A
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

        return response.json()['access_token']

    def get_response(self, url):
        headers = {'authorization': f'Bearer {self.get_token()}'}
        response = requests.get(url, headers=headers)
        return response.json()


def bike():
    tdx = TDX(client_id, client_secret)

    base_url = "https://tdx.transportdata.tw/api/basic/v2/Bike"
    bike_url = "/City/Taoyuan"

    url = f"{base_url}{'/Station'}{bike_url}?%24format=JSON"
    response_Station = tdx.get_response(url)
    
    station = ['TAO2005','TAO2004','TAO2012']
    hasbike = [False,False,False]
    #TAO2005:中原大學, TAO2004 : 中壢車站前站  ,TAO2012 : 中壢車站後站
    j = 0
    class Bike:
        Name = []
        Address = []
        Rent = []
        Return = []
    U_bike = Bike
    for No in station:
        for i in range(len(response_Station)):
            if response_Station[i]['StationUID'] == No:
                U_bike.Name.append(response_Station[i]['StationName']['Zh_tw'])
                U_bike.Address.append(response_Station[i]['StationAddress']['Zh_tw'])

                print('站名:',response_Station[i]['StationName']['Zh_tw'])
                print('位置:',response_Station[i]['StationAddress']['Zh_tw'])

        url = f"{base_url}{'/Availability'}{bike_url}?%24format=JSON"
        response_Availability = tdx.get_response(url)
        
        for i in range(len(response_Availability)):
            if response_Availability[i]['StationUID'] == No:
                U_bike.Rent.append(response_Availability[i]['AvailableRentBikes'])
                U_bike.Rent.append(response_Availability[i]['AvailableReturnBikes'])
                print('可租借數量:',response_Availability[i]['AvailableRentBikes'],'輛')
                print('可還車數量:',response_Availability[i]['AvailableReturnBikes'],'輛')
                google_map = f"{'https://www.google.com/maps/place/'}{response_Station[i]['StationPosition']['PositionLat']}{'+'}{response_Station[i]['StationPosition']['PositionLon']}"
                print(google_map,'\n')
    return U_bike

if __name__ == '__main__':
    U_bike = bike()
    # print(U_bike.Name)





   
