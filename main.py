from multiprocessing import freeze_support, Process
from src.tkinter.gui import Window
from src.common.utils import makedirs
import os
freeze_support()

if __name__ == "__main__":
    makedirs(path = os.path.abspath(os.path.dirname(__file__)) + '\\log')
    windowProcess = Process(target=Window)
    windowProcess.start()
    windowProcess.join()