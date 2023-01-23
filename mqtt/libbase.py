# -*- coding: utf-8 -*-
import json, os
import socket
import paho.mqtt.client as mqtt

def getConfig():
    d = os.path.dirname(os.path.realpath(__file__))
    f = open(d + "/config.json", "r")
    config = json.load(f)
    f.close()
    return config

def on_message(client, userdata, message,tmp=None):
    print(" Received message " + str(message.payload)
        + " on topic '" + message.topic
        + "' with QoS " + str(message.qos))

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
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
    client.connect(cMqtt['hostname'], cMqtt['port'], keepalive=60)
    return client

def loop(config, calls, client: mqtt.Client):
    bTopic = config['mqtt']['topic']
    hostname = socket.gethostname()
    for name in calls:
        if(config[name] == True):
            if(calls[name]['arg'] != False):
                val = calls[name]['func'](calls[name]['arg']())
            else:
                val = calls[name]['func']()
            topic = bTopic % (hostname, name)
            jval = json.dumps(val);
            client.publish(topic, jval)
            print("Published to %s -> %s" %(topic, jval))
            
            
