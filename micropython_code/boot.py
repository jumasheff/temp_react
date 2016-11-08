# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import machine
from measurement import sleep
webrepl.start()
gc.collect()

def do_connect():
    import network, time
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        # WRITE YOUR WIFI ACCESS POINT NAME AND PASSWORD
        wlan.connect('YOUR_WIFI_ACCESS_POINT_NAME', 'YOUR_WIFI_ACCESS_POINT_PASSWORD')
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(1)
    print('network config:', wlan.ifconfig())

def settime():
    import ntptime
    ntptime.settime()

do_connect()
settime()
gc.collect()

# If the board woke up after deepsleep, keep on going with measurements
# If a "reset" button was explicitly clicked on the board, do nothing.

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    sleep()
else:
    pass