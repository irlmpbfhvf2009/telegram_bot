from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton ,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Filters, CallbackContext,CommandHandler,MessageHandler,ConversationHandler,CallbackQueryHandler
import _button
import _config
import json

keyboard = _button.Keyboard()
init = _config.BotConfig('localhost','root','123456','telegramBot',3306)
init.connct_db()
init.create_table("CREATE TABLE if not exists manager (id INT AUTO_INCREMENT PRIMARY KEY,userId VARCHAR(255), userName VARCHAR(255))")


# CommandHandler
def start(update:Update,context:CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(keyboard.wordFlowKeyboardButton))
    if str(update.effective_chat.id) == str(update.message.from_user.id):
        return WORKFLOW
    #else:
    #    context.bot.send_message(chat_id=chat_id,text="开发中,请联系https://t.me/coffeeboy315")


# MessageHandler 第一层msg监听
def wordFlow(update:Update,context:CallbackContext):

    dict={}
    dict.update(json.loads(init.config.get('telegram-bot', 'groupLastMessageId')))
    dict.update({str(update.effective_chat.id):str(update.message.message_id)})
    init.config.set('telegram-bot',"grouplastmessageid",str(json.dumps(dict, ensure_ascii=False)))
    with open('config.ini', 'w',encoding="utf-8") as configfile:
        init.config.write(configfile)
    configfile.close()

    # 如何将我添加到您的群组
    if update.message.text == keyboard.howToAddMeToYourGroup:
        context.bot.send_message(chat_id=update.effective_chat.id , text=f'Tap on this link and then choose your group.\n\n{init.addLink}\n\n"Add admins" permission is required.',
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Add to group', url=init.addLink)]]))

    # 管理面板
    if update.message.text == keyboard.managementPanel:
        # 显示所有群组
        def selectGroupKeyboardButton():
            dict={}
            dict.update(init.group)
            button=[]
            for title in dict.values():
                button.append([KeyboardButton(title)])
            button.append(keyboard.keyboardButtonGoBack)
            return button
        for m in init.manager:
            if str(m) == str(update.message.from_user.id):
                context.bot.send_message(chat_id=update.effective_chat.id,text=f"Account {update.message.from_user.first_name} uses the administrator function")
                context.bot.send_message(chat_id=update.effective_chat.id,text=f"Please select a group",reply_markup=ReplyKeyboardMarkup(selectGroupKeyboardButton()))
                return ADMINPANEL
        context.bot.send_message(chat_id=update.effective_chat.id,text='目前尚无权限,请联系https://t.me/coffeeboy315')


    # 命令列表
    if update.message.text == keyboard.commandsList:
        context.bot.send_message(chat_id=update.effective_chat.id,text='undeveloped')
    
    # 支援团队
    if update.message.text == keyboard.supportGroup:
        context.bot.send_message(chat_id=update.effective_chat.id,text='To join support group, please tap on below buttons',
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Enter group', url=init.groupLink)]]))
    
    # 管理员设置
    if update.message.text == keyboard.adminUser:
        context.bot.send_message(chat_id = update.effective_chat.id,text=keyboard.adminUser,reply_markup = keyboard.adminUserMenu)
    return WORKFLOW

# CallbackContext 内连键盘
def choose(update:Update,context:CallbackContext):
    if update.callback_query.data==keyboard.cd_findAllAdmin:
        string=""
        for key,value in init.manager.items():
            string+=value+'　　'
        context.bot.send_message(chat_id=update.effective_chat.id,text=string)
        #context.bot.send_message(chat_id=chat_id,text=str[:(len(string)-1)])

    if update.callback_query.data==keyboard.cd_getTheRight:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "OK. Send me the 'password' .")
        return GETTHERIGHT

    if update.callback_query.data==keyboard.cd_adminExit:
        for key,value in init.manager.items():
            if update.effective_user.first_name == value:
                dictionary={}
                dictionary.update(init.manager)
                del dictionary[str(update.effective_user.id)]
                init.config.set('telegram-bot',"manager",str(json.dumps(dictionary, ensure_ascii=False)))
                with open('config.ini', 'w',encoding="utf-8") as configfile:
                    init.config.write(configfile)
                configfile.close()
        context.bot.send_message(chat_id=update.effective_chat.id,text=str(init.manager))

# 输入密码验证
def getTheRight(update:Update,context:CallbackContext):
    dictionary = {}
    dictionary.update(init.manager)

    for key,value in keyboard.wordFlow.items():
        if value == update.message.text:
            return ConversationHandler.END

    if update.message.text == init.password:
        dictionary.update({str(update.effective_user.id):update.effective_user.first_name})
        init.config.set('telegram-bot',"manager",str(json.dumps(dictionary, ensure_ascii=False)))
        with open('config.ini', 'w',encoding="utf-8") as configfile:
            init.config.write(configfile)
        configfile.close()
        context.bot.send_message(chat_id=update.effective_chat.id,text='输入正确')
        context.bot.send_message(chat_id=update.effective_chat.id,text=str(list(dictionary.values())))
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text='输入错误')



