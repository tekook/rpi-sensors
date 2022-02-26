# -*- coding: utf-8 -*-
import json, os, sys

def getConfig():
    config_file = open(os.path.dirname(os.path.realpath(__file__)) + "/sensors_config.json")
    config = json.load(config_file)
    config_file.close()
    return config


def getDHT22(pin):
    import Adafruit_DHT
    results = []
    warnings = []

    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(
        sensor, pin
    )
    if humidity is not None and temperature is not None:
        results.append(
            {
                "channel": "Temperature (DHT22)",
                "customunit": "°C",
                "float": 1,
                "value": float(temperature),
                "valueR": round(float(temperature), 2),
            }
        )
        results.append(
            {
                "channel": "Humidity (DHT22)",
                "customunit": "%",
                "float": 1,
                "value": float(humidity),
                "valueR": round(float(humidity), 2),
            }
        )
    else:
        warnings.append("DHT22 could not be read.")
    return results, warnings

def getDS18B20():
    from w1thermsensor import W1ThermSensor
    results = []
    warnings = []

    try:
        ds18b20 = W1ThermSensor()
        temperature_in_celsius = ds18b20.get_temperature()
        results.append(
            {
                "channel": "Temperature (DS18B20)",
                "customunit": "°C",
                "float": 1,
                "value": float(temperature_in_celsius),
                "valueR": round(float(temperature_in_celsius), 2),
            }
        )
    except:
        warnings.append("ds18b20: " + str(sys.exc_info()[0]))
    
    return results, warnings

def getLTR390(i2c):
    import adafruit_ltr390
    results = []
    warnings = []

    try:
        ltr = adafruit_ltr390.LTR390(i2c)
        results.append(
            {
                "channel": "UV (LTR390)",
                "customunit": "lux",
                "float": 0,
                "value": ltr.uvs,
            }
        )
        results.append(
            {
                "channel": "AmbientLight (LTR390)",
                "customunit": "lux",
                "float": 0,
                "value": ltr.light,
            }
        )
    except:
        warnings.append("ltr390: " + str(sys.exc_info()[0]))



    return results, warnings

def getMCP9808(i2c):
    import adafruit_mcp9808
    results = []
    warnings = []

    try:
        mcp = adafruit_mcp9808.MCP9808(i2c)
        results.append(
            {
                "channel": "Temperature (MCP9808)",
                "customunit": "°C",
                "float": 1,
                "value": float(mcp.temperature),
                "valueR": round(float(mcp.temperature), 2)
            }
        )
    except:
        warnings.append("mcp: " + str(sys.exc_info()[0]))
    return {"results": results, "warnings": warnings}

def getSHT4X(i2c):
    import adafruit_sht4x
    results = []
    warnings = []

    try:
        sht = adafruit_sht4x.SHT4x(i2c)
        sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
        temperature, relative_humidity = sht.measurements
        results.append(
            {
                "channel": "Temperature (SHT4x)",
                "customunit": "°C",
                "float": 1,
                "value": float(temperature),
                "valueR": round(float(temperature), 2)
            }
        )
        results.append(
            {
                "channel": "Humidity (SHT4x)",
                "customunit": "%",
                "float": 1,
                "value": float(relative_humidity),
                "valueR": round(float(relative_humidity), 2)
            }
        )
    except:
        warnings.append("sht4x: " + str(sys.exc_info()[0]))

    return results, warnings

def getDPS310(i2c):
    import adafruit_dps310
    results = []
    warnings = []

    try:
        dps310 = adafruit_dps310.DPS310(i2c)
        results.append(
            {
                "channel": "Temperature (DPS310)",
                "customunit": "°C",
                "float": 1,
                "value": float(dps310.temperature),
                "valueR": round(float(dps310.temperature), 2)
            }
        )
        results.append(
            {
                "channel": "Pressure (DPS310)",
                "customunit": "hPa",
                "float": 1,
                "value": float(dps310.pressure),
                "valueR": round(float(dps310.pressure), 2)
            }
        )
    except:
        warnings.append("dps310: " + str(sys.exc_info()[0]))
    return results, warnings

