import RPi.GPIO as GPIO 
import time
from time import sleep

in1 = 2
in2 = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)

GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)
time.sleep(5)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.HIGH)

