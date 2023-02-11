import tkinter as tk
import time,threading,configparser,webbrowser 
from multiprocessing import Process,freeze_support
#import os,signal
from src.common import logger
import logging
from src.web.app import flask
from src.bot.bot import run
from src.bot import bot

freeze_support()
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.title(f"telegram-bot {config['Telegram-BOT']['version']}")
        self.geometry("800x600")
        self.iconbitmap("src/tkinter/bot.ico")
        self.resizable(width=False,height=False)
        
        self.label = tk.Label(self,bg='green',width=50)
        self.label.pack()
        self.button3 = tk.Button(self,text="開啟網頁",command=self.openUrl)
        self.button3.pack()
        self.button6 = tk.Button(self,text="log",command=self.btn_command)
        self.button6.pack()

        # 日誌輸出
        normalTextBox = tk.Text(self, width=50,height=5)
        normalTextBox.place(x=40,y=200)
        self.log=bot.log
        handler = TextboxHandler(normalTextBox)
        self.log.addHandler(handler)
 
        t_count = threading.Thread(target=self.count)
        t_count.start()
        
        self.appStart()
        self.botStart()
        self.protocol('WM_DELETE_WINDOW', self.windowClose(self,))
        self.mainloop()

    def windowClose(self,root):
        self.apps.terminate()
        self.apps.join()
        self.bot.terminate()
        self.bot.join()
        root.destroy
        
    def openUrl(self):
        urL='http://127.0.0.1:5555'
        webbrowser.get('windows-default').open_new(urL)

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
        self.apps = Process(target=flask)
        self.apps.start()

    def botStart(self):
        self.bot = Process(target=run)
        self.bot.start()

    def btn_command(self):
        self.log.info(f"LoggerBox")

class TextboxHandler(logging.Handler):
    def __init__(self, textbox):
        logging.Handler.__init__(self)
        self.textbox = textbox
 
    def emit(self, record):
        msg = self.format(record)
        self.textbox.insert("end", msg + "\n")