def adminPanel(update:Update,context:CallbackContext):
    groupDict={}
    groupDict.update(init.useGroup)
    for key,value in init.group.items():
        if update.message.text==value:
            groupDict.update({str( update.effective_user.id):str(key)})
            init.config.set('telegram-bot',"useGroup",str(json.dumps(groupDict, ensure_ascii=False)))
            with open('config.ini', 'w',encoding="utf-8") as configfile:
                init.config.write(configfile)
            configfile.close()
            context.bot.send_message(chat_id=update.effective_chat.id,text=f"chose {update.message.text}",reply_markup=ReplyKeyboardMarkup(keyboard.workKeyboardButton))
            return ADMINWORK

    if update.message.text == keyboard.homeScreen:
        context.bot.send_message(chat_id=update.effective_chat.id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(keyboard.wordFlowKeyboardButton))
        return ConversationHandler.END
    if update.message.text == keyboard.goBack:
        context.bot.send_message(chat_id=update.effective_chat.id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(keyboard.wordFlowKeyboardButton))
        return ConversationHandler.END
    return ADMINPANEL

# 管理面板 > 功能
def adminWork(update:Update,context:CallbackContext):
    ug = json.loads(init.config.get('telegram-bot', 'useGroup'))
    dict={}
    dict.update(ug)
    for key,value in init.useGroup.items():
        if str(key)==str(update.effective_user.id):
            # 禁言系统
            if update.message.text == keyboard.banToAllPost:
                ...

            # msg清除
            if update.message.text == keyboard.groupMsgClear:
                def start_clearmsg(context: CallbackContext):
                    grouplastmessageid = json.loads(init.config.get('telegram-bot', 'grouplastmessageid'))
                    for k,v in grouplastmessageid.items():
                        if str(k) == str(dict[str(update.effective_user.id)]):
                            new_message_id = int(v)
                            while new_message_id > 1:
                                try:
                                    context.bot.delete_message(chat_id=value, message_id=new_message_id)
                                except Exception as error:
                                    ...
                                    print(f'Message_id does not exist: {new_message_id} - {error}')
                                new_message_id = new_message_id - 1
                context.job_queue.run_once(start_clearmsg,2, context=value)

    # 主画面
    if update.message.text == keyboard.homeScreen:
        context.bot.send_message(chat_id=update.effective_chat.id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(keyboard.wordFlowKeyboardButton))
        return ConversationHandler.END
    return ADMINWORK



def joinGroup(update:Update,context:CallbackContext):
    dictionary = {}
    dictionary.update(init.group)
    for member in update.message.new_chat_members:
        if member.username == init.botusername:
            context.bot.send_message(chat_id=5036779522,text=f'加入群组 {update.message.chat.title}({str(update.message.chat.id)})')
            dictionary.update({str(update.message.chat.id):update.message.chat.title})
            init.config.set('telegram-bot',"group",str(json.dumps(dictionary, ensure_ascii=False)))
            with open('config.ini', 'w',encoding="utf-8") as configfile:
                init.config.write(configfile)
            configfile.close()
        else:
            #邀請人ID
            inviteId=str(update.message.from_user.id)
            #邀請人帳號
            inviteAccount =update.message.from_user.first_name
            #被邀請人ID
            beInvitedId = str(member.id)
            #被邀請人帳號
            beInvitedAccoun = member.username

            
def leftGroup(update:Update,context:CallbackContext):
    dictionary = {}
    dictionary.update(init.group)
    if update.message.left_chat_member.username == init.botusername:
        context.bot.send_message(chat_id=5036779522,text=f'退出群组 {update.message.chat.title}({str(update.message.chat.id)})')
        del dictionary[str(update.message.chat.id)]
        init.config.set('telegram-bot',"group",str(json.dumps(dictionary, ensure_ascii=False)))
        with open('config.ini', 'w',encoding="utf-8") as configfile:
            init.config.write(configfile)
        configfile.close()


START,WORKFLOW,ADMINPANEL,GETTHERIGHT,ADMINWORK= range(5)

init.dispatcher.add_handler(
    ConversationHandler(
        entry_points=[CommandHandler('start', start),CallbackQueryHandler(choose),MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)],
        states={
            START:[CommandHandler('start', start)],
            WORKFLOW: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)],
            GETTHERIGHT: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=getTheRight)],
            ADMINPANEL: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=adminPanel)],
            ADMINWORK: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=adminWork)],
        },fallbacks=[CommandHandler('start', start),CallbackQueryHandler(choose),MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)]))

init.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, joinGroup))
init.dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, leftGroup))

def run():
    init.updater.start_polling()
    init.updater.idle()
    init.updater.stop()

if __name__ == '__main__':
    run()