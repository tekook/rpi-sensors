from threading import Event
import board, time, socket, json
import libbase as lib, libsensors as sensors
i2c = board.I2C()

calls = {
    'sht4x': {'func': sensors.getSHT4X, 'arg': board.I2C},
    'ltr390': {'func': sensors.getLTR390, 'arg': board.I2C},
    'ds18b20': {'func': sensors.getDS18B20, 'arg': False},
    'mcp9808': {'func': sensors.getMCP9808, 'arg': board.I2C},
    'dps310': {'func': sensors.getDPS310, 'arg': board.I2C},
    'hub': {'func': sensors.getHUB, 'arg': False}
}

client = lib.create_client_from_config()
config = lib.getConfig()

run = True
exit = Event()
def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    exit.set()
def main():
    client.loop_start()
    while not exit.is_set():
        lib.loop(calls,client)
        for i in range(config['mqtt']['teleperiod'] or 10):
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