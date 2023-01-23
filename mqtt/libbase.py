# -*- coding: utf-8 -*-
import json, os
import socket
import sys
import time
import paho.mqtt.client as mqtt
__config = False
__hostname = False
def getConfig():
    global __config
    if __config == False:
        print("Reading config...")
        d = os.path.dirname(os.path.realpath(__file__))
        f = open(d + "/config.json", "r")
        config = json.load(f)
        __config = config
        f.close()
    return __config

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

def create_client_from_config():
    config = getConfig()
    hostname = socket.gethostname()
    cMqtt = config['mqtt']
    client =mqtt.Client(
        hostname, 
        transport=cMqtt['transport'], 
        protocol=mqtt.MQTTv311, 
        clean_session=True
        )
    client.username_pw_set(cMqtt['username'], cMqtt['password'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.will_set(getTopic("LWT"), payload="Offline", qos=0, retain=True)
    client.connect(cMqtt['hostname'], cMqtt['port'], keepalive=60)
    return client

def getHostname():
    global __hostname
    if __hostname == False:
        __hostname = socket.gethostname()
    return __hostname

def getTopic(key):
    config = getConfig()
    bTopic = config['mqtt']['topic']
    hostname = getHostname()
    return bTopic %(hostname, key)

def loop(calls, client: mqtt.Client):
    config = getConfig()
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
            except:
                client.publish(topic, json.dumps({'ERR': str(sys.exc_info()[0]), 'time': time.strftime("%Y-%m-%dT%H:%M:%S")}))
                print("ERR: " + name + ": " + str(sys.exc_info()[0]))
