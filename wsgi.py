#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import rpisensors, json
from flask import Flask

app = Flask(__name__)

@app.route("/")
def json_dump():
    val = rpisensors.getAll()
    return json.dumps({"prtg": {"result": val[0], "text": val[1]}}, sort_keys=True, indent=4)

if __name__ == "__main__":
    app.run()