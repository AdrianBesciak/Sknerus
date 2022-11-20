from flask import Flask, request, send_from_directory, current_app, Blueprint, redirect, url_for
from config import appdata

from utils_bp import utils_bp
from mqtt_bp import mqtt_client, scheduler, mqtt_bp, MA_CONFIG
from uapi_bp import uapi_bp
from auto_bp import auto_bp, schscheduler

try: # some_very_bad_trick (TM)
    import mqtt_bp as mqtt_bp_
    devices = mqtt_bp_.devices
    import uapi_bp as uapi_bp_
    uapi_bp_.devices = devices
    import auto_bp as auto_bp_
    auto_bp_.devices = devices
except BaseException as e:
    raise e
    

app = Flask(__name__)
app.config.from_mapping(
    **MA_CONFIG
)
mqtt_client.init_app(app)
scheduler.init_app(app)
scheduler.start()
schscheduler.init_app(app)
schscheduler.start()

app.register_blueprint(utils_bp)
app.register_blueprint(mqtt_bp)
app.register_blueprint(uapi_bp)
app.register_blueprint(auto_bp)

@app.route('/', methods=["GET"])
def startscreen():
    return redirect(url_for("utils.hello_world"))

@app.route('/favicon.ico', methods=["GET"])
def favicon():
    # nie dziala ale low prio
    # return redirect(url_for("utils.favicon"))
    return send_from_directory('', 'favicon.ico')

app.run(**appdata)



