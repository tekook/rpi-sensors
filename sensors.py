#! /usr/bin/env python3
import json
import sys


settings_file = open('settings.json')
settings = json.load(settings_file)
settings_file.close()

if settings['sensors']['ltr390']['enable'] or settings['sensors']['mcp9808']['enable'] or settings['sensors']['sht4x']['enable'] or settings['sensors']['dps310']['enable'] :
    import board
    i2c = board.I2C()

results = []
warnings = []

if settings['sensors']['dht22']['enable'] :
    import Adafruit_DHT
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor,
    settings['sensors']['dht22']['pin'])
    if humidity is not None and temperature is not None:
        results.append( {
            "channel": "Temperature (DHT22)",
            "customunit": "°C",
            "float": 1,
            "value": float(format(temperature, "0.1f"))
        })
        results.append({
            "channel": "Humidity (DHT22)",
            "customunit": "%",
            "float": 1,
            "value": float(format(humidity, "0.1f"))
        })
    else :
        warnings.append("DHT22 could not be read.")



if settings['sensors']['ds18b20']['enable'] :
    from w1thermsensor import W1ThermSensor
    try :
        ds18b20 = W1ThermSensor()
        temperature_in_celsius = ds18b20.get_temperature()
        results.append( {
            "channel": "Temperature (DS18B20)",
            "customunit": "°C",
            "float": 1,
            "value": float(format(temperature_in_celsius, "0.4f"))
        })
    except :
        warnings.append(str(sys.exc_info()[0]))

if settings['sensors']['ltr390']['enable'] :
    import adafruit_ltr390
    try :
        i2c = board.I2C()
        ltr = adafruit_ltr390.LTR390(i2c)
        results.append( {
            "channel": "UV (LTR390)",
            "customunit": "lux",
            "float": 0,
            "value": ltr.uvs
        })
        results.append( {
            "channel": "AmbientLight (LTR390)",
            "customunit": "lux",
            "float": 0,
            "value": ltr.light
        })
    except :
        warnings.append(str(sys.exc_info()[0]))

if settings['sensors']['mcp9808']['enable'] :
    import adafruit_mcp9808
    mcp = adafruit_mcp9808.MCP9808(i2c)
    results.append( {
            "channel": "Temperature (MCP9808)",
            "customunit": "°C",
            "float": 1,
            "value": float(format(mcp.temperature, "0.4f"))
        })

if settings['sensors']['sht4x']['enable'] :
    import adafruit_sht4x
    sht = adafruit_sht4x.SHT4x(i2c)
    sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
    temperature, relative_humidity = sht.measurements
    results.append( {
        "channel": "Temperature (SHT4x)",
        "customunit": "°C",
        "float": 1,
        "value": float(format(temperature, "0.4f"))
    })
    results.append({
        "channel": "Humidity (SHT4x)",
        "customunit": "%",
        "float": 1,
        "value": float(format(relative_humidity, "0.4f"))
    })

if settings['sensors']['dps310']['enable'] :
    import adafruit_dps310
    dps310 = adafruit_dps310.DPS310(i2c)
    results.append( {
        "channel": "Temperature (DPS310)",
        "customunit": "°C",
        "float": 1,
        "value": float(format(dps310.temperature, "0.4f"))
    })
    results.append({
        "channel": "Pressure (SHT4x)",
        "customunit": "hPa",
        "float": 1,
        "value": float(format(dps310.pressure, "0.4f"))
    })







results.append({
    "channel": "Warnings",
    "value": len(warnings),
    "warning": 0 if len(warnings) == 0 else 1
})
if(len(warnings) == 0) :
    text = "OK"
else :
    text = ', '.join(warnings)

print(json.dumps({
    "prtg": {
        "result": results,
        "text": text
    }
}, sort_keys=True, indent=4), end='')