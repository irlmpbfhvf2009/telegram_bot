from multiprocessing import freeze_support, Process
# from src.bot.bot import run
from src.tkinter.gui import runGui
freeze_support()

if __name__ == "__main__":
    # windowProcess = Process(target=run)
    windowProcess = Process(target=runGui)
    windowProcess.start()
    windowProcess.join()