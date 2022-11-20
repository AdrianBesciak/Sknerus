import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as MQTT
import w1thermsensor

class Thermometer:
    def __init__(self, mqtt: MQTT.Client, room_id: int):
        self.mqtt = mqtt
        self.topic_prefix = '/'.join(['room',
                                     str(room_id), 'temperature/0/value/rsp'])
        self.sensor = w1thermsensor.W1ThermSensor()

    def publish_state(self):
        self.mqtt.publish(self.topic_prefix, sensor.get_temperature().str())

    def notify(self, topic, message):
        if self.topic_prefix in topic:
            self.process(topic, message)

    def process(self, topic, message):
        request = topic.split('/')[-1]
        if request == 'get':
            self.publish_state()
