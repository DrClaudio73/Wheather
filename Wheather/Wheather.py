import readenv
import os
#import usocket as socket
import socket
import utime,time
import activateNet
import mainAppConstants

def cettime(): #Many thanks to Mr. "JumpZero"!!!
    year = time.localtime()[0]       #get current year
    HHMarch   = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) #Time of March change to CEST
    HHOctober = time.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to CET
    now=time.time()
    if now < HHMarch :               # we are before last sunday of march
        cet=time.localtime(now+3600) # CET:  UTC+1H
    elif now < HHOctober :           # we are before last sunday of october
        cet=time.localtime(now+7200) # CEST: UTC+2H
    else:                            # we are after last sunday of october
        cet=time.localtime(now+3600) # CET:  UTC+1H
    return(cet)

def parseRequest(richiesta):
    richiesta_=richiesta.split("HTTP/1.")[0]
    richiesta_=richiesta_.split("GET /")[1]
    richiesta_=richiesta_.split(" ")[0]
    return richiesta_

def updateWheateherValues(boardType,counterK,tempoalboot):
    dsTemp, dh11_Temp,dh11Hum = readenv.getvalues(boardType)
    tempodareboot=utime.time()-tempoalboot
    tloc=cettime()
    tempolocaleFormattato=[]
    tempolocaleFormattato.append(str(tloc[0])+"/"+str(tloc[1])+"/"+str(tloc[2]))
    tempolocaleFormattato.append(str(tloc[3])+":"+str(tloc[4])+":"+str(tloc[5]))
    stringaHtmlDati_loc='            <tr><td>%d</td><td>%d</td><td>%s</td><td>%s</td><td>%2.1f</td><td>%d</td><td>%d</td></tr>' % (counterK, tempodareboot,tempolocaleFormattato[0],tempolocaleFormattato[1],dsTemp, dh11_Temp,dh11Hum) +'\r\n'
    dati_loc=str(counterK)+";"+str(tempodareboot)+";"+str(tempolocaleFormattato[0])+";"+str(tempolocaleFormattato[1])+";"+("%2.1f" % dsTemp)+";"+str(dh11_Temp)+";"+str(dh11Hum)+"\r\n"
    return stringaHtmlDati_loc, dati_loc

def startWebServer(boardType,s,addrListen,ResetCsvFile=False):
    print("entering setWebServer",boardType,s,addrListen)
    '''
    try:
        addrListen = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(mainAppConstants.SOCKETTIMEOUT)
        s.bind(addrListen)
        s.listen(1)
    except:
        print("EXCEPTION WHILE ALLOCATING SOCKET")
        s.close()
        return -1,ResetCsvFile
    '''
    while True:
        try:
            print('listening on', addrListen)
            cliente, addr = s.accept()
            print(cliente)
            print('client connected from:', addr)
        except:
            print("Timeout expired")
            #s.close()
            #cliente.close() no put this line otherwise local variable referenced before assignement
            return -2,ResetCsvFile
        try:
            request = cliente.recv(1024)
            request = str(request)
            print('Content = %s' % request)
            print("richiesta main loop:",parseRequest(str(request)))
        except:
            print("EXCEPTION OCCURRED WHILE RECEIVING DATA FROM SOCKET")
            #s.close()
            cliente.close()
            return -3,ResetCsvFile
        
        #Sending response
        try:
            if parseRequest(str(request))=="dati.csv": #sending dati.csv for downloading purposes
                fHeadersToSend=open('headers_download_page.txt','r')
                with fHeadersToSend:
                    for x in fHeadersToSend:
                        cliente.send(x)
                fHeadersToSend.close()
                #determine length of content to send
                fContentToSend=open('dati.csv','r')
                lunghezza=0
                with fContentToSend:
                    for x in fContentToSend:
                        lunghezza=lunghezza+len(x)
                fContentToSend.close()
                
                cliente.send(str(lunghezza)+'\r\n\r\n')
                
                fContentToSend=open('dati.csv','r')
                with fContentToSend:
                    for x in fContentToSend:
                        cliente.send(x)
                fContentToSend.close()
                cliente.close()
            elif parseRequest(str(request))=="clean_csv": #sending message that csv file will be reset
                ResetCsvFile=True
                cliente.send('HTTP/1.1 200 OK')
                cliente.send('Server: LiteSpeed')
                cliente.send('Expires: Sat, 28 Nov 2019 05:36:25 GMT')
                cliente.send('Content-Type: text/html; charset=UTF-8')
                cliente.send('Last-Modified: Sat, 28 Nov 2018 19:50:37 GMT')
                cliente.send('Cache-Control: no-cache')
                cliente.send('Connection: close\r\n\r\n')
                cliente.send('<!DOCTYPE html> <html> <head> <title>ESP32 Reading Temperature and Humidity values</title> </head>')
                cliente.send('    <body>\n        <h1>OK file will be reset!!!!</h1>\n')
                cliente.send('        <a href="/"><button class="button">RETURN!</button></a>\n')
                cliente.send('\n    </body>\n</html>')
                cliente.close()
                return 0,ResetCsvFile
            else: #sending HTML page
                if boardType=='esp32':
                    fHeadersToSend=open('headers_main_pageESP32.txt','r')
                else:
                    fHeadersToSend=open('headers_main_pageESP8266.txt','r')
                with fHeadersToSend:
                    for x in fHeadersToSend:
                        cliente.send(x)
                fHeadersToSend.close()
                #determine length of content to send
                #fContentToSend=open('dati.csv','r')
                #lunghezza=0
                #for x in fContentToSend:
                #    lunghezza=lunghezza+len(x)
                #fContentToSend.close()
                
                #cliente.send(str(lunghezza)+'\r\n\r\n')
                cliente.send('\r\n')
                fContentToSend=open('main_out.txt','r')
                with fContentToSend:
                    for x in fContentToSend:
                        cliente.send(x)
                fContentToSend.close()

                cliente.send('        </table>\n        <a href="/dati.csv"><button class="button button2">GET LOG FILE!</button></a>')
                cliente.send('\n        <a href="/clean_csv"><button class="button">CLEAN LOG FILE!</button></a>')
                cliente.send('\n        <h2>Your request was</h2>\n        <code>')
                cliente.send(request)
                cliente.send("</code>\n")

                fContentToSend=open('html_closure_main_page.txt','r')
                with fContentToSend:
                    for x in fContentToSend:
                        cliente.send(x)
                fContentToSend.close()
                cliente.close()
        except:
            print("EXCEPTION OCCURRED WHILE SENDING DATA ON SOCKET")
            #s.close()
            cliente.close()
            return -4,ResetCsvFile

