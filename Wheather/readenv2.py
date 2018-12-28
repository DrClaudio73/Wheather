def getvalues():
    import temperature
    import machine
    import dht
    import time
    import mainAppConstants

    try:
        ts=temperature.TemperatureSensor(mainAppConstants.ESP8266_TS_PIN) 
        d=dht.DHT11(machine.Pin(mainAppConstants.ESP8266_DHT_PIN))
        d.measure()
        dh11_hum=d.humidity()
        dh11_tmp=d.temperature()
        dsTemp=ts.read_temp(False)
        time.sleep(1)
        return dsTemp,dh11_tmp,dh11_hum
    except:
        time.sleep(1)
        return 0,0,0

    