#coding:utf-8
import data,time
from django.db.models import Q
from django.http import JsonResponse
from models import Action
import socket

INBED_TEMPERATURE_THRESHOD = 30
INBED_TEMPERATURE_WINDOW = 60    # s
CRY_SOUND_THRESHOD = 200
CRY_SOUND_WINDOW = 60
DEAMON_TIME_INTERVAL = 60




def pull():
    return 0

def bed_wetting(request):

    # waiting for future implemention
    resStub = {'errno':0,'res': '否'}
    return JsonResponse(resStub)

def temp(request):
    res = {'errno': 0}
    rjson  = data.getdata('temperature')

    if rjson == None or rjson['errno'] != 0:
        res['errno'] = 1
    else:
        temp = rjson['data']['datastreams'][0]['datapoints'][0]['value']
        res['res'] = round(temp,1)

    return JsonResponse(res)


def inBed(request):

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
            res['res'] = '是'
        else:
            res['res'] = '否'
    
    return JsonResponse(res)

def sleepTime(request):
    res = {'errno': 0}

    latestAction = Action.objects.order_by("-time").all()[:1][0]
    print latestAction.action_type
    if latestAction.action_type ==  'sleep':
        latestNotSleepAction = Action.objects.filter(~Q(action_type = 'sleep')).reverse()[:1][0]
        startTime = time.mktime(time.strptime(latestNotSleepAction.time,'%Y-%m-%dT%H:%M:%S'))
        #print time.mktime(time.localtime(time.time()))
        res['res'] = time.time()-startTime
    else:
        res['res'] = '没在睡觉啊'

    return JsonResponse(res)

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
            res['res'] = '是'
        else:
            res['res'] = '否'

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
            res['res'] = '是'
        else:
            res['res'] = '否'

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
    res = {'errno': 0}

    data = Action.objects.order_by("-time").all()[:100]
    
    array = []
    for item in data:
        dict = {}
        dict['time'] = item.time
        dict['action_type'] = item.action_type
        array.append(dict)
    array.reverse()
    res['data'] = array
    return JsonResponse(res)


def pull():
    current_time = time.time()
    
    rjson = data.getdata('sound,temperature',current_time , DEAMON_TIME_INTERVAL, 10)
    averageSound = calcAver(rjson['data']['datastreams'][0]['datapoints'])
    averageTem = calcAver(rjson['data']['datastreams'][1]['datapoints'])
    
    if averageSound < CRY_SOUND_THRESHOD and averageTem > INBED_TEMPERATURE_THRESHOD:
        action = Action(action_type='sleep')
    elif averageSound > CRY_SOUND_THRESHOD and averageTem > INBED_TEMPERATURE_THRESHOD:
        action = Action(action_type='cry')
    else:
        action = Action(action_type='missing')
    
    action.save()
    #print "pulling..."

def off(request):
    res = {'errno': 0}
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for data in ['0', '0', '0']:
        # 发送数据:
        s.sendto(data, ('192.168.137.2', 20000))
        # 接收数据:
    s.close()
    return JsonResponse(res)

def on(request):
    res = {'errno': 0}
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for data in ['1', '1', '1']:
        # 发送数据:
        s.sendto(data, ('192.168.137.2', 20000))
        # 接收数据:
    s.close()
    return JsonResponse(res)
