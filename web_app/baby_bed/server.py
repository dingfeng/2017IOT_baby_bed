#coding:utf-8
import data,time

from django.http import JsonResponse

INBED_TEMPERATURE_THRESHOD = 30
INBED_TEMPERATURE_WINDOW = 60    # s
CRY_SOUND_THRESHOD = 200
CRY_SOUND_WINDOW = 60

def pull():
    return 0

def bed_wetting(request):

    # waiting for future implemention
    resStub = {'res': 'False'}
    return JsonResponse(resStub)

def temp(request):
    res = {'errno': 0}
    rjson  = data.getdata('temperature')

    if rjson == None or rjson['errno'] != 0:
        res['errno'] = 1
    else:
        temp = rjson['data']['datastreams'][0]['datapoints'][0]['value']
        res['res'] = temp

    return JsonResponse(res)


def inBed():

    res = {'errno': 0}

    rjson = data.getdata('temperature', time.time(), INBED_TEMPERATURE_WINDOW, 10)

    if rjson == None or rjson['errno'] != 0:
        res['errno'] = 1

    elif rjson['data']['count'] == 0:
        res['errno'] = 2   # no data
        res['error'] = 'no data'

    else:
        averageTem = calcAver(rjson['data']['datastreams'][0]['datapoints'])
        if averageTem >= INBED_TEMPERATURE_THRESHOD:
            res['res'] = True
        else:
            res['res'] = False


def sleepTime(request):
    resStub = {'errno': 0}

    resStub['res'] = 6655
    return JsonResponse(resStub)

def isCry(request):
    res = {'errno': 0}
    rjson = data.getdata('sound', time.time(), INBED_TEMPERATURE_WINDOW, 10)

    if rjson == None or rjson['errno'] != 0:
        res['errno'] = 1

    elif rjson['data']['count'] == 0 :
        res['errno'] = 2   # no data
        res['error'] = 'no data'

    else:
        averageSound = calcAver(rjson['data']['datastreams'][0]['datapoints'])

        if averageSound >= CRY_SOUND_THRESHOD:
            res['res'] = True
        else:
            res['res'] = False

    return JsonResponse(res)


def isSleeping(request):

    res = {'errno': 0}
    rjson = data.getdata('sound,temperature', time.time(), INBED_TEMPERATURE_WINDOW, 10)

    if rjson == None or rjson['errno'] != 0:
        res['errno'] = 1

    elif rjson['data']['count'] == 0 :
        res['errno'] = 2   # no data
        res['error'] = 'no data'

    else:
        averageSound = calcAver(rjson['data']['datastreams'][0]['datapoints'])
        averageTem = calcAver(rjson['data']['datastreams'][1]['datapoints'])

        if averageSound < CRY_SOUND_THRESHOD and averageTem > INBED_TEMPERATURE_THRESHOD:
            res['res'] = True
        else:
            res['res'] = False

    return JsonResponse(res)



def calcAver(datapoints):

    #不存在为0的情况
    # if len(datapoints) == 0:
    #     return None

    total = 0
    for item in datapoints:
        total += item['value']

    return total/len(datapoints)


def history(request):
    return 0