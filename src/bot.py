import logging
import json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton ,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater, Filters,RegexHandler, CallbackContext,CommandHandler,MessageHandler,ConversationHandler
import configparser

logging.basicConfig(level=logging.DEBUG)
config = configparser.ConfigParser()
config.read('config.ini',encoding="utf-8")
description = config.get('telegram-bot', 'description')
botusername = config.get('telegram-bot', 'botUsername')
manager = json.loads(config.get('telegram-bot', 'manager'))
addLink = f'http://t.me/{botusername}?startgroup&admin=change_info'
groupLink='https://t.me/+-DZY9TwhnOlhMDc9'
updater = Updater(config.get('telegram-bot', 'token'))
dispatcher = updater.dispatcher
job_queue = updater.job_queue


START,WORKFLOW = range(2)


with open("./json/keyBoardButton.json", 'r', encoding="utf-8") as f:
    dict = json.load(f)

def start(update:Update,context:CallbackContext):
    chat_id = update.effective_chat.id
    buttons=[[KeyboardButton(dict['howToAddMeToYourGroup']),KeyboardButton(dict['managementPanel'])],
             [KeyboardButton(dict['commandsList']),KeyboardButton(dict['supportGroup'])]]
    context.bot.send_message(chat_id=chat_id,text="What con this bot do?\nPlease tap on START",
                                            reply_markup=ReplyKeyboardMarkup(buttons))
    return WORKFLOW

def wordFlow(update:Update,context:CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    if text == dict['howToAddMeToYourGroup']:
        context.bot.send_message(chat_id=chat_id,
            text=f'Tap on this link and then choose your group.\n\n{addLink}\n\n"Add admins" permission is required.',
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Add to group', url=addLink)]]))

    if text == dict['managementPanel']:
        userid=update.message.from_user.id
        for m in manager:
            if str(m) in str(userid):
                buttons=[[KeyboardButton('查詢管理員')],[KeyboardButton('新增管理員')],[KeyboardButton('刪除管理員')],[KeyboardButton('返回')]]
                #context.bot.send_message(chat_id=chat_id,text="認證完成",reply_markup=ReplyKeyboardMarkup(buttons))
                ReplyKeyboardMarkup(buttons)
                break


    if text == dict['commandsList']:
        context.bot.send_message(chat_id=chat_id,text='undeveloped')
    if text == dict['supportGroup']:
        context.bot.send_message(chat_id=chat_id,text='To join support group, please tap on below buttons',
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Enter group', url=groupLink)]]))
    return WORKFLOW

bot_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start),MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)],
    states={
        START:[CommandHandler('start', start)],
        WORKFLOW: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)],
    },
    fallbacks=[CommandHandler('start', start)])
dispatcher.add_handler(bot_handler)

def run():
    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == '__main__':
    run()