def getHUB(addr, bus):
    import smbus
    results = []
    warnings = []
    
    SENSOR_HUB_DEVICE_ADDR = int(addr, 16)
    TEMP_REG = 0x01
    LIGHT_REG_L = 0x02
    LIGHT_REG_H = 0x03
    STATUS_REG = 0x04
    ON_BOARD_TEMP_REG = 0x05
    ON_BOARD_HUMIDITY_REG = 0x06
    ON_BOARD_SENSOR_ERROR = 0x07
    BMP280_TEMP_REG = 0x08
    BMP280_PRESSURE_REG_L = 0x09
    BMP280_PRESSURE_REG_M = 0x0A
    BMP280_PRESSURE_REG_H = 0x0B
    BMP280_STATUS = 0x0C
    HUMAN_DETECT = 0x0D

    bus = smbus.SMBus(bus)

    aReceiveBuf = []

    aReceiveBuf.append(0x00) # 占位符

    for i in range(TEMP_REG,HUMAN_DETECT + 1):
        aReceiveBuf.append(bus.read_byte_data(SENSOR_HUB_DEVICE_ADDR, i))




    if aReceiveBuf[STATUS_REG] & 0x01 :
        warnings.append("HUB: Off-Board temperature sensor overrange!")
    elif aReceiveBuf[STATUS_REG] & 0x02 :
        res = False
    else :
        results.append({
            "channel": "Temperature (Off-Board)",
            "customunit": "°C",
            "value": aReceiveBuf[TEMP_REG]
        })

    res = {
        "channel": "Brightness",
        "customunit": "Lux",
        "value": 0
    }

    if aReceiveBuf[STATUS_REG] & 0x04 :
        res["warning"] = 1
        warnings.append("HUB: Onboard brightness sensor overrange!")
    elif aReceiveBuf[STATUS_REG] & 0x08 :
        res["warning"] = 1
        warnings.append("HUB: Onboard brightness sensor failure!")
    else :
        res["value"] = (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L])
    results.append(res)

    res = {
        "channel": "Temperature (On-Board)",
        "customunit": "°C",
        "value": aReceiveBuf[ON_BOARD_TEMP_REG]
    }
    if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        res["warning"] = 1
        warnings.append("HUB: Onboard temperature sensor data may not be up to date!")
    results.append(res)

    res = {
        "channel": "Humidity (On-Board)",
        "customunit": "%",
        "value": aReceiveBuf[ON_BOARD_HUMIDITY_REG]
    }
    if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        res["warning"] = 1
        warnings.append("HUB: Onboard humidity sensor data may not be up to date!")
    results.append(res)




    if aReceiveBuf[BMP280_STATUS] == 0 :
        res = {
            "channel": "Temperature (Barometer)",
            "customunit": "°C",
            "value": aReceiveBuf[BMP280_TEMP_REG]
        }
        results.append(res)
        res = {
            "channel": "Pressure (BaroMeter)",
            "customunit": "pascal",
            "value": (aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16)
        }
        results.append(res)
    else :
        warnings.append("HUB: Onboard barometer works abnormally!")

    results.append({
        "channel": "Motion Detection",
        "value": aReceiveBuf[HUMAN_DETECT] 
    })

    return results, warnings

def getAll():
    import board
    i2c = board.I2C()
    results = []
    warnings = []
    config = getConfig()

    if config["dht22"]["enable"]:
        val = getDHT22(config["dht22"]["pin"])
        results += val[0]
        warnings += val[1]
    if config["ds18b20"]:
        val = getDS18B20()
        results += val[0]
        warnings += val[1]
    if config["ltr390"]:
        val = getLTR390(i2c)
        results += val[0]
        warnings += val[1]
    if config["mcp9808"]:
        val = getMCP9808(i2c)
        results += val[0]
        warnings += val[1]
    if config["sht4x"]:
        val = getSHT4X(i2c)
        results += val[0]
        warnings += val[1]
    if config["dps310"]:
        val = getDPS310(i2c)
        results += val[0]
        warnings += val[1]
    if config["hub"]["enable"]:
        val = getHUB(config["hub"]["addr"], config["hub"]["bus"])
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
    return results, text