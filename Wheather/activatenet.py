import network
import time
import credentials

def do_setupWiFiAP():
    #network.phy_mode(network.MODE_11G)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    time.sleep(1)
    ap_if.active(True)
    #while ap_if.active() == False:
    #    pass
    ap_if.config(channel=3,password=credentials.APPass)
    print("channel",ap_if.config('channel'))
    print("essid",ap_if.config('essid'))
    print('AP network config:', ap_if.ifconfig())
    #ap_if.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
    #print('new network config:', ap_if.ifconfig())

def do_setupWiFiSTA():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        listAP=str(sta_if.scan())
        listAP=listAP.split(credentials.ToFind)[1]
        if listAP[0:9]==credentials.ToMatch:
            print("Found Access point: activating STA connection")
            print('connecting to network...')
            sta_if.connect(credentials.Router,credentials.Pass)
            while not sta_if.isconnected():
                pass
            print('STA network config:', sta_if.ifconfig()) 
        else:
            print("Running in AP mode only")
            sta_if.active(False)
    else:
        print("Already connected to AP")
        print('STA network config:', sta_if.ifconfig())