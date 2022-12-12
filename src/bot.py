import logging
import json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton ,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, CallbackContext,CommandHandler,MessageHandler,ConversationHandler
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


START,WORKFLOW,ADMINPANEL = range(3)


with open("./json/keyBoardButton.json", 'r', encoding="utf-8") as f:
    dict = json.load(f)

startKeyboardButton=[[KeyboardButton(dict['howToAddMeToYourGroup']),KeyboardButton(dict['managementPanel'])],
        [KeyboardButton(dict['commandsList']),KeyboardButton(dict['supportGroup'])]]

wordFlowKeyboardButton=[[KeyboardButton('禁言功能')],[KeyboardButton('频道信息清空')],[KeyboardButton('广告设置')],[KeyboardButton('返回')]]

def start(update:Update,context:CallbackContext):
    chat_id = update.effective_chat.id
    userid=update.message.from_user.id
    context.bot.send_message(chat_id=chat_id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(startKeyboardButton))
    if str(chat_id) == str(userid):
        return WORKFLOW
    #else:
    #    context.bot.send_message(chat_id=chat_id,text="开发中,请联系https://t.me/coffeeboy315")

def wordFlow(update:Update,context:CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    username = update.message.from_user.first_name
    if text == dict['howToAddMeToYourGroup']:
        context.bot.send_message(chat_id=chat_id , text=f'Tap on this link and then choose your group.\n\n{addLink}\n\n"Add admins" permission is required.',
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Add to group', url=addLink)]]))

    if text == dict['managementPanel']:
        userid=update.message.from_user.id
        for m in manager:
            if str(m) == str(userid):
                context.bot.send_message(chat_id=chat_id,text=f"Account {username} uses the administrator function",reply_markup=ReplyKeyboardMarkup(wordFlowKeyboardButton))
                return ADMINPANEL

        context.bot.send_message(chat_id=chat_id,text='目前尚无权限,请联系https://t.me/coffeeboy315')
    if text == dict['commandsList']:
        context.bot.send_message(chat_id=chat_id,text='undeveloped')
    if text == dict['supportGroup']:
        context.bot.send_message(chat_id=chat_id,text='To join support group, please tap on below buttons',
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Enter group', url=groupLink)]]))
    return WORKFLOW

def adminPanel(update:Update,context:CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    if text == '返回':
        context.bot.send_message(chat_id=chat_id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(startKeyboardButton))
        return START
    return ADMINPANEL

bot_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start),MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)],
    states={
        START:[CommandHandler('start', start)],
        WORKFLOW: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)],
        ADMINPANEL: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=adminPanel)],
    },
    fallbacks=[CommandHandler('start', start),MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)])
dispatcher.add_handler(bot_handler)

def run():
    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == '__main__':
    run()