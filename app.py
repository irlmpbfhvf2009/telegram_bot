import os ,sys
from flask import Flask,render_template
from gevent.pywsgi import WSGIServer

if getattr(sys, 'frozen', False):                                                                                                                                     
      template_folder = os.path.join(sys.executable, '..','templates')                                                                                                  
      static_folder = os.path.join(sys.executable, '..','static')                                                                                                       
      app = Flask(__name__, template_folder = template_folder,static_folder = static_folder)
else:
    app = Flask(__name__,template_folder='templates')


@app.route("/")
def index():
    return render_template(r'index.html')






@app.route("/getLog")
def get_log():
    line_number = [0]
    try:
        log_data = red_logs()
    except:
        return {'log_list' : ''}

    if len(log_data) - line_number[0] > 0:
        log_difference = len(log_data) - line_number[0]
        log_list = []
        for i in range(log_difference):
            log_i = log_data[-(i+1)].decode('utf-8')
            log_list.insert(0,log_i)
    _log = {
        'log_list' : log_list
    }
    line_number.append(len(log_data))
    return _log

def find_new_log():
    dir = os.path.abspath(os.getcwd())+"\log"
    file_lists = os.listdir(dir)
    file_lists.sort(key=lambda fn: os.path.getmtime(dir + "\\" + fn)
                  if not os.path.isdir(dir + "\\" + fn) else 0)
    log = os.path.join(dir, file_lists[-1])
    return log

def red_logs():
    log_path = find_new_log()
    with open(log_path,'rb') as f:
        log_size = os.path.getsize(log_path) 
        offset = -100
        if log_size == 0:
            return ''
        while True:
            if (abs(offset) >= log_size):
                f.seek(-log_size, 2)
                data = f.readlines()
                return data
            data = f.readlines()
            if (len(data) > 1):
                return data
            else:
                offset *= 2


if __name__ == '__main__':
    #app.run(host="0.0.0.0")
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    print(f"* Running on http://{http_server.address[0]}:{http_server.address[1]}")
    http_server.serve_forever()
