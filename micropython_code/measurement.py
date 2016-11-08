import machine


def get_measurements():
    import dht
    from utime import localtime
    d = dht.DHT11(machine.Pin(14))
    d.measure()
    (year, month, mday, hour, minute, second, weekday, yearday) = localtime()
    result = {
        "temperature": d.temperature(),
        "humidity": d.humidity(),
        "datetime": "{0}-{1}-{2}-{3}-{4}-{5}".format(year,month,mday,hour,minute,second),
        "location": "indoor"
    }
    return result


def send_measurements_to_server():
    import ujson as json
    import urequests as requests
    headers = {"Content-type": "application/json"}
    # PUT YOUR FIREBASE URL AND AUTH TOKEN
    url = "https://YOUR_FIREBASE_APP.firebaseio.com/measurements.json?auth=YOUR_FIREBASE_APP_TOKEN"
    j = json.dumps(get_measurements())
    requests.post(url, data=j, headers=headers)


def sleep():
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # Wake up after 8 minutes
    rtc.alarm(rtc.ALARM0, 480000)
    send_measurements_to_server()
    machine.deepsleep()
