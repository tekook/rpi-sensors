# -*- coding: utf-8 -*-
import time, board
from dotmap import DotMap

__i2c = False
__precision = 2

def setPrecision(precision: int):
    global __precision
    __precision = precision
    print("Precision set to: %i" % precision)

def getI2C() -> board.I2C:
    global __i2c
    if __i2c == False:
        __i2c = board.I2C()
    return __i2c

def getDS18B20():
    global __precision
    from w1thermsensor import W1ThermSensor
    ds18b20 = W1ThermSensor()
    temperature = ds18b20.get_temperature()
    return {
        "temp": round(float(temperature), __precision),
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def getLTR390():
    import adafruit_ltr390
    ltr = adafruit_ltr390.LTR390(getI2C())
    return {
        "uvs": ltr.uvs,
        "uvi": ltr.uvi,
        "light": ltr.light,
        "lux": ltr.lux,
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
def getBH1750():
    import adafruit_bh1750
    res = adafruit_bh1750.BH1750(getI2C())
    return {
        "resolution": res.resolution,
        "mode": res.mode,
        "lux": res.lux,
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def getVEML7700():
    import adafruit_veml7700
    res = adafruit_veml7700.VEML7700(getI2C())
    return {
        "lux": res.lux,
        "light": res.light,
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def getMCP9808():
    global __precision
    import adafruit_mcp9808
    mcp = adafruit_mcp9808.MCP9808(getI2C())
    return {
        "temp": round(float(mcp.temperature), __precision),
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def getSHT4X():
    global __precision
    import adafruit_sht4x
    sht = adafruit_sht4x.SHT4x(getI2C())
    sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
    temperature, relative_humidity = sht.measurements
    return {
        "temp": round(float(temperature), __precision),
        "humidity": round(float(relative_humidity), __precision),
        "serial_number": sht.serial_number,
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def getDPS310():
    global __precision
    import adafruit_dps310
    dps310 = adafruit_dps310.DPS310(getI2C())
    temperature = dps310.temperature
    pressure = dps310.pressure
    return {
        "temp": round(float(temperature), __precision),
        "pressure": round(float(pressure), __precision),
        "altitude": dps310.altitude,
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
