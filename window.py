import RPi.GPIO as GPIO
from gpiozero import Servo
from time import sleep

def window_change_callback(channel):
    print("GPIO ", channel, " has new state: ", GPIO.input(channel))

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(21, GPIO.BOTH, bouncetime=200)
GPIO.add_event_callback(21, window_change_callback)

servo = Servo(14)

try:
    while True:
        servo.min()
        sleep(0.5)
        servo.mid()
        sleep(0.5)
        servo.max()
        sleep(0.5)
except KeyboardInterrupt:
	print("Program stopped")