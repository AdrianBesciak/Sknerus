from flask import Flask, request, send_from_directory, Response, current_app, Blueprint, redirect, url_for

from utils_bp import utils_bp

app = Flask(__name__)

@app.route('/', methods=["GET"])
def startscreen():
    return redirect(url_for("utils.hello_world"))

@app.route('/favicon.ico', methods=["GET"])
def favicon():
    pass
    # return redirect(url_for("utils.favicon"))
    # return send_from_directory('', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

app.register_blueprint(utils_bp)
app.run("localhost", 5000)