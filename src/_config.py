import configparser
import json
from telegram.ext import Updater
import time
import logging

class BotConfig:
    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('config.ini',encoding="utf-8")
        self.description = self.config.get('telegram-bot', 'description')
        self.botusername = self.config.get('telegram-bot', 'botUsername')
        self.password = self.config.get('telegram-bot', 'password')
        self.manager = json.loads(self.config.get('telegram-bot', 'manager'))
        self.group =  json.loads(self.config.get('telegram-bot', 'group'))
        self.useGroup = json.loads(self.config.get('telegram-bot', 'useGroup'))
        self.addLink = f'http://t.me/{self.botusername}?startgroup&admin=change_info'
        self.groupLink='https://t.me/+-DZY9TwhnOlhMDc9'
        self.updater = Updater(self.config.get('telegram-bot', 'token'))
        self.dispatcher = self.updater.dispatcher

        logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]  %(levelname)s [%(filename)s %(funcName)s] [ line:%(lineno)d ] %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[logging.StreamHandler(),logging.FileHandler(f'log//{time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())}.log', 'w', 'utf-8')])


