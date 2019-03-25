import requests
import json
import urllib3
import paho.mqtt.client as mqtt
import time
import datetime
import os
import sys

#file_object = open("url.txt", "r")
#url1 = file_object.read()
#file_object.close()
url1 = "http://webplant.azurewebsites.net/api/PlantSensorData1"
url2 = "http://webplant.azurewebsites.net/api/PlantSensorData2"
url3 = "http://webplant.azurewebsites.net/api/PlantSensorData3"

headers = {'content-type': 'application/json'}
broker_address='192.168.1.12'

ts = int(time.time())
tim = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
client = mqtt.Client('P1')
client.connect(broker_address)
client.loop_start()
client.subscribe('vg/post')

for number in range(1,4):
    client.subscribe('vg/planta%d/fukt/luft'%(number))
    client.subscribe('vg/planta%d/fukt/jord'%(number))
    client.subscribe('vg/planta%d/temp'%(number))
    client.subscribe('vg/planta%d/ljus'%(number))
    client.subscribe('vg/planta%d/move'%(number))

moist1 = 0
moist2 = 0
moist3 = 0
ljus1 = 0
ljus2 = 0
ljus3 = 0
temp1 = 0
temp2 = 0
temp3 = 0
hum1 = 0
hum2 = 0
hum3 = 0

def changeMoist1(val):
    global moist1
    moist1 = val
    return moist1

def changeLjus1(val):
    global ljus1
    ljus1 = val
    return ljus1

def changeTemp1(val):
    global temp1
    temp1 = val
    return temp1

def changeHum1(val):
    global hum1
    hum1 = val
    return hum1

def changeMoist2(val):
    global moist2
    moist2 = val
    return moist2

def changeLjus2(val):
    global ljus2
    ljus2 = val
    return ljus2

def changeTemp2(val):
    global temp2
    temp2 = val
    return temp2

def changeHum2(val):
    global hum2
    hum2 = val
    return hum2
    
def changeMoist3(val):
    global moist3
    moist3 = val
    return moist3

def changeLjus3(val):
    global ljus3
    ljus3 = val
    return ljus3

def changeTemp3(val):
    global temp3
    temp3 = val
    return temp3

def changeHum3(val):
    global hum3
    hum3 = val
    return hum3
    
def changeTime():
    global tim
    global ts
    ts = int(time.time())
    tim = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
num = 1
dickLjus = [changeLjus1, changeLjus2, changeLjus3]
dickMoist = [changeMoist1, changeMoist2, changeMoist3]
dickTemp = [changeTemp1, changeTemp2, changeTemp3]
dickHum = [changeHum1, changeHum2, changeHum3]

url = [url1, url2, url3]


def getSensorAPI():
        response1 = requests.get(url[0], headers).json()
        response2 = requests.get(url[1], headers).json()
        response3 = requests.get(url[2], headers).json()
        for m in range(0,10):
            for n in range(0, len(response3)):
                
                postToMQTT('vg/date' ,datetime.datetime.fromtimestamp(response1[0]['Timestamp']).strftime('%Y-%m-%d %H:%M:%S'))
                postToMQTT('vg/planta'+str(1)+'/fukt/jord1' ,response1[n]['Moist'])
                postToMQTT('vg/planta'+str(1)+'/fukt/luft1' ,response1[n]['Hum'])
                postToMQTT('vg/planta'+str(1)+'/temp1' ,response1[n]['Temp'])
                postToMQTT('vg/planta'+str(1)+'/ljus1' ,response1[n]['Light'])
                
                postToMQTT('vg/planta'+str(2)+'/fukt/jord1' ,response2[n]['Moist'])
                postToMQTT('vg/planta'+str(2)+'/fukt/luft1' ,response2[n]['Hum'])
                postToMQTT('vg/planta'+str(2)+'/temp1' ,response2[n]['Temp'])
                postToMQTT('vg/planta'+str(2)+'/ljus1' ,response2[n]['Light'])
                
                postToMQTT('vg/planta'+str(3)+'/fukt/jord1' ,response3[n]['Moist'])
                postToMQTT('vg/planta'+str(3)+'/fukt/luft1' ,response3[n]['Hum'])
                postToMQTT('vg/planta'+str(3)+'/temp1' ,response3[n]['Temp'])
                postToMQTT('vg/planta'+str(3)+'/ljus1' ,response3[n]['Light'])            
                time.sleep(5)
    
def postToMQTT(n, m):
    #response = getSensorAPI()
    #print(response)
    print('posted: '+str(n)+'Mess: '+str(m))
    print(client.publish(n, json.dumps(m)))

def on_message(client, userdata, message):
    print("topic: %s, message: %s"%(message.topic, message.payload.decode('utf-8')))
    
    if(message.topic == 'vg/post'):
        changeTime()
        #getSensorAPI()
        
    if((message.topic).startswith('vg/planta1')):
        updateValueFromTopic(0, message)
    if((message.topic).startswith('vg/planta2')):
        updateValueFromTopic(1, message)
    if((message.topic).startswith('vg/planta3')):
        updateValueFromTopic(2, message)

def updateValueFromTopic(number, message):
    changeTime();
    if('ljus' in message.topic):
        print('ljus: '+dickLjus[number](message.payload.decode('utf-8')))
    if('temp' in message.topic):
        print('Temp: '+dickTemp[number](message.payload.decode('utf-8')))
    if('luft' in message.topic):
        print('Hum: '+dickHum[number](message.payload.decode('utf-8')))
    if('jord' in message.topic):
        print('Jord: '+dickMoist[number](message.payload.decode('utf-8')))
        


def postToSensorApi():
    
    dick1 = [moist1, moist2, moist3]
    dick2 = [ljus1, ljus2, ljus3]
    dick3 = [temp1,  temp2,  temp3]
    dick4 = [hum1, hum2, hum3]
    
    for number in range(0,3):
        dir={'Pir': '0', 'Light': dick2[number],'Hum': dick4[number], 'Moist': dick1[number], 'Timestamp': ts, 'Temp': dick3[number]}
        headers = {'content-type': 'application/json'}
        print(dir)
        print(url[number])
        post = requests.post(url[number], data=json.dumps(dir), headers=headers).json()
    
    return post


getSensorAPI()
#print(postToSensorApi())

client.on_message=on_message
from threading import Timer

def timeout():
    print("-----------------------30 min check----------------------\n")
    print(postToSensorApi())
    timerfun()

def timerfun():
    t = Timer(1800, timeout)
    t.start()
    t.join()
timerfun()



