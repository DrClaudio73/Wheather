import Wheather
import uos
import activateNet
import utime

activateNet.do_setupWiFiAP()
activateNet.do_setupWiFiSTA()

tempoalboot=utime.time()

Wheather.main(uos.uname().sysname,tempoalboot)