def main(boardType,tempoalboot):
    print("\n=====================================\nWelcome to Wheather App on "+str(boardType)+".....\n=====================================\n")
    counterK=0
    ResetCsvFile=False
    wait=0
    try:
        addrListen = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(mainAppConstants.SOCKETTIMEOUT)
        print("mainAppConstants.SOCKETTIMEOUT",mainAppConstants.SOCKETTIMEOUT)
        s.bind(addrListen)
        s.listen(1)
        print("first allocation",s.fileno())
    except:
        wait=1
        s.close()
        print('errore in first socket allocation')

    while True:
        wait=0
        try:
            if s.fileno()==-1:
                print('file no = -1')
                addrListen = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(mainAppConstants.SOCKETTIMEOUT)
                s.bind(addrListen)
                s.listen(1)
                print("loop allocation",s.fileno())
            else:
                print('else file no = ',s.fileno())
        except:
            print("EXCEPTION WHILE ALLOCATING SOCKET")
            wait=1
            s.close()
            #return -1,ResetCsvFile

        #After MAX_SAMPLES_STORED samples
        if counterK == 0:
            #resets the content of html page
            fout=open('main_out.txt','w')
            fout.write('')
            fout.close()

            #starts new section in csv file
            fin=open('headers_download_file.txt','r')
            fout=open('dati.csv','a')
            for x in fin:
                fout.write(x)
            fout.close()
            fin.close()

        if ResetCsvFile:
            fout=open('main_out.txt','w')
            fout.write('')
            fout.close()

            fin=open('headers_download_file.txt','r')
            fout=open('dati.csv','w')
            for x in fin:
                fout.write(x)
            fout.close()
            fin.close()
            ResetCsvFile=False
        #Getting Samples
        stringaHtmlDati, dati=updateWheateherValues(boardType,counterK,tempoalboot)
        #Updating html main page
        fout=open('main_out.txt','a')
        fout.write(stringaHtmlDati)
        fout.close()
        #Updating download file
        fout=open("dati.csv","a")
        fout.write(dati)
        fout.close()

        counterK=(counterK+1)%mainAppConstants.MAX_SAMPLES_STORED
        print("counterK",counterK)

        #printing content of file dati.csv for debug purpose only
        f=open("dati.csv","r")
        with f:
            print(f.read())
        f.close()
        
        #verifies if in the meanwhile WiFiSTA came up
        activateNet.do_setupWiFiSTA()

        retCode,ResetCsvFile=startWebServer(boardType,s,addrListen)
        if wait == -1:
            print('\nWaiting for TIME SLEEP.....\n')
            utime.sleep(145)
    #no_debug()