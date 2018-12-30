import network
import credentials
from ntptime import settime
import mainAppConstants
import time

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
    try:
        sta_if = network.WLAN(network.STA_IF)
    except:
        print("error in creating STA IF")
        return(-1)
    try:
        staconnected=sta_if.isconnected()
    except:
        print("error in verifying if STA IF is connected")
        return(-1)
    if not staconnected:
        try:
            noAPFound=False
            sta_if.active(True)
            listAP=str(sta_if.scan())
            if listAP.find(credentials.ToFind1)>0:
                password=credentials.Pass1
                APFound=credentials.ToFind1
            elif listAP.find(credentials.ToFind2)>0:
                password=credentials.Pass2
                APFound=credentials.ToFind2
            else:
                noAPFound=True
        except:
            print("error in scanning APs available")
            return(-1)

        if noAPFound==False:
            print("Found Access point: activating STA connection")
            print('connecting to network...')
            try:
                sta_if.connect(APFound,password)
                while not sta_if.isconnected():
                    pass
                print('STA network config:', sta_if.ifconfig()) 
            except:
                print("error in connencting to AP found")
                return(-1)
            try:
                settime()
            except:
                print("not able to connect to NTP server")
            return 0
        else:
            print("No known STA found......running in AP mode only!!!")
            try:
                sta_if.active(False)
            except:
                print("error in deactivating STA IF!")
                return(-1)
            return -1
    else:
        print("Already connected to AP")
        print('STA network config:', sta_if.ifconfig())
        try:
            settime()
        except:
            print("not able to connect to NTP server")
        return 0