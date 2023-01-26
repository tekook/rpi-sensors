# -*- coding: utf-8 -*-
import time, board

__i2c = False

def getI2C() -> board.I2C:
    global __i2c
    if __i2c == False:
        __i2c = board.i2c()
    return __i2c

def getDS18B20():
    from w1thermsensor import W1ThermSensor
    ds18b20 = W1ThermSensor()
    temperature = ds18b20.get_temperature()
    return {
        "temp": float(temperature),
        "temp_rounded": round(float(temperature), 2),
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def getLTR390():
    import adafruit_ltr390
    ltr = adafruit_ltr390.LTR390(getI2C())
    return {
        "uvs": ltr.uvs,
        "light": ltr.light,
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def getMCP9808():
    import adafruit_mcp9808
    mcp = adafruit_mcp9808.MCP9808(getI2C())
    return {
        "temp": float(mcp.temperature),
        "temp_rounded": round(float(mcp.temperature), 2),
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def getSHT4X():
    import adafruit_sht4x
    sht = adafruit_sht4x.SHT4x(getI2C())
    sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
    temperature, relative_humidity = sht.measurements
    return {
        "temp": float(temperature),
        "temp_rounded": round(float(temperature),2),
        "humidity": float(relative_humidity),
        "humidity_rounded": round(float(relative_humidity), 2),
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def getDPS310():
    import adafruit_dps310
    dps310 = adafruit_dps310.DPS310(getI2C())
    temperature = dps310.temperature
    pressure = dps310.pressure
    return {
        "temp": float(temperature),
        "temp_rounded": round(float(temperature),2),
        "pressure": float(pressure),
        "pressure_rounded": round(float(pressure), 2),
        "time": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

def getHUB(addr = "0x17", bus = 1):
    import smbus
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

    result = {}


    if aReceiveBuf[STATUS_REG] & 0x01 :
        warnings.append("HUB: Off-Board temperature sensor overrange!")
    elif aReceiveBuf[STATUS_REG] & 0x02 :
        res = False
    else :
        result['temp_off_board'] = aReceiveBuf[TEMP_REG];

    if aReceiveBuf[STATUS_REG] & 0x04 :
        warnings.append("HUB: Onboard brightness sensor overrange!")
    elif aReceiveBuf[STATUS_REG] & 0x08 :
        warnings.append("HUB: Onboard brightness sensor failure!")
    else :
        result['brightness'] = (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L])
    if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        warnings.append("HUB: Onboard temperature sensor data may not be up to date!")

    result['humidity_on_board'] = aReceiveBuf[ON_BOARD_HUMIDITY_REG]
    if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        warnings.append("HUB: Onboard humidity sensor data may not be up to date!")




    if aReceiveBuf[BMP280_STATUS] == 0 :
        result['temperature_barometer'] = aReceiveBuf[BMP280_TEMP_REG]
        result['pressure_barometer'] = (aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16)
    else :
        warnings.append("HUB: Onboard barometer works abnormally!")

    result['motion'] = aReceiveBuf[HUMAN_DETECT] 
    result['warnings'] = warnings
    result['time'] = time.strftime("%Y-%m-%dT%H:%M:%S")

    return result