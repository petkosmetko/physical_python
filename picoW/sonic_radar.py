from machine import Pin, PWM
import utime

servo = PWM(Pin(0))
servo.freq(50)

trigger = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)
led = Pin(2, Pin.OUT)
last_servo_time = 0
servo_state = 0   # 0 = right, 1 = left

last_ultra_time = 0
distance = 0



def set_servo_ms(ms):
    duty = int((ms / 20.0) * 65535)
    servo.duty_u16(duty)

def ultrasonic():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()

    while echo.value() == 0:
        start = utime.ticks_us()
    while echo.value() == 1:
        end = utime.ticks_us()

    duration = end - start
    return (duration * 0.0343) / 2

while True:
    now = utime.ticks_ms()

    if utime.ticks_diff(now, last_ultra_time) >= 100:
        distance = ultrasonic()
        if distance < 10:
            led.value(1)
        else:
            led.value(0)
        print("Distance:", distance)
        last_ultra_time = now

    if utime.ticks_diff(now, last_servo_time) >= 1000:
        if servo_state == 0:
            set_servo_ms(1.55)  # right
            servo_state = 1
        else:
            set_servo_ms(1.45)  # left
            servo_state = 0
        last_servo_time = now

    utime.sleep_ms(5)

