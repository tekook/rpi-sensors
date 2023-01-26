from threading import Event
import libbase as lib, libsensors as sensors

exit = Event()
def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    exit.set()

def main():
    client = lib.create_client_from_config()
    config = lib.getConfig()      
    client.loop_start()
    while not exit.is_set():
        lib.loop(client)
        for i in range(config.get('mqtt.teleperiod', 10)):
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