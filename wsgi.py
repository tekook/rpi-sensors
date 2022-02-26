#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import rpisensors, json, board
from flask import Flask

app = Flask(__name__)
calls = {
    'sht4x': {'func': rpisensors.getSHT4X},
    'ltr390': {'func': rpisensors.getLTR390},
    'ds18b20': {'func': rpisensors.getDS18B20, 'arg': False},
    'mcp9808': {'func': rpisensors.getMCP9808},
    'dps310': {'func': rpisensors.getDPS310}
}

@app.route("/prtg")
def json_dump():
    val = rpisensors.getAll()
    return json.dumps({"prtg": {"result": val[0], "text": val[1]}}, sort_keys=True, indent=4)

@app.route("/sensor/<name>")
def getSHT4(name: str):
    name = name.lower()
    if(name in calls):
        i2c = board.I2C()
        if(calls[name]['arg']):
            val = calls[name]['func'](i2c)
        else:
            val = calls[name]['func']()
        return {'result': val[0], 'warnings': val[1]}
    else:
        return 'Not found', 404

if __name__ == "__main__":
    app.run()