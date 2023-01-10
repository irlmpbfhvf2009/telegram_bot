from src import bot
from flask import Flask,render_template,jsonify,request,send_from_directory
import threading
from src import _sql

app = Flask(__name__)

class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run(host="0.0.0.0")

class TelegramThread(threading.Thread):
    def run(self) -> None:
        try:
            bot.run()
        except:
            ...
            
            
def runSQL():
    return _sql.DBHP("telegram-bot.db")


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/getPassword")
def getPassword():
    sql = runSQL()
    password = sql.password
    return password

if __name__ == '__main__':
    flask_thread = FlaskThread()
    telegram_thread = TelegramThread()
    flask_thread.start()
    telegram_thread.start()