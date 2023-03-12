from multiprocessing import freeze_support, Process
from src.tkinter.gui import runGui

if __name__ == "__main__":
    freeze_support()
    windowProcess = Process(target=runGui)
    windowProcess.start()
    windowProcess.join()