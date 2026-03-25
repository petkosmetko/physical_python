# This file is executed on every boot (including wake-boot from deepsleep)

import network
import socket
import time
from machine import Pin, ADC

# =============================
# ADC SETUP (adjust pin if needed)
# =============================
adc = ADC(Pin(0))   # change pin if your sensor is on different GPIO

# =============================
# WIFI SETTINGS
# =============================
ssid = 'PICO_LED_AP'
password = '12345678'

sta = network.WLAN(network.STA_IF)

# ===== Minimal fixes for ESP32-C3 =====
# Reset interface
if sta.isconnected():
    sta.disconnect()
sta.active(False)
time.sleep(0.5)
sta.active(True)

# Disable power save (prevents handshake/internal state errors)
sta.config(pm=0)

# Connect to AP
sta.connect(ssid, password)
# =======================================

timeout = 15
start = time.time()

while not sta.isconnected():
    status = sta.status()
    print("Status:", status)

    if status < 0:
        print("Connection failed with status:", status)
        break

    if time.time() - start > timeout:
        print("Connection timeout")
        break

    time.sleep(1)

if not sta.isconnected():
    print("WiFi FAILED")
    raise RuntimeError("WiFi failed")

print("Connected to Pico W:", sta.ifconfig())

# =============================
# UDP SETUP
# =============================
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pico_ip = '192.168.4.1'   # default Pico W AP IP
port = 5005

print("Starting main loop...")

# =============================
# MAIN LOOP
# =============================
while True:
    value = adc.read_u16()

    if value < 65000:
        udp.sendto(b"A", (pico_ip, port))
        print("Person detected! ADC:", value)
        time.sleep(0.05)

    time.sleep(0.01)

