def getvalues(boardType):
    import temperature
    import machine
    import dht
    import time
    import mainAppConstants

    if boardType == 'esp32':
        TSPIN=mainAppConstants.ESP32_TS_PIN
        DHTPIN=mainAppConstants.ESP32_DHT_PIN
    else:
        TSPIN=mainAppConstants.ESP8266_TS_PIN
        DHTPIN=mainAppConstants.ESP8266_DHT_PIN

    try:
        ts=temperature.TemperatureSensor(TSPIN) 
        d=dht.DHT11(machine.Pin(DHTPIN))
        d.measure()
        dh11_hum=d.humidity()
        dh11_tmp=d.temperature()
        dsTemp=ts.read_temp(False)
        time.sleep(1)
        return dsTemp,dh11_tmp,dh11_hum
    except:
        time.sleep(1)
        return 0,0,0