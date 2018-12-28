def no_debug():
    import esp
    # this can be run from the REPL as well
    esp.osdebug(None)

import readenv2
import os
#import usocket as socket
import socket
import utime
import activatenet

dati="i;tempodareboot;tempolocaleFormattato;dsTemp;dh11_Temp;dh11Hum\r\n"
stringaHtmlDati =""
counterK=0

def parse_request(richiesta):
    richiesta=richiesta.split("HTTP/1.")[0]
    richiesta=richiesta.split("GET /")[1]
    richiesta=richiesta.split(" ")[0]
    return richiesta

def updateWheateherValues():
    global dati, stringaHtmlDati
    dsTemp, dh11_Temp,dh11Hum = readenv2.getvalues()
    tempodareboot=utime.time()
    tloc=utime.localtime()
    tempolocaleFormattato=str(tloc[0])+"/"+str(tloc[1])+"/"+str(tloc[2])+"  "+str(tloc[3])+":"+str(tloc[4])+":"+str(tloc[5])
    stringaHtmlDati=stringaHtmlDati+'            <tr><td>%d</td><td>%s</td><td>%s</td><td>%2.1f</td><td>%2.1f</td><td>%2.1f</td></tr>' % (counterK, tempodareboot,tempolocaleFormattato,dsTemp, dh11_Temp,dh11Hum) +'\n'
    dati=dati+str(counterK)+";"+str(tempodareboot)+";"+str(tempolocaleFormattato)+";"+str(dsTemp)+";"+str(dh11_Temp)+";"+str(dh11Hum)+"\r\n"

def start_server():
    http_headers = """HTTP/1.1 200 OK\r\nServer: LiteSpeed\r\nConnection: close\r\nExpires: Sat, 28 Nov 2019 05:36:25 GMT\r\nContent-Type: text/html; charset=UTF-8\r\nLast-Modified: Sat, 28 Nov 2018 19:50:37 GMT\r\nCache-Control: no-cache\r\n\r\n"""
    http_headers_download="""HTTP/1.1 200 OK\r\nServer: LiteSpeed\r\nContent-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\r\nContent-Disposition: attachment; filename="dati.csv"\r\nContent-Length:"""+str(len(dati))+"\r\nConnection: close\r\nCache-Control: no-cache\r\n\r\n"


    html="""<!DOCTYPE html>\n<html>\n    <head>\n        <meta http-equiv="refresh" content="5">\r\n<title>ESP32 Reading Temperature and Humidity values</title>\n<meta name="viewport" content="width=device-width, initial-scale=1">\n    
    <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}</style>\n</head>\n
    <body>\n            <h1>ESP8266 Wheather</h1>\n
            <table border="1"> <tr><th>i</th><th>Time from reboot</th><th>Localtime</th><th>DS Temperature [°C]</th><th>DH11 Temperature [°C]</th><th>DH11 Humidity [%]</th></tr>\n
    """
    htmlClosure= "\n        </body>\n    </html>"

    try:
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        print("addr:",addr)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("s:",s)
        s.settimeout(11.0)
        s.bind(addr)
        s.listen(1)
        print('listening on', addr)
    except:
        s.close()
        return -1
    #rows=[]
    while True:
        #response=""
        try:
            cliente, addr = s.accept()
            print(cliente)
            print('client connected from:', addr)
        except:
            print("Timeout expired")
            s.close()
            break
        
        try:
            request = cliente.recv(1024)
            request = str(request)
            print('Content = %s' % request)
            print("richiesta main loop:",parse_request(str(request)))
        except:
            print("EXCEPTION OCCURRED WHILE RECEIVING DATA FROM SOCKET")
            s.close()
            cliente.close()
            break
        
        if parse_request(str(request))=="file.txt":
            response=http_headers_download+dati
        else:
            response=http_headers+html+stringaHtmlDati+'            </table>\n<a href="/file.txt"><button class="button button2">GET LOG FILE!</button></a><h2>Your request was</h2>\n<code>'+request+"</code>\n"+htmlClosure
        print(response)
        '''
        for jk in range(0,len(response),10):
            cliente.send(response[jk:jk+10])
        '''
        try:
            for testo in response:
                cliente.send(testo)
        except:
            print("EXCEPTION OCCURRED WHILE SENDING DATA ON SOCKET")
            s.close()
        s.close()    
        cliente.close()
        break

print("Welcome to webserver section.....\n")

while True:
    updateWheateherValues()
    counterK=(counterK+1)%1500
    print("counterK",counterK)
    f=open("dati.csv","w")
    with f:
        f.write(dati)

    f=open("dati.csv","r")
    with f:
        print(f.read())

    if counterK == 0:
        dati="i;tempodareboot;tempolocaleFormattato;dsTemp;dh11_Temp;dh11Hum\r\n"
        stringaHtmlDati = ""
        activatenet.do_setupWiFiSTA()

    print(start_server())
#no_debug()