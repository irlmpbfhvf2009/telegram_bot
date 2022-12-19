import configparser
import json
from telegram.ext import Updater
import _sql

sql=_sql.DBHP("telegram-bot.db")
class BotConfig:
    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('config.ini',encoding="utf-8")
        self.description = self.config.get('telegram-bot', 'description')
        self.botusername = sql.botusername
        self.password = sql.password
        self.manager = json.loads(self.config.get('telegram-bot', 'manager'))
        self.group =  json.loads(self.config.get('telegram-bot', 'group'))
        self.useGroup = json.loads(self.config.get('telegram-bot', 'useGroup'))
        self.addLink = f'http://t.me/{sql.botusername}?startgroup&admin=change_info'
        self.groupLink='https://t.me/+-DZY9TwhnOlhMDc9'
        self.updater = Updater(sql.token)
        self.dispatcher = self.updater.dispatcher


        #self.botusername = self.config.get('telegram-bot', 'botUsername')
        #self.password = self.config.get('telegram-bot', 'password')
        #self.addLink = f'http://t.me/{self.botusername}?startgroup&admin=change_info'
        #self.updater = Updater(self.config.get('telegram-bot', 'token'))


