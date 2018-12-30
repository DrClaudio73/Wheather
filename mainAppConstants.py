#USED CONSTANTS
MAX_SAMPLES_STORED = 3000
ESP8266_TS_PIN=4
ESP8266_DHT_PIN=5
ESP32_TS_PIN=22
ESP32_DHT_PIN=23

SOCKETTIMEOUT=300.0

OK = 0
KO = -1
STA_AVAILABLE= OK

THREAD_INTERVAL=50
MAX_KKK_WD=int(SOCKETTIMEOUT/THREAD_INTERVAL+2)