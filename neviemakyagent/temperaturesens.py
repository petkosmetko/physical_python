from machine import Pin
from time import sleep
import dht
 
sensor = dht.DHT11(Pin(15))
 
while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
 
    print(temp, 'C')
    print(hum, '%')
 
    sleep(0.5)
