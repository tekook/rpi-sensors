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
        with open(d + "/config.json", "r") as f:
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
            'veml7700': {'func': sensors.getVEML7700, 'arg': False}
        }
    return __calls

def on_message(client, userdata, message,tmp=None):
    print(" Received message " + str(message.payload)
        + " on topic '" + message.topic
        + "' with QoS " + str(message.qos))

def on_log(client, userdata, level, buf):
    global __config
    if __config.get("mqtt", default=DotMap()).get("log", False):
        print("log:",buf)

def on_connect(client: mqtt.Client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
        client.publish(getTopic('LWT'), payload="Online", qos=0, retain=True)
        client.connected = True
    else:
        print("Bad connection Returned code=",rc)
        client.connected = False

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
    client.on_log = on_log
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

def publish(client: mqtt.Client, topic: str, payload):
    res = client.publish(topic, payload)
    status = res[0]
    if status == 0:
        print(f"Send `{payload}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic `{topic}`")


def loop(client: mqtt.Client):
    global __errors
    config = getConfig()
    calls = getCalls()
    for name in calls:
        if(config.get(name, False) == True):
            topic = getTopic(name)
            try:
                if(calls.get(name + ".arg", False) != False):
                    val = calls[name]['func'](calls[name]['arg']())
                else:
                    val = calls[name]['func']()
                jval = json.dumps(val)
                publish(client, topic, jval)
                __errors[name] = 0
            except Exception as err:
                errors = increaseError(name)
                jval = json.dumps({'ERR': str(err), 'ERRCOUNT': errors, 'time': time.strftime("%Y-%m-%dT%H:%M:%S")})
                publish(client, topic, jval)
                print("Published ERR to %s -> %s" %(topic, jval))
                if errors >= 10:
                    config[name] = False
                    print(f"Disabling `{name}` for too many errors")
