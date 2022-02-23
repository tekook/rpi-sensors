#! /usr/bin/env python3
import rpisensors, board, json
from flask import Flask

app = Flask(__name__)
i2c = board.I2C()
results = []
warnings = []
config = rpisensors.getConfig()

if config["dht22"]["enable"]:
    val = rpisensors.getDHT22(config["dht22"]["pin"])
    results += val[0]
    warnings += val[1]
if config["ds18b20"]:
    val = rpisensors.getDS18B20()
    results += val[0]
    warnings += val[1]
if config["ltr390"]:
    val = rpisensors.getLTR390(i2c)
    results += val[0]
    warnings += val[1]
if config["mcp9808"]:
    val = rpisensors.getMCP9808(i2c)
    results += val[0]
    warnings += val[1]
if config["sht4x"]:
    val = rpisensors.getSHT4X(i2c)
    results += val[0]
    warnings += val[1]
if config["dps310"]:
    val = rpisensors.getDPS310(i2c)
    results += val[0]
    warnings += val[1]
if config["hub"]["enable"]:
    val = rpisensors.getHUB(config["hub"]["addr"], config["hub"]["bus"])
    results += val[0]
    warnings += val[1]


results.append(
    {
        "channel": "Warnings",
        "value": len(warnings),
        "warning": 0 if len(warnings) == 0 else 1,
    }
)
if len(warnings) == 0:
    text = "OK"
else:
    text = ", ".join(warnings)


@app.route("/")
def json_dump():
    return json.dumps({"prtg": {"result": results, "text": text}}, sort_keys=True, indent=4)

if __name__ == "__main__":
    app.run()