from threading import Event
import sys

from dotmap import DotMap
import libbase as lib, libsensors as sensors

exit = Event()
def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    exit.set()

def main():
    config = lib.getConfig()
    client = lib.create_client_from_config()
    client.loop_start()
    mqtt = config.get("mqtt", default=DotMap())
    teleperiod = mqtt.get("teleperiod", 300)
    print("TelePeriod:", teleperiod)
    precision = mqtt.get("precision", 3)
    sensors.setPrecision(precision)
    while not exit.is_set():
        lib.loop(client)
        for i in range(teleperiod):
            exit.wait(1)

    client.loop_stop() 
    client.disconnect()

if __name__ == '__main__':

    import signal
    for sig in ('TERM', 'HUP', 'INT'):
        try:
            signal.signal(getattr(signal, 'SIG'+sig), quit);
        except:
            print("Could not register SIG"+sig)
    main()