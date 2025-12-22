import time
from machine import Pin, PWM, ADC

RED = 0
GREEN = 1
BLUE = 2

adcpin1 = 26
adcpin2 = 27
adcpin3 = 28

button = machine.Pin(0,machine.Pin.IN, machine.Pin.PULL_UP)

pot1 = ADC(adcpin1)
pot2 = ADC(adcpin2)
pot3 = ADC(adcpin3)

pwm_pins = [13,14,15]

pwms = [PWM(Pin(pwm_pins[RED])),
        PWM(Pin(pwm_pins[GREEN])),
        PWM(Pin(pwm_pins[BLUE]))]
for pwm in pwms:
    pwm.freq(1000)

def ReadPotentiometer1():
    adcpin = 26
    pot = ADC(adcpin1)
    
    adc_value1 = pot.read_u16()
    return adc_value1

def ReadPotentiometer2():
    adcpin = 27
    pot = ADC(adcpin2)
    
    adc_value2 = pot.read_u16()
    return adc_value2

def ReadPotentiometer3():
    adcpin = 28
    pot = ADC(adcpin3)
    
    adc_value3 = pot.read_u16()
    return adc_value3

def basic_svetielka():
    while True:
        potvalue1 = ReadPotentiometer1()
        potvalue2 = ReadPotentiometer2()
        potvalue3 = ReadPotentiometer3()

        pwms[RED].duty_u16(int(potvalue1))
        pwms[GREEN].duty_u16(int(potvalue2))
        pwms[BLUE].duty_u16(int(potvalue3))
        if not button.value() == 1:
                    pulse()
def pulse():
    last_state = 0
    while last_state <1:
        for i in range(0,66):
            time.sleep(0.06)
            rgb_value = i*1000
            print(rgb_value)

        for i in range(66,-1,-1):
            time.sleep(0.06)
            rgb_value = i*1000
            print(rgb_value)
            if not button.value() == 1:
                basic_svetielka()
                last_state =+ 3

while True:
    basic_svetielka()

