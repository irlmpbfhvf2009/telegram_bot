import app
import multiprocessing as mp
from src.common.gui import Window
from src import bot

mp.freeze_support()

if __name__=="__main__":
    p1 = mp.Process(target=app.flask)
    p2 = mp.Process(target=Window)
    p1.start()
    p2.start()
    bot.run()