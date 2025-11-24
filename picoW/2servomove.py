# pico_ap_led.py
import network
import socket
from machine import Pin, PWM
import time

led_onboard = machine.Pin("LED",machine.Pin.OUT)


servo1 = PWM(Pin(0))
servo2 = PWM(Pin(1))

servo1.freq(50)
servo2.freq(50)


def set_servo_ms(servo, ms):
    duty = int((ms / 20.0) * 65535)
    servo.duty_u16(duty)

# -------- Controls --------

def stop(serv):
    set_servo_ms(serv,1.5)   # 1.5 ms → stop

def full_speed_cw(serv):
    set_servo_ms(serv,2.0)   # 2.0 ms → CW max

def full_speed_ccw(serv):
    set_servo_ms(serv,1.0)   # 1.0 ms → CCW max

def slow_cw(serv):
    set_servo_ms(serv,1.7)   # Slightly above 1.5 ms

def slow_ccw(serv):
    set_servo_ms(serv,1.3)   # Slightly below 1.5 ms


def raketovy_pohon1():
    full_speed_ccw(servo1)

def raketovy_pohon2():
    full_speed_ccw(servo2)
    
def raketovy_reverse1():
    full_speed_cw(servo1)

def raketovy_reverse2():
    full_speed_cw(servo2)

def stop1():
    stop(servo1)

def stop2():
    stop(servo2)

'''

'''
# Start wifi Access Point
ap = network.WLAN(network.AP_IF)
ap.config(essid='PICO_LED_AP', password='12345678')
ap.active(True)
print('Access Point active, IP:', ap.ifconfig()[0])

# UDP setup
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('0.0.0.0', 5005))
for i in range(5):   
    led_onboard.toggle()
    time.sleep(0.2)
    led_onboard.toggle()
    time.sleep(0.2)
print("Listening for button packets...")

while True:
    data, addr = udp.recvfrom(1024)
    msg = data.decode().strip()
    print("Received:", msg)

    if msg == "OI":
        raketovy_pohon1()
    elif msg == "OO":
        stop1()
    if msg == "II":
        raketovy_reverse1()
    elif msg == "IO":
        stop1()

    if msg == "BOI":
        raketovy_pohon2()
    elif msg == "BOO":
        stop2()
    if msg == "BII":
        raketovy_reverse2()
    elif msg == "BIO":
        stop2()
        


