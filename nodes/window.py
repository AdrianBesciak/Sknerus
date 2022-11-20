import RPi.GPIO as GPIO
from gpiozero import Servo
from time import sleep
import paho.mqtt.client as MQTT
import threading
import sys

room_id = int(sys.argv[1])
window_id = int(sys.argv[2])
servo_pin = int(sys.argv[3])
switch_pin = int(sys.argv[4])

class Window:
    def __init__(self, servo_pin: int, switch_pin: int, mqtt: MQTT.Client, room_id: int, window_id: int):
        self.servo = Servo(servo_pin)
        self.switch_pin = switch_pin
        self.mqtt = mqtt
        self.topic_prefix = '/'.join(['room',
                                     str(room_id), 'window', str(window_id), 'state'])
        print(self.topic_prefix)
        self.init_switch()

    def publish_state(self, pin):
        self.mqtt.publish(self.topic_prefix+'/rsp',
                          'open' if GPIO.input(self.switch_pin) == 1 else 'closed')

    def init_switch(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.switch_pin, GPIO.BOTH, bouncetime=200)
        GPIO.add_event_callback(self.switch_pin, self.publish_state)

    def notify(self, topic, message):
        if self.topic_prefix in topic:
            self.process(topic, message)

    def process(self, topic, message):
        request = topic.split('/')[-1]
        if request == 'get':
            self.publish_state(None)
        elif request == 'set':
            print("Setting servo to ", message)
            if message == b'open':
                self.servo.value = -1
            elif message == b'closed':
                self.servo.value = 0.6

mqtt = MQTT.Client()
mqtt.connect("siur123.pl", port = 18833)

w = Window(servo_pin, switch_pin, mqtt, room_id, window_id)

mqtt.on_message = lambda client, data, message:w.notify(message.topic, message.payload)
mqtt.subscribe('#')

t = threading.Thread(target=mqtt.loop_forever)
t.start()

while True:
    sleep(1000)
# def window_change_callback(channel):
#     print("GPIO ", channel, " has new state: ", GPIO.input(channel))


# GPIO.setmode(GPIO.BCM)
# GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.add_event_detect(21, GPIO.BOTH, bouncetime=200)
# GPIO.add_event_callback(21, window_change_callback)

# servo = Servo(14)

# try:
#     while True:
#         for i in range(-20, 20):
#             servo.value = i/20
#             sleep(0.1)
# except KeyboardInterrupt:
# 	print("Program stopped")
