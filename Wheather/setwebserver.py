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
import mainAppConstants

#dati="i;tempodareboot;tempolocaleFormattato;dsTemp;dh11_Temp;dh11Hum\r\n"
counterK=0

def parse_request(richiesta):
    richiesta_=richiesta.split("HTTP/1.")[0]
    richiesta_=richiesta_.split("GET /")[1]
    richiesta_=richiesta_.split(" ")[0]
    return richiesta_

def updateWheateherValues():
    #global dati, stringaHtmlDati
    dsTemp, dh11_Temp,dh11Hum = readenv2.getvalues()
    tempodareboot=utime.time()
    tloc=utime.localtime()
    tempolocaleFormattato=str(tloc[0])+"/"+str(tloc[1])+"/"+str(tloc[2])+"  "+str(tloc[3])+":"+str(tloc[4])+":"+str(tloc[5])
    stringaHtmlDati_loc='            <tr><td>%d</td><td>%s</td><td>%s</td><td>%2.1f</td><td>%2.1f</td><td>%2.1f</td></tr>' % (counterK, tempodareboot,tempolocaleFormattato,dsTemp, dh11_Temp,dh11Hum) +'\n'
    dati_loc=str(counterK)+";"+str(tempodareboot)+";"+str(tempolocaleFormattato)+";"+str(dsTemp)+";"+str(dh11_Temp)+";"+str(dh11Hum)+"\r\n"
    return stringaHtmlDati_loc, dati_loc

def start_server():
    try:
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(300.0)
        s.bind(addr)
        s.listen(1)
        print('listening on', addr)
    except:
        print("Exception while allocating SOCKET")
        return -1

    while True:
        try:
            cliente, addr = s.accept()
            print(cliente)
            print('client connected from:', addr)
        except:
            print("Timeout expired")
            s.close()
            #cliente.close()
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
        
        #Preparing response
        
        #Sending response
        try: #try
            if parse_request(str(request))=="file.txt": #sending dati.csv for downloading purposes
                fHeadersToSend=open('headers_download_page.txt','r')
                with fHeadersToSend:
                    for x in fHeadersToSend:
                        cliente.send(x)
                fHeadersToSend.close()
                #determine lenght of content to send
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
            else: #sending HTML page
                #response=http_headers+html+stringaHtmlDati+'            </table>\n<a href="/file.txt"><button class="button button2">GET LOG FILE!</button></a><h2>Your request was</h2>\n<code>'+request+"</code>\n"+htmlClosure
                fHeadersToSend=open('headers_main_page.txt','r')
                with fHeadersToSend:
                    for x in fHeadersToSend:
                        cliente.send(x)
                        print(x)
                fHeadersToSend.close()
                #determine lenght of content to send
                #fContentToSend=open('dati.csv','r')
                #lunghezza=0
                #for x in fContentToSend:
                #    lunghezza=lunghezza+len(x)
                #fContentToSend.close()
                
                #cliente.send(str(lunghezza)+'\r\n\r\n')
                
                fContentToSend=open('main_out.txt','r')
                with fContentToSend:
                    for x in fContentToSend:
                        cliente.send(x)
                        print(x)
                fContentToSend.close()

                cliente.send('</table>\n<a href="/file.txt"><button class="button button2">GET LOG FILE!</button></a><h2>Your request was</h2>\n<code>')
                cliente.send(request)
                cliente.send("</code>\n")

                fContentToSend=open('html_closure_main_page.txt','r')
                with fContentToSend:
                    for x in fContentToSend:
                        cliente.send(x)
                        print(x)
                fContentToSend.close()

                cliente.close()

        except: #except
            print("EXCEPTION OCCURRED WHILE SENDING DATA ON SOCKET")
            s.close()
            cliente.close()

print("Welcome to webserver section.....\n")

while True:
    #After MAX_SAMPLES_STORED samples
    if counterK == 0:
        #resets the content of files DA VALUTARE SE RESETTARLO QUESTO
        fout=open('main_out.txt','w')
        #fin=open('headers_main_page.txt','r')
        #for x in fin:
        fout.write('')
        fout.close()
        #fin.close()

        fout=open('dati.csv','w')
        fin=open('headers_download_file.txt','r')
        for x in fin:
            fout.write(x)
        fout.close()
        fin.close()

    #Getting Samples
    stringaHtmlDati, dati=updateWheateherValues()
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

    if counterK == mainAppConstants.MAX_SAMPLES_STORED-1:
        #verifies if in the meanwhile WiFiSTA came up
        activatenet.do_setupWiFiSTA()

    start_server()
#no_debug()