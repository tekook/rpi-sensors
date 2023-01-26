# -*- coding: utf-8 -*-
import json, os
from pprint import pprint
import socket
import time
from dotmap import DotMap
import paho.mqtt.client as mqtt
import libsensors as sensors
__config = False
__calls = False
__hostId = False
__errors = {}
def getConfig() -> DotMap:
    global __config
    if __config == False:
        print("Reading config...")
        d = os.path.dirname(os.path.realpath(__file__))
        f = open(d + "/config.json", "r")
        config = json.load(f)
        __config = DotMap(config, _dynamic=False)
        f.close()
    return __config

def getCalls():
    global __calls
    if __calls == False:
        __calls = {
            'sht4x':    {'func': sensors.getSHT4X, 'arg': False},
            'ltr390':   {'func': sensors.getLTR390, 'arg': False},
            'ds18b20':  {'func': sensors.getDS18B20, 'arg': False},
            'mcp9808':  {'func': sensors.getMCP9808, 'arg': False},
            'dps310':   {'func': sensors.getDPS310, 'arg': False},
            'bh1750':   {'func': sensors.getBH1750, 'arg': False},
            'veml7700': {'func': sensors.getVEML7700, 'arg': False},
            'hub':      {'func': sensors.getHUB, 'arg': False},
        }
    return __calls

def on_message(client, userdata, message,tmp=None):
    print(" Received message " + str(message.payload)
        + " on topic '" + message.topic
        + "' with QoS " + str(message.qos))

def on_connect(client: mqtt.Client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
        client.publish(getTopic('LWT'), payload="Online", qos=0, retain=True)
    else:
        print("Bad connection Returned code=",rc)

def create_client_from_config() -> mqtt.Client:
    config = getConfig()
    cMqtt = config.mqtt
    client =mqtt.Client(
        getHostIdentifier(), 
        transport=cMqtt.transport, 
        protocol=mqtt.MQTTv311, 
        clean_session=True
        )
    client.username_pw_set(cMqtt.username, cMqtt.password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.will_set(getTopic("LWT"), payload="Offline", qos=0, retain=True)
    client.connect(cMqtt.hostname, cMqtt.port, keepalive=60)
    return client

def getHostIdentifier()->str:
    global __hostId
    if __hostId == False:
        __hostId = socket.gethostname()
    return __hostId

def getTopic(key:str):
    config = getConfig()
    bTopic = config.mqtt.topic
    hostname = getHostIdentifier()
    return bTopic %(hostname, key)

def increaseError(name: str) -> int:
    global __errors
    if name in __errors:
        __errors[name] = __errors[name] + 1
    else:
        __errors[name] = 1
    return __errors[name]

def loop(client: mqtt.Client):
    global __errors
    config = getConfig()
    calls = getCalls()
    for name in calls:
        if(config[name] == True):
            topic = getTopic(name)
            try:
                if(calls[name]['arg'] != False):
                    val = calls[name]['func'](calls[name]['arg']())
                else:
                    val = calls[name]['func']()
                jval = json.dumps(val)
                client.publish(topic, jval)
                print("Published to %s -> %s" %(topic, jval))
                __errors[name] = 0
            except Exception as err:
                errors = increaseError(name)
                jval = json.dumps({'ERR': str(err), 'ERRCOUNT': errors, 'time': time.strftime("%Y-%m-%dT%H:%M:%S")})
                client.publish(topic, jval)
                print("Published ERR to %s -> %s" %(topic, jval))
                if errors >= 10:
                    config[name] = False
