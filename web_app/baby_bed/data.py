#coding:utf-8           

import requests
import time

device_id = '22956758'
url = 'http://api.heclouds.com/devices/{0}/datapoints'.format(device_id)

def get(headers = {}, params = {}):
    r = requests.get(url, headers = headers, params = params)
    return r.json() if r.ok else None

def post(headers = {}, params = {}):
    r = requests.post(url, headers = headers, params = params)
    return r.json() if r.ok else None


def getdata(datastream, end = None, range = None, limit = 1):

    #currentTime = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(time.time()))

    params = {
        'datastream_id': datastream,  # datastream id
        'start': time.strftime('%Y-%m-%dT%H:%M:%S',end - range),  # start time of the desired period (optional)
        'end': time.strftime('%Y-%m-%dT%H:%M:%S',end),  # end time of the desired period   (optional)
        'limit': limit,  # number of results
        'newadd': False,  # only see newly added records
        'sort': 'DESC',  # always want the latest
    }
    headers = {
        'api-key': '6rMeFGhOlDJjWt1EfmpfEu8hNTc='
        # 'api-key': 'zMKoOvZlUKXJ7v3=9ikrldSuNI4='
    }
    rjson = get(headers=headers, params=params)



