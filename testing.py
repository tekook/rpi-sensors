#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import rpisensors, board, time;
i2c = board.I2C()
config = rpisensors.getConfig()

print("[press ctrl+c to end the script]") 
try:
    while True:
        val = rpisensors.getHUB(config["hub"]["addr"], config["hub"]["bus"])
        res = val[0]
        human = res[len(res)-1]["value"]
        print("Human: %d" % (human))
        time.sleep(1)
except KeyboardInterrupt:
    print("Script end!")