import time
from machine import Pin, PWM

RED = 0
GREEN = 1
BLUE = 2

pwm_pins = [13,14,15]

pwms = [PWM(Pin(pwm_pins[RED])),
        PWM(Pin(pwm_pins[GREEN])),
        PWM(Pin(pwm_pins[BLUE]))
        ]
[pwm.freq(1000) for pwm in pwms]

while True:
    pwms[RED].duty_u16(10000)
    pwms[GREEN].duty_u16(10000)
    pwms[BLUE].duty_u16(10000)


