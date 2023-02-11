from multiprocessing import freeze_support,Process
from src.tkinter.gui import Window

freeze_support()

if __name__=="__main__":
    windowProcess = Process(target=Window)
    windowProcess.start()
    windowProcess.join()