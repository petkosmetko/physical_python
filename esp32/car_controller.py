# esp32_sta_button.py
import network
import socket
import time
import machine
from machine import Pin
led_onboard = machine.Pin(4,machine.Pin.OUT)


# Wi-Fi credentials (connect to Pico W AP)
ssid = 'PICO_LED_AP'
password = '12345678'

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid, password)

while not sta.isconnected():
    print("Connecting...")
    time.sleep(1)
print("Connected to Pico W:", sta.ifconfig())
for i in range(5):   
    led_onboard.toggle()
    time.sleep(0.2)
    led_onboard.toggle()
    time.sleep(0.2)

# UDP socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pico_ip = '192.168.4.1'   # default AP IP
port = 5005

button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(17, Pin.IN, Pin.PULL_UP)
button3 = Pin(22, Pin.IN, Pin.PULL_UP)
button4 = Pin(23, Pin.IN, Pin.PULL_UP)
button5 = Pin(18, Pin.IN, Pin.PULL_UP)
button6 = Pin(19, Pin.IN, Pin.PULL_UP)

# Main loop
last_state1 = 1
last_state2 = 1
last_state3 = 1
last_state4 = 1
last_state5 = 1
last_state6 = 1

while True:
# Right button on the right.
    state1 = button1.value()
    if state1 != last_state1:
        if state1 == 0:  # button pressed
            udp.sendto(b"OI", (pico_ip, port))
            print("pravy cudlik pravy 1")
        else:            # button released
            udp.sendto(b"OO", (pico_ip, port))
            print("pravy cudlik pravy 0")
        last_state1 = state1
# Right button on the left.
    state2 = button2.value()
    if state2 != last_state2:
        if state2 == 0:  # button pressed
            udp.sendto(b"II", (pico_ip, port))
            print("pravy cudlik lavy 1")
        else:            # button released
            udp.sendto(b"IO", (pico_ip, port))
            print("pravy cudlik lavy 0")
        last_state2 = state2
# Left button on the right.
    state3 = button3.value()
    if state3 != last_state3:
        if state3 == 0:  # button pressed
            udp.sendto(b"BOI", (pico_ip, port))
            print("lave cudliky pravy1")
        else:            # button released
            udp.sendto(b"BOO", (pico_ip, port))
            print("lave cudliky pravy 0")
        last_state3 = state3
# Left button on the left.
    state4 = button4.value()
    if state4 != last_state4:
        if state4 == 0:  # button pressed
            udp.sendto(b"BII", (pico_ip, port))
            print("lave cudliky lavy 1")
        else:            # button released
            udp.sendto(b"BIO", (pico_ip, port))
            print("lave cudliky lavy 0")
        last_state4 = state4
    
  
    time.sleep(0.05)


