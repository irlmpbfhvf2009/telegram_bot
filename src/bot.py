import logging
import json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton ,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, CallbackContext,CommandHandler,MessageHandler,ConversationHandler,CallbackQueryHandler
import configparser

logging.basicConfig(level=logging.DEBUG)
config = configparser.ConfigParser()
config.read('config.ini',encoding="utf-8")
description = config.get('telegram-bot', 'description')
botusername = config.get('telegram-bot', 'botUsername')
password = config.get('telegram-bot', 'password')
manager = json.loads(config.get('telegram-bot', 'manager'))
group =  json.loads(config.get('telegram-bot', 'group'))
useGroup = json.loads(config.get('telegram-bot', 'useGroup'))
addLink = f'http://t.me/{botusername}?startgroup&admin=change_info'
groupLink='https://t.me/+-DZY9TwhnOlhMDc9'
updater = Updater(config.get('telegram-bot', 'token'))
dispatcher = updater.dispatcher
job_queue = updater.job_queue


START,WORKFLOW,ADMINPANEL,GETTHERIGHT,ADMINWORK,STARTCLEARMSG= range(6)


with open("./json/keyBoardButton.json", 'r', encoding="utf-8") as f:
    keyBoardDict = json.load(f)
with open("./json/inlinekeyboardbutton.json", 'r', encoding="utf-8") as f:
    inlinekeyboardDict = json.load(f)

wordFlowKeyboardButton=[[KeyboardButton(keyBoardDict['wordFlow']['howToAddMeToYourGroup']),KeyboardButton(keyBoardDict['wordFlow']['managementPanel'])],
                    [KeyboardButton(keyBoardDict['wordFlow']['commandsList']),KeyboardButton(keyBoardDict['wordFlow']['supportGroup'])],
                    [KeyboardButton(keyBoardDict['wordFlow']['adminUser'])]]
                    

workKeyboardButton=[[KeyboardButton(keyBoardDict['work']['banToAllPost']),KeyboardButton(keyBoardDict['work']['groupMsgClear'])],
                        [KeyboardButton(keyBoardDict['work']['adSettings']),KeyboardButton(keyBoardDict['work']['analysisDay'])],
                        [KeyboardButton(keyBoardDict['work']['homeScreen'])]]

adminUserMenu=InlineKeyboardMarkup([
        [InlineKeyboardButton(inlinekeyboardDict['adminUser']['findAllAdmin'], callback_data=inlinekeyboardDict['adminUser']['cd_findAllAdmin'])],
        [InlineKeyboardButton(inlinekeyboardDict['adminUser']['getTheRight'], callback_data=inlinekeyboardDict['adminUser']['cd_getTheRight'])],
        [InlineKeyboardButton(inlinekeyboardDict['adminUser']['adminExit'], callback_data=inlinekeyboardDict['adminUser']['cd_adminExit'])]])


def selectGroupKeyboardButton():
    dict={}
    dict.update(group)
    button=[]
    for title in dict.values():
        button.append([KeyboardButton(title)])
    button.append([KeyboardButton(keyBoardDict['common']['goBack'])])
    return button


def start(update:Update,context:CallbackContext):
    chat_id = update.effective_chat.id
    userid=update.message.from_user.id
    context.bot.send_message(chat_id=chat_id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(wordFlowKeyboardButton))
    if str(chat_id) == str(userid):
        return WORKFLOW
    #else:
    #    context.bot.send_message(chat_id=chat_id,text="开发中,请联系https://t.me/coffeeboy315")


