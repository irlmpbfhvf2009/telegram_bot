import configparser
from telethon import TelegramClient, events, sync
from telethon.errors import SessionPasswordNeededError
import _sql
config = configparser.ConfigParser()
config.read('config.ini')
session_name=config['Telegram-APIS']['session_name']
api_id=config['Telegram-APIS']['api_id']
api_hash=config['Telegram-APIS']['api_hash']
client = TelegramClient(config['Telegram-APIS']['session_name'], api_id=config['Telegram-APIS']['api_id'], api_hash=config['Telegram-APIS']['api_hash'])
#client.connect()
#client.start()

sql = _sql.DBHP("telegram-bot.db")

time = sql.inviteFriendsAutoClearTime
print(type(time))