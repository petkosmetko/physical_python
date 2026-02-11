# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import machine
import time

photoresistor = machine.ADC(4)

while True:
    value = photoresistor.read_u16()
    print(value)
    time.sleep_ms(10)

