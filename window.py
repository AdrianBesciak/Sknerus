import RPi.GPIO as GPIO
from gpiozero import Servo
from time import sleep
import paho.mqtt.client as MQTT


class Window:
    def __init__(self, servo_pin: int, switch_pin: int, mqtt: MQTT.Client, room_id: int, window_id: int):
        self.servo = Servo(servo_pin)
        self.switch_pin = switch_pin
        self.mqtt = mqtt
        self.topic_prefix = '/'.join(['room',
                                     str(room_id), 'window', str(window_id)])
        self.init_switch()

    def publish_switch_state(self):
        self.mqtt.publish(self.topic_prefix+'/state',
                          'open' if GPIO.input(self.switch_pin) == 1 else 'closed')

    def init_switch(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.switch_pin, GPIO.BOTH, bouncetime=200)
        GPIO.add_event_callback(self.switch_pin, self.publish_switch_state)

    def notify(self, topic, message):
        if self.topic_prefix in topic:
            self.process(topic, message)

    def process(self, topic, message):
        request = topic.split('/')[-1]
        if request == 'get':
            self.publish_switch_state()
        elif request == 'set':
            if message == 'open':
                self.servo.value = 1
            elif message == 'closed':
                self.servo.value = -1





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
