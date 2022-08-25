from decimal import ROUND_DOWN
from re import A
from unicodedata import name
import requests
from datetime import datetime
from hashlib import sha1
import pandas as pd


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


def bus_RouteName(url):
    tdx = TDX(client_id, client_secret)
    #https://tdx.transportdata.tw/api/basic/v2/Bus/DisplayStopOfRoute/City/Taoyuan/155?%24format=JSON
    response = tdx.get_response(url)
    return response

from pprint import pprint
if __name__ == '__main__':
    with open( r"C:\python\交通查詢\bus_Route_station.csv", mode = "w",encoding = "utf-8" ) as file:
        file.write('車次\n')
    route = pd.read_csv(r"C:\python\交通查詢\bus_Route.csv")
    for i in range(len(route['公車班次'])):
        base_url = "https://tdx.transportdata.tw/api/basic/v2/Bus"
        endpoint = "/DisplayStopOfRoute/City/Taoyuan/"
        route = pd.read_csv(r"C:\python\交通查詢\bus_Route.csv")
        url = f"{base_url}{endpoint}{route['公車班次'][i]}?$24format=JSON"
        print(url)
        result = bus_RouteName(url)

        with open( r"C:\python\交通查詢\bus_Route_station.csv", mode = "a",encoding = "utf-8" ) as file:
            file.write(result[0]['RouteName']['Zh_tw'])

        for i in range(len(result[0]['Stops'])):
            with open( r"C:\python\交通查詢\bus_Route_station.csv", mode = "a",encoding = "utf-8" ) as file:
                file.write(','+result[0]['Stops'][i]['StopName']['Zh_tw'])
        with open( r"C:\python\交通查詢\bus_Route_station.csv", mode = "a",encoding = "utf-8" ) as file:
                file.write('\n')