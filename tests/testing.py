#! /usr/bin/env python3
import os
import time
import board
import adafruit_ltr390
import adafruit_mcp9808
import adafruit_sht4x
import adafruit_dps310
import Adafruit_DHT


os.system('clear')
dht = Adafruit_DHT.DHT22

i2c = board.I2C()
ltr = adafruit_ltr390.LTR390(i2c)

mcp = adafruit_mcp9808.MCP9808(i2c)

sht = adafruit_sht4x.SHT4x(i2c)
print("Found SHT4x with serial number", hex(sht.serial_number))
sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
print("Current mode is: ", adafruit_sht4x.Mode.string[sht.mode])

dps310 = adafruit_dps310.DPS310(i2c)

from w1thermsensor import W1ThermSensor
ds18b20 = W1ThermSensor()


while True:
    temperature, relative_humidity = sht.measurements
    print("UV:", ltr.uvs, "\t\t\tAmbient Light:", ltr.light)
    print("MCP Temp:", mcp.temperature, "°C")
    print("SHT Temp: %0.4f °C\tHumidity: %0.4f %%" % (temperature, relative_humidity))
    #print("SHT Humidity: %0.1f %%" % relative_humidity)
    print("DPS Temp: %.4f °C\tPressure = %.4f hPa"% (dps310.temperature, dps310.pressure))
    #print("DPS Pressure = %.2f hPa"%dps310.pressure)
    
    dhtHumidity, dhtTemp = Adafruit_DHT.read_retry(dht, 12)
    print("DHT Temp: %0.4f °C\tHumidity: %0.4f %%" % (dhtTemp, dhtHumidity))
    print("DS~ Temp: %0.4f °C" % ds18b20.get_temperature())
    print("-------------------------------------------------------------------------------")
    time.sleep(1)