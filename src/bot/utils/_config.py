from telegram.ext import Updater
import configparser
import tkinter as tk

class BotConfig:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            self.updater = Updater(config['Telegram-BOT']['token'])
        except KeyError:
            def center_window(w, h):
                ws = root.winfo_screenwidth()
                hs = root.winfo_screenheight()
                x = (ws/2) - (w/2)
                y = (hs/2) - (h/2)
                root.geometry('%dx%d+%d+%d' % (w, h, x, y))
            root = tk.Tk()
            def _exit():
                root.quit()
                root.destroy()
            root.title('oxxo.studio')
            center_window(300,200)

            entry = tk.Entry(root)  # 放入單行輸入框
            entry.pack()
            btn1 = tk.Button(root, text='確認')   # 放入顯示按鈕，點擊後執行 show 函式
            btn1.pack()
            btn2 = tk.Button(root, text='取消',command=_exit)  # 放入清空按鈕，點擊後執行 clear 函式
            btn2.pack()
            root.mainloop()
            
            
        self.botusername = self.updater.bot.username
        self.dispatcher = self.updater.dispatcher
