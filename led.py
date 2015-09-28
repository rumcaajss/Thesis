#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
def blink(pin):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(1)
    return
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
for i in range(0,10):
    blink(23)
GPIO.cleanup()
