import tkinter as tk
import time
import threading
import configparser

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.title(f"telegram-bot {config['Telegram-BOT']['version']}")
        self.geometry("800x600")
        self.iconbitmap("static/bot.ico")
        self.resizable(width=False,height=False)

        self.label = tk.Label(self,bg='green',width=50)
        self.label.pack()

        t_count = threading.Thread(target=self.count)
        t_count.start()

        self.mainloop()

    def count(self):
        self.label = tk.Label(self,bg='green',width=50)
        self.label.pack()
        while True:
            try:
                date = time.strftime("%Y-%m-%d   %H:%M:%S")
                self.label.config(text=date)
                self.update()
                time.sleep(1)
            except:
                break