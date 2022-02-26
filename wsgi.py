#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import rpisensors, json, board
from flask import Flask

app = Flask(__name__)
calls = {
    'sht4x': {'func': rpisensors.getSHT4X},
    'ltr390': {'func': rpisensors.getLTR390},
    'ds18b20': {'func': rpisensors.getDS18B20}
}

@app.route("/prtg")
def json_dump():
    val = rpisensors.getAll()
    return json.dumps({"prtg": {"result": val[0], "text": val[1]}}, sort_keys=True, indent=4)

@app.route("/sensor/<name>")
def getSHT4(name: str):
    if(calls[name]):
        i2c = board.I2C();
        val = calls[name]['func'](i2c);
        return {'result': val[0], 'warnings': val[1]}
    else:
        return 'Not found', 404

if __name__ == "__main__":
    app.run()