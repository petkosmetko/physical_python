# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network
import socket
import time
from machine import Pin

# Wi-Fi credentials (connect to Pico W AP)
ssid = 'PICO_LED_AP'
password = '12345678'

sta = network.WLAN(network.STA_IF)
sta.active(False)
time.sleep(1)
sta.active(True)
sta.connect(ssid, password)

while not sta.isconnected():
    print("Connecting...")
    time.sleep(1)
print("Connected to Pico W:", sta.ifconfig())

# UDP socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pico_ip = '192.168.4.1'   # default AP IP
port = 5005


while True:
    if adc.read_u16() < 65000:
        udp.sendto(b"A",(esp_led_ip, port))
        print("person detected!")
        time.sleep(0.05)

