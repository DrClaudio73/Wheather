# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()
gc.collect()

#import readenv2
#import setwebserver

import activatenet

activatenet.do_setupWiFiAP()
activatenet.do_setupWiFiSTA()

import setwebserver