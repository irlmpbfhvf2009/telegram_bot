
import logging
import json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton ,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, CallbackContext,CommandHandler,MessageHandler, CallbackQueryHandler,ConversationHandler
import configparser

config = configparser.ConfigParser()
config.read('config.ini',encoding="utf-8")
token = config.get('telegram', 'token')
description = config.get('telegram', 'description')

with open("json/inlinekeyboardbutton.json", 'r', encoding="utf-8") as f:
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
        [InlineKeyboardButton(dict['channelMsgControl'], callback_data=dict['cd_channelMsgControl'])],
        [InlineKeyboardButton('删除指定时间内的重复发言', callback_data='c')],
        [InlineKeyboardButton(dict['adSettings'], callback_data=dict['cd_adSettings'])],
        [InlineKeyboardButton('设置邀请指定人数后才能发言,几天数为一个周期', callback_data='e')],
        [InlineKeyboardButton('关注指定频道成员才能发言,没有达标甚至提醒内容', callback_data='f')],
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
        [InlineKeyboardButton('設置廣告內容', callback_data='groupSetAdvertiseContent')],
        [InlineKeyboardButton('設置間隔時間(秒)', callback_data='groupSetAdvertiseTime')],
        [InlineKeyboardButton('查看目前設定', callback_data='viewadsetting')],
        [InlineKeyboardButton(dict['goAdminMenu'], callback_data=dict['cd_goAdminMenu'])]])

silenceMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('群组開啟禁言', callback_data='groupOpenSilence')],
        [InlineKeyboardButton('群组關閉禁言', callback_data='groupCloseSilence')],
        [InlineKeyboardButton(dict['goAdminMenu'], callback_data=dict['cd_goAdminMenu'])]])

channelMsgControlMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton('开始群组消息清空', callback_data='startClearMsg')],
        [InlineKeyboardButton('停止清空', callback_data='stopClearMsg')],
        [InlineKeyboardButton('设置秒数', callback_data='setClearTimes')],
        [InlineKeyboardButton('删除指定用户消息', callback_data='delUserMsg')],
        [InlineKeyboardButton(dict['goAdminMenu'], callback_data=dict['cd_goAdminMenu'])]])
