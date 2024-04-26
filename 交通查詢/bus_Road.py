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


client_id = ''
client_secret = ''


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


def bus():
    tdx = TDX(client_id, client_secret)

    base_url = "https://tdx.transportdata.tw/api"
    endpoint = "/basic/v2/Bus/EstimatedTimeOfArrival/InterCity/"
    OriginStationID = '1570'
    #https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/InterCity/1811?%24format=JSON
    
    url = f"{base_url}{endpoint}{OriginStationID}?$24format=JSON"
    response = tdx.get_response(url)
    return response

if __name__ == '__main__':
    result = bus()
    #FIXME 結論未完全
    for i in range(len(result)):
        for j in range(len(result)):
            if result[j]['Direction'] == 0:
                if result[j]['StopSequence'] == i:
                    try:
                        print(result[j]['StopSequence'],result[j]['StopName']['Zh_tw'],'\n',math.floor(result[j]['EstimateTime']/60),'分',result[j]['EstimateTime']%60,'秒\n')
                    except:
                        if result[j]['StopStatus'] == 3:
                            print(result[j]['StopSequence'],result[j]['StopName']['Zh_tw'],'\n','末班車駛離\n')
                        else:
                            print(result[j]['StopSequence'],result[j]['StopName']['Zh_tw'],'\n','error\n')





   
