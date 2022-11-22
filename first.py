import os
import logging

from random import randint

from telegram import Update
from telegram.ext import Updater, Filters, CallbackContext,CommandHandler
from telegram.ext import MessageHandler, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton 

token='5855785269:AAH9bvPpYudd2wSAvMnBTiKakCeoB92_Z_8'
logging.basicConfig(level=logging.DEBUG)
updater = Updater(token)

menu=InlineKeyboardMarkup([
        [InlineKeyboardButton('管理员设置', callback_data='adminMenu')],
        [InlineKeyboardButton('用户设置', callback_data='userMenu')],
        [InlineKeyboardButton('分析当日', callback_data='analyze')],
        [InlineKeyboardButton('联系作者ryan', url='https://t.me/coffeeboy315')]])

adminMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('禁言功能', callback_data='g')],
        [InlineKeyboardButton('提示信息控制 xx秒自动删除掉', callback_data='b')],
        [InlineKeyboardButton('删除指定时间内的重复发言', callback_data='c')],
        [InlineKeyboardButton('设置间隔时间发广告,几天数为一个周期', callback_data='d')],
        [InlineKeyboardButton('设置邀请指定人数后才能发言', callback_data='e')],
        [InlineKeyboardButton('关注指定频道成员才能发言,没有达标甚至提醒内容', callback_data='f')],
        [InlineKeyboardButton('删除指定时间内的重复发言', callback_data='g')],
        [InlineKeyboardButton('返回', callback_data='back')]])

userMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('您@用户：您需要邀请2位好友后可以正常发言', callback_data='h')],
        [InlineKeyboardButton('您@用户：您需要关注频道 @xx 后可以正常发言  （跳转频道删除掉', callback_data='i')],
        [InlineKeyboardButton('返回', callback_data='back')]])

analyze=InlineKeyboardMarkup([
        [InlineKeyboardButton('昨天新进成员 流失成员，被邀请成员，活跃度成员', callback_data='k')],
        [InlineKeyboardButton('返回', callback_data='back')]])

silenceMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('群组開啟禁言', callback_data='groupOpenSilence')],
        [InlineKeyboardButton('群组關閉禁言', callback_data='groupCloseSilence')],
        [InlineKeyboardButton('返回', callback_data='back')]])

# auto message
def message_handler(update: Update, context: CallbackContext):
    #context.bot.send_message(chat_id=update.message.chat.id, text=update.message.text)
    if update.message.text == '/start':
        context.bot.send_message(chat_id = update.message.chat.id, text = "钢弹也是机器人",reply_markup = menu)

def choose(update: Update, context: CallbackContext):

    chatid=update.callback_query.message.chat_id
    current = context.bot.getChat(chatid).permissions

    if update.callback_query.data=='adminMenu':
        update.callback_query.edit_message_reply_markup(adminMenu)
    if update.callback_query.data=='userMenu':
        update.callback_query.edit_message_reply_markup(userMenu)
    if update.callback_query.data=='analyze':
        update.callback_query.edit_message_reply_markup(analyze)
    if update.callback_query.data=='back':
        update.callback_query.edit_message_reply_markup(menu)
    if update.callback_query.data=='g':
        update.callback_query.edit_message_reply_markup(silenceMenu)

    if update.callback_query.data=='groupOpenSilence':
        current.can_send_messages = False
        #current.can_send_media_messages = False
        #current.can_send_other_messages = False
        #current.can_send_polls = False
        context.bot.set_chat_permissions(chat_id = chatid, permissions = current)
    if update.callback_query.data=='groupCloseSilence':
        current.can_send_messages = True
        current.can_send_media_messages = True
        current.can_send_other_messages = True
        current.can_send_polls = True
        context.bot.set_chat_permissions(chat_id = chatid, permissions = current)



def main():
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(choose))
    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == "__main__":
    main()
