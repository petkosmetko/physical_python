import time
from machine import Pin, PWM, ADC


RED = 0
GREEN = 1
BLUE = 2

adcpin1 = 0
adcpin2 = 1
adcpin3 = 2

pot1 = ADC(adcpin1)
pot2 = ADC(adcpin2)
pot3 = ADC(adcpin3)

pwm_pins = [5,6,7]

pwms = [PWM(Pin(pwm_pins[RED])),
        PWM(Pin(pwm_pins[GREEN])),
        PWM(Pin(pwm_pins[BLUE]))
        ]
[pwm.freq(1000) for pwm in pwms]
def ReadPotentiometer1():
    pot = ADC(adcpin1)
    
    adc_value1 = pot.read_u16()
    return adc_value1

def ReadPotentiometer2():
    pot = ADC(adcpin2)
    
    adc_value2 = pot.read_u16()
    return adc_value2

def ReadPotentiometer3():
    pot = ADC(adcpin3)
    
    adc_value3 = pot.read_u16()
    return adc_value3

while True:
    potvalue1 = ReadPotentiometer1()
    potvalue2 = ReadPotentiometer2()
    potvalue3 = ReadPotentiometer3()

    pwms[RED].duty_u16(int(potvalue1))
    pwms[GREEN].duty_u16(int(potvalue2))
    pwms[BLUE].duty_u16(int(potvalue3))
    
