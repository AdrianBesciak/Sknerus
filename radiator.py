from lamp import *


class Radiator(Lamp):
    def __init__(self, led_pin: int, mqtt: MQTT.Client, room_id: int):
        super.__init__(self, led_pin, mqtt, room_id)
        self.topic_prefix = '/'.join(['room',
                                      str(room_id), 'radiator', '0', 'state'])


mqtt = MQTT.Client()
mqtt.connect("siur123.pl", port=18833)

w = Radiator(21, mqtt, 15)

mqtt.on_message = lambda client, data, message: w.notify(
    message.topic, message.payload)
mqtt.subscribe('#')

t = threading.Thread(target=mqtt.loop_forever)
t.start()

while True:
    sleep(1000)
