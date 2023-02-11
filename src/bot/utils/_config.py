from telegram.ext import Updater
from src.sql._sql import DBHP
from configparser import ConfigParser

class BotConfig:
    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        sql = DBHP()
        self.updater = Updater(config['Telegram-BOT']['token'])
        self.dispatcher = self.updater.dispatcher
        self.botusername = sql.botusername

