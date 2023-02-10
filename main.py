import app
import multiprocessing as mp
from src.common import gui
from src import bot

def flask():
    app.flask()
def window():
    window = gui.Window()
    window.mainloop()
def botrun():
    bot.run()


if __name__=="__main__":
    p1 = mp.Process(target=flask)
    p2 = mp.Process(target=window)
    p3 = mp.Process(target=botrun)
    p1.start()
    p2.start()
    p3.start()