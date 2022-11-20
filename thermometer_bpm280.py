from time import sleep
import paho.mqtt.client as MQTT
import threading
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bmp280 import BMP280

import sys

room_id = int(sys.argv[1])

class Thermometer_BMP280:
    def __init__(self, mqtt: MQTT.Client, room_id: int):
        self.mqtt = mqtt
        self.topic_prefix = '/'.join(['room',
                                     str(room_id), 'temperature', '0', 'value'])
        i2c = SMBus(1)
        self.sensor = BMP280(i2c_dev=i2c)
        print(self.sensor.get_temperature())

    def publish_state(self, pin):
        self.mqtt.publish(self.topic_prefix+'/rsp',
                          str(self.sensor.get_temperature()))

    def notify(self, topic, message):
        if self.topic_prefix in topic:
            self.process(topic, message)

    def process(self, topic, message):
        request = topic.split('/')[-1]
        if request == 'get':
            self.publish_state(None)


mqtt = MQTT.Client()
mqtt.connect("siur123.pl", port=18833)

w = Thermometer_BMP280(mqtt, room_id)

mqtt.on_message = lambda client, data, message: w.notify(
    message.topic, message.payload)
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
