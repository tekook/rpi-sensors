#! /usr/bin/env python3
import json
import sys


settings_file = open("settings.json")
settings = json.load(settings_file)
settings_file.close()

if (
    settings["ltr390"]
    or settings["mcp9808"]
    or settings["sht4x"]
    or settings["dps310"]
):
    import board

    i2c = board.I2C()

results = []
warnings = []

if settings["dht22"]["enable"]:
    import Adafruit_DHT

    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(
        sensor, settings["dht22"]["pin"]
    )
    if humidity is not None and temperature is not None:
        results.append(
            {
                "channel": "Temperature (DHT22)",
                "customunit": "°C",
                "float": 1,
                "value": float(temperature),
            }
        )
        results.append(
            {
                "channel": "Humidity (DHT22)",
                "customunit": "%",
                "float": 1,
                "value": float(humidity),
            }
        )
    else:
        warnings.append("DHT22 could not be read.")


if settings["ds18b20"]:
    from w1thermsensor import W1ThermSensor

    try:
        ds18b20 = W1ThermSensor()
        temperature_in_celsius = ds18b20.get_temperature()
        results.append(
            {
                "channel": "Temperature (DS18B20)",
                "customunit": "°C",
                "float": 1,
                "value": float(temperature_in_celsius),
            }
        )
    except:
        warnings.append("ds18b20: ", str(sys.exc_info()[0]))

if settings["ltr390"]:
    import adafruit_ltr390

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
        warnings.append("ltr390: ", str(sys.exc_info()[0]))

if settings["mcp9808"]:
    import adafruit_mcp9808

    try:
        mcp = adafruit_mcp9808.MCP9808(i2c)
        results.append(
            {
                "channel": "Temperature (MCP9808)",
                "customunit": "°C",
                "float": 1,
                "value": float(mcp.temperature),
            }
        )
    except:
        warnings.append("mcp: ", str(sys.exc_info()[0]))


if settings["sht4x"]:
    import adafruit_sht4x

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
            }
        )
        results.append(
            {
                "channel": "Humidity (SHT4x)",
                "customunit": "%",
                "float": 1,
                "value": float(relative_humidity),
            }
        )
    except:
        warnings.append("sht4x: ", str(sys.exc_info()[0]))

if settings["dps310"]:
    import adafruit_dps310

    try:
        dps310 = adafruit_dps310.DPS310(i2c)
        results.append(
            {
                "channel": "Temperature (DPS310)",
                "customunit": "°C",
                "float": 1,
                "value": float(dps310.temperature),
            }
        )
        results.append(
            {
                "channel": "Pressure (SHT4x)",
                "customunit": "hPa",
                "float": 1,
                "value": float(dps310.pressure),
            }
        )
    except:
        warnings.append("dps310: ", str(sys.exc_info()[0]))


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

print(
    json.dumps({"prtg": {"result": results, "text": text}}, sort_keys=True, indent=4),
    end="",
)
