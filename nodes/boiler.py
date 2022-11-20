import RPi.GPIO as GPIO
from gpiozero import Servo
from time import sleep
import paho.mqtt.client as MQTT
import threading
import sys

room_id = int(sys.argv[1])
boiler_pin = int(sys.argv[2])

class Boiler:
    def __init__(self, led_pin: int, mqtt: MQTT.Client, room_id: int):
        self.pin = led_pin
        self.mqtt = mqtt
        self.topic_prefix = '/'.join(['room',
                                      str(room_id), 'boiler', '0', 'state'])
        print(self.topic_prefix)
        self.init_pin()

    def publish_state(self, pin):
        self.mqtt.publish(self.topic_prefix+'/rsp',
                          'on' if GPIO.input(self.pin) == 1 else 'off')

    def init_pin(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

    def notify(self, topic, message):
        if self.topic_prefix in topic:
            self.process(topic, message)

    def process(self, topic, message):
        request = topic.split('/')[-1]
        if request == 'get':
            self.publish_state(None)
        elif request == 'set':
            print("Setting Boiler to ", message)
            if message == b'on':
                GPIO.output(self.pin, GPIO.HIGH)
            elif message == b'off':
                GPIO.output(self.pin, GPIO.LOW)


mqtt = MQTT.Client()
mqtt.connect("siur123.pl", port=18833)

w = Boiler(boiler_pin, mqtt, room_id)

mqtt.on_message = lambda client, data, message: w.notify(
    message.topic, message.payload)
mqtt.subscribe('#')

t = threading.Thread(target=mqtt.loop_forever)
t.start()

while True:
    sleep(1000)