# 菜單選擇
def choose(update: Update, context: CallbackContext):

    chatid=update.callback_query.message.chat_id
    current = context.bot.getChat(chatid).permissions
    ucq=update.callback_query
    bot=context.bot
    
    if ucq.data==dict['cd_setAdmin']:
        ucq.edit_message_text(dict['setAdmin'])
        ucq.edit_message_reply_markup(adminMenu)
    if ucq.data==dict['cd_setUser']:
        ucq.edit_message_text(dict['setUser'])
        ucq.edit_message_reply_markup(userMenu)
    if ucq.data==dict['cd_analysisDay']:
        ucq.edit_message_text(dict['analysisDay'])
        ucq.edit_message_reply_markup(analyze)
    if ucq.data==dict['cd_goBack']:
        ucq.edit_message_text(dict['menu'])
        ucq.edit_message_reply_markup(menu)
    if ucq.data==dict['cd_goAdminMenu']:
        ucq.edit_message_text(dict['setAdmin'])
        ucq.edit_message_reply_markup(adminMenu)
    if ucq.data==dict['cd_bannedToAllPost']:
        ucq.edit_message_text(dict['banToAllPost'])
        ucq.edit_message_reply_markup(silenceMenu)

    # 清空频道MSG
    if ucq.data==dict['cd_channelMsgControl']:
        ucq.edit_message_text(dict['channelMsgControl'])
        ucq.edit_message_reply_markup(channelMsgControlMenu)
    # 开始清空
    if ucq.data=='startClearMsg':
        return STARTCLEARMSG

    # 广告设置
    if ucq.data==dict['cd_adSettings']:
        ucq.edit_message_text(dict['adSettings'])
        ucq.edit_message_reply_markup(advertiseMenu)
    # 查看目前广告设置
    if ucq.data=='viewadsetting':
        with open("json/advertise.json",'r',encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            text=load_dict['advertiseText']
            time=load_dict['advertiseTime']
        with open("json/advertise.json",'w',encoding='utf-8') as f:
            json.dump(load_dict, f,ensure_ascii=False)
        load_f.close()
        f.close()
        bot.send_message(chat_id = chatid, text = f"間隔時間{time}s \n內容:{text}")
        ucq.edit_message_reply_markup(advertiseMenu)


    # 開啟廣告推送
    if ucq.data=='groupOpenAdvertise':
        with open("json/advertise.json", 'r', encoding="utf-8") as f:
            data = json.load(f)
        advertiseTime = data['advertiseTime']
        advertiseText = data['advertiseText']
        f.close()
        if advertiseTime != 0:
            #廣告推播
            bot.send_message(chat_id = chatid, text = '開啟廣告推送')
            job_queue = updater.job_queue
            def send_message_job():
                bot.send_message(chat_id=chatid,text=advertiseText)
            job_queue.run_repeating(send_message_job,interval=int(advertiseTime),first=0.0)
            job_queue.start()
        else:
            context.bot.send_message(chat_id = chatid, text = '0')
    # 關閉廣告推送
    if ucq.data=='groupCloseAdvertise':
        job_queue = updater.job_queue
        job_queue.stop()
        bot.send_message(chat_id =chatid, text = '關閉廣告推送')

    # 設置廣告推送內容
    if ucq.data=='groupSetAdvertiseContent':
        bot.send_message(chat_id = chatid, text = "OK. Send me the new 'content'.")
        return SET_ADVERTISETEXT

    # 設置廣告推送間隔時間(秒)
    if ucq.data=='groupSetAdvertiseTime':
        bot.send_message(chat_id = chatid, text = "OK. Send me the new 'time(s)'.")
        return SET_ADVERTISETIME
        
    # 關閉用戶禁言
    if ucq.data=='groupCloseSilence':
        current.can_send_messages = True
        current.can_send_media_messages = True
        current.can_send_other_messages = True
        current.can_send_polls = True
        current.can_add_web_page_previews=True
        current.can_change_info=True
        current.can_invite_users=True
        current.can_pin_messages=True
        bot.set_chat_permissions(chat_id = chatid, permissions = current)
        bot.send_message(chat_id = chatid, text = "OK. Setting Finish ")

    #開啟用戶禁言
    if ucq.data=='groupOpenSilence':
        current.can_send_messages = False
        current.can_send_media_messages = False
        current.can_send_other_messages = False
        current.can_send_polls = False
        current.can_add_web_page_previews=False
        current.can_change_info=False
        current.can_invite_users=False
        current.can_pin_messages=False
        bot.set_chat_permissions(chat_id = chatid, permissions = current)
        bot.send_message(chat_id = chatid, text = "OK. Setting Finish ")

START,FIRST_HANDLER,SET_ADVERTISETIME,SET_ADVERTISETEXT,STARTCLEARMSG= range(5)

# 开始
#def start(update: Update, context: CallbackContext):
#    chat_id = update.message.chat.id
#    bot=context.bot
#    bot.send_message(chat_id = chat_id,text='菜單', reply_markup = menu)
#    return FIRST_HANDLER

# 还没使用
def first_handler(update: Update, context: CallbackContext):
    return FIRST_HANDLER

# 清理MSG
def start_clearmsg(update: Update, context: CallbackContext):
    new_message_id = update.message.message_id
    while new_message_id > 1:
        try:
            context.bot.delete_message(chat_id=update.message.chat.id, message_id=new_message_id)
        except Exception as error:
            print(f'Message_id does not exist: {new_message_id} - {error}')
            return ConversationHandler.END
        new_message_id = new_message_id - 1
    return STARTCLEARMSG

# 设置广告发送时间
def set_advertisetime(update: Update, context: CallbackContext):
    text=update.message.text
    chat_id = update.message.chat.id
    bot=context.bot
    if text.isdigit() == True:

        with open("json/advertise.json",'r',encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            load_dict['advertiseTime']=text
        with open("json/advertise.json",'w',encoding='utf-8') as f:
            json.dump(load_dict, f,ensure_ascii=False)
        load_f.close()
        f.close()

        bot.send_message(chat_id = chat_id, text = f'Ad interval is set to {text} seconds') 
        bot.send_message(chat_id = chat_id, text = dict['adSettings'], reply_markup = advertiseMenu)
        return ConversationHandler.END
    else:
        bot.send_message(chat_id = chat_id, text = 'Please key in numbers')
        return SET_ADVERTISETIME

# 设置广告内容
def set_advertisetext(update: Update, context: CallbackContext):
    chat_id=update.message.chat.id
    text=update.message.text
    bot=context.bot

    with open("json/advertise.json",'r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        load_dict['advertiseText']=text
    with open("json/advertise.json",'w',encoding='utf-8') as f:
        json.dump(load_dict, f,ensure_ascii=False)
    load_f.close()
    f.close()

    if text:
        bot.send_message(chat_id = chat_id, text = f'Ad Text is set to {text}') 
        bot.send_message(chat_id = chat_id, text = dict['adSettings'], reply_markup = advertiseMenu)
        return ConversationHandler.END
    return SET_ADVERTISETEXT
AAA=range(1)
def startCommand(update:Update,context:CallbackContext):
    buttons=[[KeyboardButton('11'),KeyboardButton('33')],[KeyboardButton('22')]]
    context.bot.send_message(chat_id=update.effective_chat.id,reply_markup=ReplyKeyboardMarkup(buttons))
    return AAA

def main():
    dispatcher=updater.dispatcher
    dispatcher.add_handler( 
        ConversationHandler(
            entry_points=[CommandHandler('start', startCommand)],
            states={
                AAA:[MessageHandler(filters=Filters.text & (~ Filters.command), callback=startCommand)],
            },fallbacks=[CommandHandler('start', startCommand)],))
    #dispatcher.add_handler(CommandHandler("start",startCommand))
    dispatcher.add_handler( 
        ConversationHandler(
            entry_points=[CallbackQueryHandler(choose)],
            states={
                SET_ADVERTISETIME: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=set_advertisetime)],
                SET_ADVERTISETEXT: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=set_advertisetext)],
                STARTCLEARMSG: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=start_clearmsg)],
            },fallbacks=[CallbackQueryHandler(choose)],))

    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == "__main__":
    main()
