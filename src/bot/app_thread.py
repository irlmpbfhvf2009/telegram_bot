from flask import Flask
from threading import Thread

app = Flask(__name__)

class MyThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.daemon = True
        self.app = app
        self.app.run(debug=True, host='0.0.0.0', port=8080)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    thread = MyThread(app)
    # thread.start()
