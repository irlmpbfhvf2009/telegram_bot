import time,threading,configparser,webbrowser,tkinter,logging,os,signal,datetime
from multiprocessing import Process
from src.common import logger
from src.common.utils import chick_port
from src.web.app import flask
from src.bot.bot import run

class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.title(f"telegram-bot {config['Telegram-BOT']['version']}")
        self.geometry("800x600")
        self.resizable(width=False,height=False)
        
        self.label = tkinter.Label(self,bg='green',width=50)
        self.label.pack()
        self.button3 = tkinter.Button(self,text="開啟網頁",command=self.appStart)
        self.button3.pack()
        self.button3 = tkinter.Button(self,text="啟動機器人",command=self.botStart)
        self.button3.pack()

        # 日誌輸出
        self.normalTextBox = tkinter.Text(self, width=70,height=20)
        self.normalTextBox.place(x=40,y=200)
        self.log=logger.Logging(file='log/'+str(datetime.datetime.now().date())+'.log')
        handler = TextboxHandler(self.normalTextBox)
        self.log.addHandler(handler)
 
        threading.Thread(target=self.count).start()
        self.appPid = 987654321987654321987654321
        self.botPid = 987654321987654321987654312
        self.protocol('WM_DELETE_WINDOW', self.windowClose)
        self.log.info("界面载入完成")
        self.mainloop()

    def windowClose(self):
        try:
            os.kill(self.appPid, signal.SIGTERM)
            os.kill(self.botPid, signal.SIGTERM)
        except:
            print("退出程序")
        self.quit()
        self.destroy()
        

    def count(self):
        while True:
            try:
                date = time.strftime("%Y-%m-%d   %H:%M:%S")
                self.label.config(text=date)
                self.update()
                time.sleep(1)
            except:
                break

    def appStart(self):
        if(chick_port()==False):
            app = Process(target=flask)
            app.start()
            self.appPid=app.pid
            urL='http://127.0.0.1:5555'
            webbrowser.get('windows-default').open_new(urL)
        else:
            urL='http://127.0.0.1:5555'
            webbrowser.get('windows-default').open_new(urL)

    def botStart(self):
        bot = Process(target=run)
        bot.start()
        self.botPid=bot.pid


class TextboxHandler(logging.Handler):
    def __init__(self, textbox):
        logging.Handler.__init__(self)
        self.textbox = textbox
 
    def emit(self, record):
        msg = self.format(record)
        self.textbox.insert("end", msg + "\n")