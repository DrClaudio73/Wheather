# This file is executed on every boot (including wake-boot from deepsleep)
def no_debug():
    import esp
    esp.osdebug(None)

import uos
if uos.uname().sysname == "esp32":
    no_debug()

import gc
#import webrepl
#webrepl.start()
gc.collect()

#init a fake i time in case the STA won't be available
import machine
rtc=machine.RTC()
rtc.datetime((2019,1,1,0,0,0,1,1))
#rtc.init((2019,1,1,0,0,0,1,1))
