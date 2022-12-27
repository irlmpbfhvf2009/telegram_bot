from telegram.ext import Updater
from src import _sql
import configparser

class BotConfig:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        sql = _sql.DBHP("telegram-bot.db")
        self.updater = Updater(config['Telegram-BOT']['token'])
        self.dispatcher = self.updater.dispatcher
        self.botusername = sql.botusername

