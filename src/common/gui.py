import tkinter as tk
import time
import threading

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("telegram-bot 1.6.1")
        self.geometry("800x600")
        self.iconbitmap("1.ico")
        self.resizable(width=False,height=False)

        self.label = tk.Label(self,bg='green',width=50)
        self.label.pack()

        t_count = threading.Thread(target=self.count)
        t_count.start()

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
