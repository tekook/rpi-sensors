#! /usr/bin/env python3
import json
from gpiozero import CPUTemperature
cpu = CPUTemperature()
print(json.dumps({
    "prtg": {
        "result": [
            {
                "channel": "CPU",
                "float": 1,
                "value": cpu.temperature
            }
        ]
    }
}), end='')