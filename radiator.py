from lamp import *

room_id = int(sys.argv[1])
radiator_pin = int(sys.argv[2])

class Radiator(Lamp):
    def __init__(self, led_pin: int, mqtt: MQTT.Client, room_id: int):
        super.__init__(self, led_pin, mqtt, room_id)
        self.topic_prefix = '/'.join(['room',
                                      str(room_id), 'radiator', '0', 'state'])


mqtt = MQTT.Client()
mqtt.connect("siur123.pl", port=18833)

w = Radiator(radiator_pin, mqtt, room_id)

mqtt.on_message = lambda client, data, message: w.notify(
    message.topic, message.payload)
mqtt.subscribe('#')

t = threading.Thread(target=mqtt.loop_forever)
t.start()

while True:
    sleep(1000)
