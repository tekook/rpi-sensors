#! /usr/bin/env python3
import rpisensors, json

val = rpisensors.getAll()

print(
    json.dumps({"prtg": {"result": val[0], "text": val[1]}}, sort_keys=True, indent=4),
    end="",
)
