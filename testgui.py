import multiprocessing as mp
import tkinter as tk
from src import bot
import time
import threading
import os

window = tk.Tk()
window.title("telegram-bot 1.6.1")
window.geometry("800x600")
window.iconbitmap("1.ico")
window.resizable(width=False,height=False)

def count():
    label = tk.Label(window,bg='green',width=50)
    label.pack()
    button.pack()
    button2.pack()  
    while True:
        try:
            date = time.strftime("%Y-%m-%d   %H:%M:%S")
            label.config(text=date)
            window.update()
            time.sleep(1)
        except:
            break

def start_bot():
    bot_path = os.path.abspath(os.getcwd()+"/executeProgram/main.exe")
    t= threading.Thread(target=os.system,args=(bot_path,))
    t.start()
    app_path = os.path.abspath(os.getcwd()+"/executeProgram/app.exe")
    t2= threading.Thread(target=os.system,args=(app_path,))
    t2.start()

t_count = threading.Thread(target=count)
t_count.start()
button = tk.Button(window,text='啟動Bot',command= start_bot , width=10,height=5,font=10)
button2 = tk.Button(window,text='開啟網頁' , width=20)


window.mainloop()