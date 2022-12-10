
import logging
import json
from telegram import *
from telegram.ext import *
import configparser


config = configparser.ConfigParser()
config.read('config.ini',encoding="utf-8")
token = config.get('telegram', 'token')
description = config.get('telegram', 'description')

with open("json/inlinekeyboardbutton.json", 'r', encoding="utf-8") as f:
    dict = json.load(f)

logging.basicConfig(level=logging.DEBUG)

updater = Updater(token)

def startCommand(update:Update,context:CallbackContext):
    buttons=[[KeyboardButton('11'),KeyboardButton('33')],[KeyboardButton('22')]]
    context.bot.send_message(chat_id=update.effective_chat.id,text="qweqwe",
    reply_markup=ReplyKeyboardMarkup(buttons))
def main():

    dispatcher=updater.dispatcher
    dispatcher.add_handler(CommandHandler("start",startCommand))
    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == "__main__":
    main()
