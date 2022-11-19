from lamp import *

class Boiler(Lamp):
    def __init__(self, led_pin: int, mqtt: MQTT.Client, room_id: int):
        super.__init__(self, led_pin, mqtt, room_id)
        self.topic_prefix = '/'.join(['room',
                                      str(room_id), 'boiler'])

