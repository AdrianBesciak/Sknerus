import RPi.GPIO as GPIO

def window_change_callback(channel):
    print("GPIO ", channel, " has new state: ", GPIO.input(channel))

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(21, GPIO.BOTH, bouncetime=200)
GPIO.add_event_callback(21, window_change_callback)
while True:
    pass