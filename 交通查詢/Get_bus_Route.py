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


def Get_bus_Route():
    tdx = TDX(client_id, client_secret)
    base_url = "https://tdx.transportdata.tw/api/basic/v2/Bus"
    endpoint = "/Route/City/Taoyuan"
    url = f"{base_url}{endpoint}?$24format=JSON"
    #https://tdx.transportdata.tw/api/basic/v2/Bus/Route/City/Taoyuan?%24format=JSON
    response = tdx.get_response(url)
    return response

from pprint import pprint
if __name__ == '__main__':
    result = Get_bus_Route()
    # print(result)
    with open( r"C:\python\交通查詢\bus_Route.csv", mode = "w",encoding = "utf-8" ) as file:
        file.write('公車班次'+'\n')
    for i in range(len(result)):
        with open( r"C:\python\交通查詢\bus_Route.csv", mode = "a",encoding = "utf-8" ) as file:
            file.write(result[i]['SubRoutes'][0]['SubRouteName']['Zh_tw']+'\n')


