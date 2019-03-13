import requests
import json
import urllib3
import paho.mqtt.client as mqtt
import time
import datetime

file_object = open("url.txt", "r")
url = file_object.read()
file_object.close()
headers = {'content-type': 'application/json'}
broker_address='192.168.1.82'
moistval = 0
ljus = 0
temp = 0

    
ts = int(time.time())
print(ts)
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print(st)
                                                
broker_address='192.168.1.82'
client = mqtt.Client('P1')
client.connect(broker_address)
client.loop_start()
client.subscribe('vg/post')
client.subscribe('vg/fukt/jord')
client.subscribe('vg/temp')
client.subscribe('vg/ljus')

def changeMoist(val):
    global moistval
    moistval = float(val)

def changeLjus(val):
    global ljus
    ljus = val
def changeTemp(val):
    global temp
    temp = val
    
def on_message(client, userdata, message):
    print('mess:', str(message.payload.decode('utf-8')))
    print("topic "+message.topic)
    if(message.topic == 'vg/post'):
        postMoistToMQTT()
        
    if(message.topic == 'vg/fukt/jord'):
        changeMoist(message.payload.decode('utf-8'))
        print('moistval: '+moistval)
        postMoistToMQTT2(message.payload.decode('utf-8'))
    if(message.topic == 'vg/ljus'):
        changeLjus(message.payload.decode('utf-8'))
        print('ljus val: '+ljus)
    if(message.topic == 'vg/temp'):
        changeTemp(message.payload.decode('utf-8'))
        print('Temp val: '+temp)
        
def postToSensorApi(timestamp):
    dir={'MoistInt': 1, 'timestamp': timestamp}
    headers = {'content-type': 'application/json'}
    post = requests.post(url, data=json.dumps(dir), headers=headers).json()
    
    return post

def getSensorAPI():
    response = requests.get(url, headers).json()
    return response
    
def postToMQTT():
    print('posted: '+str(st))
    client.publish('vg/data', json.dumps(st))

def postMoistToMQTT():
    print('posted: ',moistval)
    return client.publish('vg/data/fukt', moistval)

print(getSensorAPI())
postMoistToMQTT()
client.on_message=on_message



