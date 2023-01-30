import os
import configparser

class Dirs:
    def __init__(self):
        os.makedirs("./log",exist_ok=True)
        if not os.path.isfile(os.path.abspath(os.getcwd())+"\config.ini"):
            print("遗失config.ini....")
            token = input("please enter your token : ")
            f = open("config.ini","w+")
            f.close()
            config=configparser.ConfigParser()
            config['Telegram-BOT'] = {}
            config['Telegram-BOT']['token'] = token
            with open('config.ini', 'w') as a:
                config.write(a)
            a.close()