def wordFlow(update:Update,context:CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    username = update.message.from_user.first_name
    msgId = update.message.message_id

    groupLastMessageId =  json.loads(config.get('telegram-bot', 'groupLastMessageId'))
    dict={}
    dict.update(groupLastMessageId)
    dict.update({str(chat_id):str(msgId)})
    config.set('telegram-bot',"grouplastmessageid",str(json.dumps(dict, ensure_ascii=False)))
    config.write
    with open('config.ini', 'w',encoding="utf-8") as configfile:
        config.write(configfile)
    configfile.close()


    if text == keyBoardDict['wordFlow']['howToAddMeToYourGroup']:
        context.bot.send_message(chat_id=chat_id , text=f'Tap on this link and then choose your group.\n\n{addLink}\n\n"Add admins" permission is required.',
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Add to group', url=addLink)]]))

    if text == keyBoardDict['wordFlow']['managementPanel']:
        userid=update.message.from_user.id
        for m in manager:
            if str(m) == str(userid):
                context.bot.send_message(chat_id=chat_id,text=f"Account {username} uses the administrator function")
                context.bot.send_message(chat_id=chat_id,text=f"Please select a group",reply_markup=ReplyKeyboardMarkup(selectGroupKeyboardButton()))
                return ADMINPANEL
        context.bot.send_message(chat_id=chat_id,text='目前尚无权限,请联系https://t.me/coffeeboy315')
    if text == keyBoardDict['wordFlow']['commandsList']:
        context.bot.send_message(chat_id=chat_id,text='undeveloped')
    if text == keyBoardDict['wordFlow']['supportGroup']:
        context.bot.send_message(chat_id=chat_id,text='To join support group, please tap on below buttons',
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Enter group', url=groupLink)]]))
    if text == keyBoardDict['wordFlow']['adminUser']:
        context.bot.send_message(chat_id = chat_id,text=keyBoardDict['wordFlow']['adminUser'],reply_markup = adminUserMenu)
    return WORKFLOW

def choose(update:Update,context:CallbackContext):
    chat_id=update.effective_chat.id
    if update.callback_query.data==inlinekeyboardDict['adminUser']['cd_findAllAdmin']:
        string=""
        for key,value in manager.items():
            string+=value+'　　'
        context.bot.send_message(chat_id=chat_id,text=string)
        #context.bot.send_message(chat_id=chat_id,text=str[:(len(string)-1)])

    if update.callback_query.data==inlinekeyboardDict['adminUser']['cd_getTheRight']:
        context.bot.send_message(chat_id = chat_id, text = "OK. Send me the 'password' .")
        return GETTHERIGHT

    if update.callback_query.data==inlinekeyboardDict['adminUser']['cd_adminExit']:
        for key,value in manager.items():
            if update.effective_user.first_name == value:
                dictionary={}
                dictionary.update(manager)
                del dictionary[str(update.effective_user.id)]
                config.set('telegram-bot',"manager",str(json.dumps(dictionary, ensure_ascii=False)))
                with open('config.ini', 'w',encoding="utf-8") as configfile:
                    config.write(configfile)
                configfile.close()
        context.bot.send_message(chat_id=update.effective_chat.id,text=str(manager))

def getTheRight(update:Update,context:CallbackContext):
    chat_id=update.effective_chat.id
    dictionary = {}
    dictionary.update(manager)
    text=update.message.text

    for key,value in keyBoardDict['wordFlow'].items():
        if value == text:
            return ConversationHandler.END

    if text == password:
        dictionary.update({str(update.effective_user.id):update.effective_user.first_name})
        config.set('telegram-bot',"manager",str(json.dumps(dictionary, ensure_ascii=False)))
        with open('config.ini', 'w',encoding="utf-8") as configfile:
            config.write(configfile)
        configfile.close()
        context.bot.send_message(chat_id=chat_id,text='输入正确')
        context.bot.send_message(chat_id=chat_id,text=str(list(dictionary.values())))
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=chat_id,text='输入错误')


def adminPanel(update:Update,context:CallbackContext):
    chat_id = update.effective_chat.id
    userid = update.effective_user.id
    text = update.message.text
    groupDict={}
    groupDict.update(useGroup)
    for key,value in group.items():
        if text==value:
            groupDict.update({str(userid):str(key)})
            config.set('telegram-bot',"useGroup",str(json.dumps(groupDict, ensure_ascii=False)))
            with open('config.ini', 'w',encoding="utf-8") as configfile:
                config.write(configfile)
            configfile.close()
            context.bot.send_message(chat_id=chat_id,text=f"chose {text}",reply_markup=ReplyKeyboardMarkup(workKeyboardButton))
            return ADMINWORK

    if text == keyBoardDict['work']['homeScreen']:
        context.bot.send_message(chat_id=chat_id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(wordFlowKeyboardButton))
        return ConversationHandler.END
    return ADMINPANEL

def adminWork(update:Update,context:CallbackContext):
    chat_id=update.effective_chat.id
    userid=update.effective_user.id
    text=update.message.text
    for key,value in useGroup.items():
        if str(key)==str(userid):
            if text == keyBoardDict['work']['banToAllPost']:
                ...
            if text == keyBoardDict['work']['groupMsgClear']:
                context.bot.send_message(chat_id=userid,text="Please tap on CLEAR")
                new_message_id = update.message.message_id
                while new_message_id > 1:
                    try:
                        context.bot.delete_message(chat_id=value, message_id=new_message_id)
                    except Exception as error:
                        print(f'Message_id does not exist: {new_message_id} - {error}')
                        #return ConversationHandler.END
                    new_message_id = new_message_id - 1
                #return STARTCLEARMSG


    if text == keyBoardDict['work']['homeScreen']:
        context.bot.send_message(chat_id=chat_id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(wordFlowKeyboardButton))
        return ConversationHandler.END
    return ADMINWORK

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

def joinGroup(update:Update,context:CallbackContext):
    dictionary = {}
    dictionary.update(group)
    for member in update.message.new_chat_members:
        if member.username == botusername:
            context.bot.send_message(chat_id=5036779522,text=f'加入群组 {update.message.chat.title}({str(update.message.chat.id)})')
            dictionary.update({str(update.message.chat.id):update.message.chat.title})
            config.set('telegram-bot',"group",str(json.dumps(dictionary, ensure_ascii=False)))
            with open('config.ini', 'w',encoding="utf-8") as configfile:
                config.write(configfile)
            configfile.close()

def leftGroup(update:Update,context:CallbackContext):
    dictionary = {}
    dictionary.update(group)
    if update.message.left_chat_member.username == botusername:
        context.bot.send_message(chat_id=5036779522,text=f'退出群组 {update.message.chat.title}({str(update.message.chat.id)})')
        del dictionary[str(update.message.chat.id)]
        config.set('telegram-bot',"group",str(json.dumps(dictionary, ensure_ascii=False)))
        with open('config.ini', 'w',encoding="utf-8") as configfile:
            config.write(configfile)
        configfile.close()


dispatcher.add_handler(
    ConversationHandler(
        entry_points=[CommandHandler('start', start),CallbackQueryHandler(choose),MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)],
        states={
            START:[CommandHandler('start', start)],
            WORKFLOW: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)],
            GETTHERIGHT: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=getTheRight)],
            ADMINPANEL: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=adminPanel)],
            ADMINWORK: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=adminWork)],
            STARTCLEARMSG: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=start_clearmsg)],
        },fallbacks=[CommandHandler('start', start),CallbackQueryHandler(choose),MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)]))


dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, joinGroup))
dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, leftGroup))

def run():
    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == '__main__':
    run()