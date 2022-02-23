#! /usr/bin/env python3
import rpisensors, json
from flask import Flask

app = Flask(__name__)

val = rpisensors.getAll()


@app.route("/")
def json_dump():
    return json.dumps({"prtg": {"result": val[0], "text": val[1]}}, sort_keys=True, indent=4)

if __name__ == "__main__":
    app.run(host='0.0.0.0')