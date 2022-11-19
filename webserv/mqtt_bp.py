from flask import Blueprint
from flask_mqtt import Mqtt

filter = "#"

mqtt_bp = Blueprint("mqtt", __name__, url_prefix="/mqtt")

mqtt_client = Mqtt()
mqtt_client.subscribe(filter)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(filter) # subscribe topic
   else:
       print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))