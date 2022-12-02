
import logging
import json
from threading import Timer
from telegram import Update
from telegram.ext import Updater, Filters, CallbackContext,CommandHandler,MessageHandler, InlineQueryHandler, CallbackQueryHandler,ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton 



with open("data.json", 'r', encoding="utf-8") as f:
    data = json.load(f)
token=data['token']
description = data['description']
advertiseText = data['advertiseText']

logging.basicConfig(level=logging.DEBUG)
updater = Updater(token)

#菜單
menu=InlineKeyboardMarkup([
        [InlineKeyboardButton('管理员设置', callback_data='adminMenu')],
        [InlineKeyboardButton('用户设置', callback_data='userMenu')],
        [InlineKeyboardButton('分析当日', callback_data='analyze')],
        [InlineKeyboardButton('联系作者ryan', url='https://t.me/coffeeboy315')]])

adminMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('禁言功能', callback_data='a')],
        [InlineKeyboardButton('提示信息控制 xx秒自动删除掉', callback_data='b')],
        [InlineKeyboardButton('删除指定时间内的重复发言', callback_data='c')],
        [InlineKeyboardButton('设置间隔时间发广告', callback_data='d')],
        [InlineKeyboardButton('设置邀请指定人数后才能发言,几天数为一个周期', callback_data='e')],
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
        
advertiseMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('開啟推送', callback_data='groupOpenAdvertise')],
        [InlineKeyboardButton('關閉推送', callback_data='groupCloseAdvertise')],
        [InlineKeyboardButton('設置廣告內容', callback_data='groupSetAdvertiseText')],
        [InlineKeyboardButton('設置間隔時間(秒)', callback_data='groupSetAdvertiseTime')],
        [InlineKeyboardButton('返回', callback_data='backAdminMenu')]])

silenceMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('群组開啟禁言', callback_data='groupOpenSilence')],
        [InlineKeyboardButton('群组關閉禁言', callback_data='groupCloseSilence')],
        [InlineKeyboardButton('返回', callback_data='backAdminMenu')]])


# auto message
def message_handler(update: Update, context: CallbackContext):
    if update.message.text == '/start' or update.message.text == '/start@CCP1121_BOT':
        context.bot.send_message(chat_id = update.message.chat.id,text='菜單', reply_markup = menu)
    if update.message.text == '/help' or update.message.text == '/help@CCP1121_BOT':
        context.bot.send_message(chat_id = update.message.chat.id, text = description)

# 菜單選擇
def choose(update: Update, context: CallbackContext):
    chatid=update.callback_query.message.chat_id
    current = context.bot.getChat(chatid).permissions

    if update.callback_query.data=='adminMenu':
        update.callback_query.edit_message_text('管理员设置')
        update.callback_query.edit_message_reply_markup(adminMenu)
    if update.callback_query.data=='userMenu':
        update.callback_query.edit_message_text('用户设置')
        update.callback_query.edit_message_reply_markup(userMenu)
    if update.callback_query.data=='analyze':
        update.callback_query.edit_message_text('分析当日')
        update.callback_query.edit_message_reply_markup(analyze)
    if update.callback_query.data=='back':
        update.callback_query.edit_message_reply_markup(menu)
    if update.callback_query.data=='backAdminMenu':
        update.callback_query.edit_message_text('管理员设置')
        update.callback_query.edit_message_reply_markup(adminMenu)
    if update.callback_query.data=='a':
        update.callback_query.edit_message_text('禁言功能')
        update.callback_query.edit_message_reply_markup(silenceMenu)
    if update.callback_query.data=='d':
        update.callback_query.edit_message_text('设置间隔时间发广告')
        update.callback_query.edit_message_reply_markup(advertiseMenu)


    # 開啟廣告推送
    if update.callback_query.data=='groupOpenAdvertise':
        with open("data.json", 'r', encoding="utf-8") as f:
            data = json.load(f)
        advertiseTime = data['advertiseTime']
        if advertiseTime != 0:
            #廣告推播
            context.bot.send_message(chat_id = chatid, text = '開啟廣告推送')
            job_queue = updater.job_queue
            def send_message_job(context: CallbackContext):
                context.bot.send_message(chat_id=chatid,text=advertiseText + str(advertiseTime)+'秒')
            job_queue.run_repeating(send_message_job,interval=advertiseTime,first=0.0)
            job_queue.start()
        else:
            context.bot.send_message(chat_id = chatid, text = '0')

    # 關閉廣告推送
    if update.callback_query.data=='groupCloseAdvertise':
        job_queue = updater.job_queue
        job_queue.stop()
        context.bot.send_message(chat_id =chatid, text = '關閉廣告推送')

    # 設置廣告推送內容
    if update.callback_query.data=='groupSetAdvertiseText':
        ...
    # 設置廣告推送間隔時間(秒)
    if update.callback_query.data=='groupSetAdvertiseTime':

        context.bot.sendChatAction(action = 'typing', chat_id = chatid)
        context.bot.send_message(chat_id = chatid, text = "OK. Send me the new 'time(s)' text. ")
        if update.message=='1':
            context.bot.send_message(chat_id = chatid, text = "2")


        with open("data.json",'r',encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            load_dict['advertiseTime']=20
        with open("data.json",'w',encoding='utf-8') as f:
            json.dump(load_dict, f,ensure_ascii=False)
        
    # 關閉用戶禁言
    if update.callback_query.data=='groupCloseSilence':
        current.can_send_messages = True
        current.can_send_media_messages = True
        current.can_send_other_messages = True
        current.can_send_polls = True
        current.can_add_web_page_previews=True
        current.can_change_info=True
        current.can_invite_users=True
        current.can_pin_messages=True
        context.bot.set_chat_permissions(chat_id = chatid, permissions = current)
        context.bot.send_message(chat_id = chatid, text = "OK. Setting Finish ")

    #開啟用戶禁言
    if update.callback_query.data=='groupOpenSilence':
        current.can_send_messages = False
        current.can_send_media_messages = False
        current.can_send_other_messages = False
        current.can_send_polls = False
        current.can_add_web_page_previews=False
        current.can_change_info=False
        current.can_invite_users=False
        current.can_pin_messages=False
        context.bot.set_chat_permissions(chat_id = chatid, permissions = current)
        context.bot.send_message(chat_id = chatid, text = "OK. Setting Finish ")

def main():
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(choose))
    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == "__main__":
    main()
