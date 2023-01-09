from src import bot
from flask import Flask,render_template,jsonify,request,send_from_directory
import os
import threading

app = Flask(__name__)
app.debug = False
@app.route("/")
def hello():
    return render_template('index.html')

def runHtml():
    return os.system("flask run")
def runBOT():
    return bot.run()
if __name__ == '__main__':
    html = threading.Thread(target=runHtml)
    b= threading.Thread(target=runBOT)
    #os.system("flask run")
    #bot.run()
    b.start()
    html.start()