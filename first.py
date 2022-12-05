
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
f.close()
with open("inlinekeyboardbutton.json", 'r', encoding="utf-8") as f:
    dict = json.load(f)


logging.basicConfig(level=logging.DEBUG)
updater = Updater(token)

#菜單
menu=InlineKeyboardMarkup([
        [InlineKeyboardButton(dict['setAdmin'], callback_data=dict['cd_setAdmin'])],
        [InlineKeyboardButton(dict['setUser'], callback_data=dict['cd_setUser'])],
        [InlineKeyboardButton(dict['analysisDay'], callback_data=dict['cd_analysisDay'])],
        [InlineKeyboardButton(dict['callRyan'], url=dict['callRyan_url'])]])

adminMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton(dict['banToAllPost'], callback_data=dict['cd_bannedToAllPost'])],
        [InlineKeyboardButton('提示信息控制 xx秒自动删除掉', callback_data='b')],
        [InlineKeyboardButton('删除指定时间内的重复发言', callback_data='c')],
        [InlineKeyboardButton('设置间隔时间发广告', callback_data='d')],
        [InlineKeyboardButton('设置邀请指定人数后才能发言,几天数为一个周期', callback_data='e')],
        [InlineKeyboardButton('关注指定频道成员才能发言,没有达标甚至提醒内容', callback_data='f')],
        [InlineKeyboardButton('删除指定时间内的重复发言', callback_data='g')],
        [InlineKeyboardButton(dict['goBack'], callback_data=dict['cd_goBack'])]])

userMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('您@用户：您需要邀请2位好友后可以正常发言', callback_data='h')],
        [InlineKeyboardButton('您@用户：您需要关注频道 @xx 后可以正常发言  （跳转频道删除掉', callback_data='i')],
        [InlineKeyboardButton(dict['goBack'], callback_data=dict['cd_goBack'])]])

analyze=InlineKeyboardMarkup([
        [InlineKeyboardButton('昨天新进成员 流失成员，被邀请成员，活跃度成员', callback_data='k')],
        [InlineKeyboardButton(dict['goBack'], callback_data=dict['cd_goBack'])]])
        
advertiseMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('開啟推送', callback_data='groupOpenAdvertise')],
        [InlineKeyboardButton('關閉推送', callback_data='groupCloseAdvertise')],
        [InlineKeyboardButton('設置廣告內容', callback_data='groupSetAdvertiseText')],
        [InlineKeyboardButton('設置間隔時間(秒)', callback_data='groupSetAdvertiseTime')],
        [InlineKeyboardButton(dict['goAdminMenu'], callback_data=dict['cd_goAdminMenu'])]])

silenceMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('群组開啟禁言', callback_data='groupOpenSilence')],
        [InlineKeyboardButton('群组關閉禁言', callback_data='groupCloseSilence')],
        [InlineKeyboardButton(dict['goAdminMenu'], callback_data=dict['cd_goAdminMenu'])]])



# 菜單選擇
def choose(update: Update, context: CallbackContext):
    chatid=update.callback_query.message.chat_id
    current = context.bot.getChat(chatid).permissions

    if update.callback_query.data==dict['cd_setAdmin']:
        update.callback_query.edit_message_text(dict['setAdmin'])
        update.callback_query.edit_message_reply_markup(adminMenu)
    if update.callback_query.data==dict['cd_setUser']:
        update.callback_query.edit_message_text(dict['setUser'])
        update.callback_query.edit_message_reply_markup(userMenu)
    if update.callback_query.data==dict['cd_analysisDay']:
        update.callback_query.edit_message_text(dict['analysisDay'])
        update.callback_query.edit_message_reply_markup(analyze)
    if update.callback_query.data=='back':
        update.callback_query.edit_message_reply_markup(menu)
    if update.callback_query.data=='backAdminMenu':
        update.callback_query.edit_message_text(dict['setAdmin'])
        update.callback_query.edit_message_reply_markup(adminMenu)
    if update.callback_query.data==dict['cd_bannedToAllPost']:
        update.callback_query.edit_message_text(dict['banToAllPost'])
        update.callback_query.edit_message_reply_markup(silenceMenu)
    if update.callback_query.data=='d':
        update.callback_query.edit_message_text('设置间隔时间发广告')
        update.callback_query.edit_message_reply_markup(advertiseMenu)


    # 開啟廣告推送
    if update.callback_query.data=='groupOpenAdvertise':
        with open("advertise.json", 'r', encoding="utf-8") as f:
            data = json.load(f)
        advertiseTime = data['advertiseTime']
        advertiseText = data['advertiseText']
        f.close()

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
        context.bot.send_message(chat_id = chatid, text = "OK. Send me the new 'time(s)' text.")
        return SET_ADVERTISETIME
        
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

START,FIRST_HANDLER,SET_ADVERTISETIME= range(3)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id = update.message.chat.id,text='菜單', reply_markup = menu)
    return FIRST_HANDLER

def first_handler(update: Update, context: CallbackContext):
    return FIRST_HANDLER

def set_advertisetime(update: Update, context: CallbackContext):
    text=update.message.text
    if text.isdigit() == True:

        with open("advertise.json",'r',encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            load_dict['advertiseTime']=text
        with open("advertise.json",'w',encoding='utf-8') as f:
            json.dump(load_dict, f,ensure_ascii=False)
        load_f.close()
        f.close()

        context.bot.send_message(chat_id = update.message.chat.id, text = f'Ad interval is set to {text} seconds') 
        context.bot.send_message(chat_id = update.message.chat.id,text='设置间隔时间发广告', reply_markup = advertiseMenu)
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id = update.message.chat.id, text = 'Please key in numbers')
        return SET_ADVERTISETIME

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END


def main():
    #updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
    #updater.dispatcher.add_handler(CallbackQueryHandler(choose))
    updater.dispatcher.add_handler( 
        ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                #FIRST_HANDLER: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=first_handler)],
            },fallbacks=[CommandHandler('start', start)],))

    updater.dispatcher.add_handler( 
        ConversationHandler(
            entry_points=[CallbackQueryHandler(choose)],
            states={
                SET_ADVERTISETIME: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=set_advertisetime)],
            },fallbacks=[CallbackQueryHandler(choose)],))

    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == "__main__":
    main()
