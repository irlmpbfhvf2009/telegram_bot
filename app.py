from src import bot
from flask import Flask,render_template,jsonify,request,send_from_directory
import threading

app = Flask(__name__)

class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run(host="0.0.0.0")

@app.route("/")
def index():
    return render_template('index.html')

