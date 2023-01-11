from src import bot
from flask import Flask,render_template,jsonify,request,send_from_directory
import threading
import app

class TelegramThread(threading.Thread):
    def run(self) -> None:
        try:
            bot.run()
        except:
            ...

if __name__ == '__main__':
    flask_thread = app.FlaskThread()
    telegram_thread = TelegramThread()
    flask_thread.start()
    telegram_thread.start()