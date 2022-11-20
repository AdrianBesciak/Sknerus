from flask import Flask, request, send_from_directory, current_app, Blueprint, redirect, url_for
from flask.wrappers import Response

from utils_bp import utils_bp
from mqtt_bp import mqtt_client, scheduler, mqtt_bp, MA_CONFIG

app = Flask(__name__)
app.config.from_mapping(
    **MA_CONFIG
)
mqtt_client.init_app(app)
scheduler.init_app(app)
scheduler.start() # potrzebne?

app.register_blueprint(utils_bp)
app.register_blueprint(mqtt_bp)

@app.route('/', methods=["GET"])
def startscreen():
    return redirect(url_for("utils.hello_world"))

@app.route('/favicon.ico', methods=["GET"])
def favicon():
    # nie dziala ale low prio
    # return redirect(url_for("utils.favicon"))
    return send_from_directory('', 'favicon.ico')

app.run(    
    host = "localhost",
    port = 5000,
)



