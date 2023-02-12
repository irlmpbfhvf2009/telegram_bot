from telegram.ext import Updater
import configparser

class BotConfig:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.updater = Updater(config['Telegram-BOT']['token'])
        self.dispatcher = self.updater.dispatcher
