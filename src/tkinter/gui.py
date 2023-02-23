import time,threading,configparser,webbrowser,tkinter,os,signal,datetime,inspect,ctypes
import tkinter.font as tkFont
from tkinter import messagebox
from multiprocessing import Process
from src.common import logger
from src.common.utils import chick_port,Log,makedirs,currentDirectory
#from src.web.app import flask
# from src.bot.bot import run
from src.sql._sql import DBHP

class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        config = configparser.ConfigParser()
        if os.path.isfile('config.ini'):
            config.read('config.ini')
            try:
                self.token = config['Telegram-BOT']['token']
                self.version = "1.6.4"
            except KeyError:
                config['Telegram-BOT'] = { 'token': '','version': '1.6.4' }
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
        else:
            config['Telegram-BOT'] = { 'token':'','version': '1.6.4' }
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            self.token = config['Telegram-BOT']['token']
            self.version = "1.6.4"
            
            
        self.title("telegram-bot")
        makedirs(path = currentDirectory() + '\\log')
        with open(os.path.abspath(os.getcwd())+"\log\gui_.log",'a+',encoding='utf-8') as test:
            test.truncate(0)
        self.log=logger.Logging(file='log/'+str(datetime.datetime.now().date())+'.log',guiFile='log/gui_.log')
        def center_window(w, h):
            ws = self.winfo_screenwidth()
            hs = self.winfo_screenheight()
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)
            self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        center_window(700,400)
        self.resizable(width=False,height=False)
        fontStyle = tkFont.Font(family="Lucida Grande", size=16)
        self.label_time = tkinter.Label(self,font=fontStyle)
        self.label_botstate = tkinter.Label(self,text="BOT状态：未启动")
        self.label_appstate = tkinter.Label(self,text="网页状态：未启动")
        self.label_botusername = tkinter.Label(self,text="机器人：")
        self.label_version = tkinter.Label(self,text="版本号："+self.version)
        self.label_token = tkinter.Label(self,text="Token："+self.token)
        
        self.button_app_run = tkinter.Button(self,text="开启网页",command=self.appStart,width=9,height=2)
        self.button_bot_run = tkinter.Button(self,text="启动BOT",command=self.botStart,width=9,height=2)
        
        # 日誌輸出
        self.normalTextBox = tkinter.Text(self, width=98,height=10)
        self.normalTextBox.bind("<Key>", lambda e: self.ctrlEvent(e))
        #self.log.addHandler(TextboxHandler(self.normalTextBox))
        
        # 布局
        self.label_time.place(x=50, y=20)
        self.label_botstate.place(x=50,y=60)
        self.label_appstate.place(x=50,y=90)
        self.label_botusername.place(x=50,y=120)
        self.label_token.place(x=50,y=150)
        self.label_version.place(x=50,y=180)
        
        self.button_bot_run.place(x=550, y=40)
        self.button_app_run.place(x=450, y=40)
        self.normalTextBox.place(x=5, y=250)
        
        
        self.t_count = threading.Thread(target=self.count)
        self.t_inftxt = threading.Thread(target=self.in_f_txt)
        self.t_count.start()
        self.t_inftxt.start()
        
        self.appPid = 987654321987654321987654321
        self.botPid = 987654321987654321987654312
        self.protocol('WM_DELETE_WINDOW', self.windowClose)

    def windowClose(self):
        try:
            os.kill(self.appPid, signal.SIGTERM)
            os.kill(self.botPid, signal.SIGTERM)
        except:
            print("退出程序")
        finally:
            self.stop_thread(self.t_count)
            self.stop_thread(self.t_inftxt)
            self.quit()
            self.destroy()
        
    def ctrlEvent(self,event):
        if(12==event.state and event.keysym=='c' ):
            return
        else:
            return "break"

    def count(self):
        while True:
            try:
                date = time.strftime("%Y-%m-%d   %H:%M:%S")
                self.label_time.config(text=date)
                self.update()
                time.sleep(1)
            except:
                break
            
    def in_f_txt(self):
        while True:
            try:
                self.normalTextBox.delete('1.0','end')
                file=os.path.abspath(os.getcwd())+"\log\gui_.log"
                if os.path.exists(file):
                    with open(file,'r',encoding='utf-8') as logFile:
                        i=0
                        for r in logFile:
                            i+=1
                            self.normalTextBox.insert("insert",r)
                        self.normalTextBox.see(str(i)+".0")
                        time.sleep(5)
            except Exception as e:
                self.log.info(e)
                break
            
    def log_count(self):
        file=Log().find_new_log
        if os.path.exists(file):
            count = 0
            with open(file, 'rb') as f :
                while True:
                    line = f.readline()
                    if not line:
                        break
                    count +=1
            return str(count)
        return "0"


            
    def appStart(self):
        port = 5556
        if(chick_port(port=port)==False):
            from src.web.app import flask
            app = Process(target=flask,args=(port,))
            app.start()
            self.appPid=app.pid
            urL=f'http://127.0.0.1:{port}'
            webbrowser.get('windows-default').open_new(urL)
            self.label_appstate.config(text=f"网页状态：已启动 port:{str(port)}")
            self.log.info("伺服器启动")
            self.log.info(f"Running on http:127.0.0.1:{port}")
        else:
            urL=f'http://127.0.0.1:{port}'
            webbrowser.get('windows-default').open_new(urL)

    def botStart(self):
        from telegram import TelegramError
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.label_token.config(text="Token："+ config['Telegram-BOT']['token'])
        
        try:
            from src.bot.bot import run
            bot = Process(target=run)
            bot.start()
            self.botPid=bot.pid
            self.button_bot_run.config(text="停止BOT",command=self.botStop)
            self.label_botstate.config(text="BOT状态：已启动")
            self.label_botusername.config(text="机器人："+DBHP().botusername)
        except TelegramError as e:
            if str(e) == "Invalid token":
                messagebox.showwarning('Invalid token', '请检查config.ini')
                self.log.info("Invalid token")
        except Exception as e:
            self.log.info(str(e))

        
    def botStop(self):
        os.kill(self.botPid, signal.SIGTERM)
        self.log.info("BOT停止运作")
        self.button_bot_run.config(text="启动BOT",command=self.botStart)
        self.label_botstate.config(text="BOT状态：未启动")
        
    def _async_raise(self,tid, exctype):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    def stop_thread(self,thread):
        self._async_raise(thread.ident, SystemExit)
    
            
def runGui():
    Window().mainloop()

#class TextboxHandler(logging.Handler):
#    def __init__(self, textbox):
#        logging.Handler.__init__(self)
#        self.textbox = textbox
# 
#    def emit(self, record):
#        msg = self.format(record)
#        self.textbox.insert("end", msg + "\n")