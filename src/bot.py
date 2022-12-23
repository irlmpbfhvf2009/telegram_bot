from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton ,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Filters, CallbackContext,CommandHandler,MessageHandler,ConversationHandler,CallbackQueryHandler,ChatMemberHandler,handler
import json
from src import _button
from src import _config
from src import _sql
import logging
import datetime
import time

logging.basicConfig(level=logging.DEBUG,
            format='[%(asctime)s]  %(levelname)s [%(filename)s %(funcName)s] [ line:%(lineno)d ] %(message)s',
            datefmt='%Y-%m-%d %H:%M',
            #handlers=[logging.StreamHandler()])
            handlers=[logging.StreamHandler(),logging.FileHandler(f'log//{time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())}.log', 'w', 'utf-8')])

keyboard = _button.Keyboard()
init = _config.BotConfig()

def runSQL():
    return _sql.DBHP("telegram-bot.db")
# 更新config table botuserName
runSQL().updateConfig(init.updater.bot.username)

# CommandHandler
def start(update:Update,context:CallbackContext):
    sql = runSQL()
    # 限制邀請人數才能發言
    if update.message.chat.type == 'private':
        context.bot.send_message(chat_id=update.effective_chat.id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(keyboard.wordFlowKeyboardButton))
        if str(update.effective_chat.id) == str(update.message.from_user.id):
            return WORKFLOW
    else:
        if sql.getIsManager(update.effective_user.id) == "False" or sql.getManager(update.effective_user.id) is None:
            if sql.getInviteFriendsSet == "True":
                if update.message.from_user.first_name != "Telegram":
                    try:
                        if update.message.reply_to_message.forward_from_chat.type != "channel":
                            if sql.messageLimitToInviteFriends(update.message.from_user.id) == False:
                                len = sql.getDynamicInviteFriendsQuantity(update.message.from_user.id)
                                mention = "["+update.message.from_user.first_name+"](tg://user?id="+str(update.message.from_user.id)+")"
                                context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.message.message_id)
                                context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需要邀请{len}位好友后可以正常发言",parse_mode="Markdown")
                            elif sql.messageLimitToInviteFriends(update.message.from_user.id) == True:
                                try:
                                    if context.bot.get_chat_member(int(sql.getChannelId()[0]),update.effective_user.id).status =="left":
                                        if sql.getFollowChannelSet() == "True":
                                            channelmark = "[@"+sql.channelTitle+"]("+sql.channelLink+")"
                                            mention = "["+update.message.from_user.first_name+"](tg://user?id="+str(update.message.from_user.id)+")"
                                            context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.message.message_id)
                                            context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需关注频道{channelmark}后可以正常发言",parse_mode="Markdown")
                                except Exception as e:
                                    print("機器人尚未加入頻道"+str(e))
                    except:
                        if sql.messageLimitToInviteFriends(update.message.from_user.id) == False:
                            len = sql.getDynamicInviteFriendsQuantity(update.message.from_user.id)
                            mention = "["+update.message.from_user.first_name+"](tg://user?id="+str(update.message.from_user.id)+")"
                            context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.message.message_id)
                            context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需要邀请{len}位好友后可以正常发言",parse_mode="Markdown")
                            try:
                                if context.bot.get_chat_member(int(sql.getChannelId()[0]),update.effective_user.id).status =="left":
                                    if sql.getFollowChannelSet() == "True":
                                        channelmark = "[@"+sql.channelTitle+"]("+sql.channelLink+")"
                                        context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需关注频道{channelmark}后可以正常发言",parse_mode="Markdown")
                            except:
                                print("機器人尚未加入頻道")
                        elif sql.messageLimitToInviteFriends(update.message.from_user.id) == True:
                            try:
                                if context.bot.get_chat_member(int(sql.getChannelId()[0]),update.effective_user.id).status =="left":
                                    if sql.getFollowChannelSet() == "True":
                                        mention = "["+update.message.from_user.first_name+"](tg://user?id="+str(update.message.from_user.id)+")"
                                        channelmark = "[@"+sql.channelTitle+"]("+sql.channelLink+")"
                                        context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.message.message_id)
                                        context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需关注频道{channelmark}后可以正常发言",parse_mode="Markdown")
                            except Exception as e:
                                print("機器人尚未加入頻道"+str(e))

# MessageHandler 第一层msg监听
def wordFlow(update:Update,context:CallbackContext):
    sql = runSQL()

    # 记录群组最后messageId(方便删除用)
    if sql.inviteFriendsAutoClearTime != "0":
        sql.insertLastGroupMessageId(update.message.chat.id,update.message.message_id)
    
    # 自动清除邀请好友记录
    sql.AutoClearinviteFriends()

    first_name = update.message.from_user.first_name
    # 限制邀請人數才能發言
    if update.message.chat.type != 'private':
        if sql.getIsManager(update.effective_user.id) == "False" or sql.getManager(update.effective_user.id) is None:
            if sql.getInviteFriendsSet() == "True":
                if first_name != "Telegram":
                    try:
                        if update.message.reply_to_message.forward_from_chat.type != "channel":
                            if sql.messageLimitToInviteFriends(update.message.from_user.id) == False:
                                len = sql.getDynamicInviteFriendsQuantity(update.message.from_user.id)
                                mention = "["+first_name+"](tg://user?id="+str(update.message.from_user.id)+")"
                                context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.message.message_id)
                                context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需要邀请{len}位好友后可以正常发言",parse_mode="Markdown")
                                try:
                                    if context.bot.get_chat_member(int(sql.getChannelId()[0]),update.effective_user.id).status =="left":
                                        if sql.getFollowChannelSet() == "True":
                                            channelmark = "[@"+sql.channelTitle+"]("+sql.channelLink+")"
                                            context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需关注频道{channelmark}后可以正常发言",parse_mode="Markdown")
                                except:
                                    print("機器人尚未加入頻道")
                            elif sql.messageLimitToInviteFriends(update.message.from_user.id) == True:
                                try:
                                    if context.bot.get_chat_member(int(sql.getChannelId()[0]),update.effective_user.id).status =="left":
                                        if sql.getFollowChannelSet() == "True":
                                            mention = "["+first_name+"](tg://user?id="+str(update.message.from_user.id)+")"
                                            channelmark = "[@"+sql.channelTitle+"]("+sql.channelLink+")"
                                            context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.message.message_id)
                                            context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需关注频道{channelmark}后可以正常发言",parse_mode="Markdown")
                                except Exception as e:
                                    print("機器人尚未加入頻道"+str(e))
                    except:
                        if sql.messageLimitToInviteFriends(update.message.from_user.id) == False:
                            len = sql.getDynamicInviteFriendsQuantity(update.message.from_user.id)
                            mention = "["+first_name+"](tg://user?id="+str(update.message.from_user.id)+")"
                            context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.message.message_id)
                            context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需要邀请{len}位好友后可以正常发言",parse_mode="Markdown")
                            try:
                                if context.bot.get_chat_member(int(sql.getChannelId()[0]),update.effective_user.id).status =="left":
                                    if sql.getFollowChannelSet() == "True":
                                        channelmark = "[@"+sql.channelTitle+"]("+sql.channelLink+")"
                                        context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需关注频道{channelmark}后可以正常发言",parse_mode="Markdown")
                            except Exception as e:
                                print("機器人尚未加入頻道"+str(e))
                        elif sql.messageLimitToInviteFriends(update.message.from_user.id) == True:
                            try:
                                if context.bot.get_chat_member(int(sql.getChannelId()[0]),update.effective_user.id).status =="left":
                                    if sql.getFollowChannelSet() == "True":
                                        mention = "["+first_name+"](tg://user?id="+str(update.message.from_user.id)+")"
                                        channelmark = "[@"+sql.channelTitle+"]("+sql.channelLink+")"
                                        context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.message.message_id)
                                        context.bot.send_message(chat_id=update.effective_chat.id,text=f"{mention}：您需关注频道{channelmark}后可以正常发言",parse_mode="Markdown")
                            except Exception as e:
                                print("機器人尚未加入頻道"+str(e))
    else:
        # 如何将我添加到您的群组
        if update.message.text == keyboard.howToAddMeToYourGroup:
            addGroupLink = f'http://t.me/{sql.botusername}?startgroup&admin=change_info'
            context.bot.send_message(chat_id=update.effective_chat.id , text=f'Tap on this link and then choose your group.\n{addGroupLink}\n\n"Add admins" permission is required.',
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Add to group', url=addGroupLink)]]))

        # 如何将我添加到您的频道
        if update.message.text == keyboard.howToAddMeToYourChannel:
            addChannelLink = f'http://t.me/{sql.botusername}?startchannel&admin=change_info'
            context.bot.send_message(chat_id=update.effective_chat.id , text=f'Tap on this link and then choose your channel.\n{addChannelLink}\n\n"Add admins" permission is required.',
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Add to channel', url=addChannelLink)]]))


        # 管理面板
        if update.message.text == keyboard.managementPanel:
            # 显示所有群组
            def selectGroupKeyboardButton():
                results = sql.getAllJoinGroupIdAndTitle()
                button=[]
                for result in results:
                    button.append([KeyboardButton(result[1]+f" ({result[0]})")])
                button.append(keyboard.keyboardButtonGoBack)
                return button
            if sql.getIsManager(update.message.from_user.id) == 'True':
                context.bot.send_message(chat_id=update.effective_chat.id,text=f"Account {update.message.from_user.first_name} uses the administrator function")
                context.bot.send_message(chat_id=update.effective_chat.id,text=f"Please select a group",reply_markup=ReplyKeyboardMarkup(selectGroupKeyboardButton()))
                return SELECTGROUP
            else:
                context.bot.send_message(chat_id=update.effective_chat.id,text="you don't have permission")

        # 支援团队
        if update.message.text == keyboard.supportGroup:
            groups = sql.getAllJoinGroupIdAndTitle()
            for group in groups:
                groupLink = sql.getJoinGroupLink(group[0])
                context.bot.send_message(chat_id=update.effective_chat.id,text=f'To join {group[1]} group, please tap on below buttons',
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Enter group", url=groupLink[0])]
                ]))

            channels = sql.getAllJoinChannelIdAndTitle()
            for channel in channels:
                channelLink = sql.getJoinChannelLink(channel[0])
                context.bot.send_message(chat_id=update.effective_chat.id,text=f'To join {channel[1]} channel, please tap on below buttons',
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Enter channel", url=channelLink[0])]
                ]))
                
        # 管理员设置
        if update.message.text == keyboard.adminUser:
            context.bot.send_message(chat_id = update.effective_chat.id,text=keyboard.adminUser,reply_markup = keyboard.adminUserMenu)
        # 返回
        if update.message.text == keyboard.goBack:
            context.bot.send_message(chat_id=update.effective_chat.id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(keyboard.wordFlowKeyboardButton))
        # 主画面
        if update.message.text == keyboard.homeScreen:
            context.bot.send_message(chat_id=update.effective_chat.id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(keyboard.wordFlowKeyboardButton))
            return ConversationHandler.END
    return WORKFLOW

# CallbackContext 内连键盘
def choose(update:Update,context:CallbackContext):
    sql = runSQL()
    if update.callback_query.data==keyboard.cd_findAllAdmin:
        results = sql.getAllManager()
        string=""
        for result in results:
            mention = "["+result[1]+"](tg://user?id="+result[0]+")"
            string+=mention+" "
        context.bot.send_message(chat_id=update.effective_chat.id,text=f"目前管理员：{string}",parse_mode="Markdown")
    if update.callback_query.data==keyboard.cd_getTheRight:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "OK. Send me the 'password' .")
        return GETTHERIGHT
    if update.callback_query.data==keyboard.cd_adminExit:
        result = sql.exitManager(update.effective_user.id)
        context.bot.send_message(chat_id=update.effective_chat.id,text=result)

    if sql.getIsManager(update.effective_user.id) == "False":
        context.bot.send_message(chat_id=update.effective_chat.id,text="You are not an administrator Please login")
    else:
        if update.callback_query.data==keyboard.cd_paramSet:
            context.bot.send_message(chat_id = update.effective_chat.id,text=keyboard.paramSet,reply_markup = keyboard.paramSettingMenu)
        if update.callback_query.data == keyboard.cd_passwordCheck:
            context.bot.send_message(chat_id=update.effective_chat.id,text='password : '+sql.password)
        if update.callback_query.data == keyboard.cd_passwordChange:
            context.bot.send_message(chat_id=update.effective_chat.id,text="OK. Send me the new 'password'")
            return CHANGEPASSWORD
        if update.callback_query.data == keyboard.cd_openInviteFriends:
            context.bot.send_message(chat_id=update.effective_chat.id,text="OK. start success")
            sql.openInviteFriends()
        if update.callback_query.data == keyboard.cd_closeInviteFriends:
            context.bot.send_message(chat_id=update.effective_chat.id,text="OK. stop success")
            sql.closeInviteFriends()
        if update.callback_query.data == keyboard.cd_openFollowChannel:
            context.bot.send_message(chat_id=update.effective_chat.id,text="OK. start success")
            sql.openFollowChannel()
        if update.callback_query.data == keyboard.cd_closeFollowChannel:
            context.bot.send_message(chat_id=update.effective_chat.id,text="OK. stop success")
            sql.closeFollowChannel()
        if update.callback_query.data == keyboard.cd_setInviteFriendsQuantity:
            context.bot.send_message(chat_id=update.effective_chat.id,text="OK. Send me the new 'number' of people")
            return SETINVITEFRIENDSQUANTITY
        if update.callback_query.data == keyboard.cd_setInviteFriendsAutoClearTime:
            context.bot.send_message(chat_id=update.effective_chat.id,text="OK. Send me the new 'day'")
            return SETINVITEFRIENDSAUTOCLEARTIME
# 修改密码
def changePassword(update:Update,context:CallbackContext):
    sql = runSQL()
    sql.updatePassword(update.message.text)
    context.bot.send_message(chat_id = update.effective_chat.id, text = f"Set the password to {update.message.text} Success!")
    return ConversationHandler.END
def setInviteFriendsQuantity(update:Update,context:CallbackContext):
    sql = runSQL()
    try:
        if type(int(update.message.text)) == int:
            sql.setInviteFriendsQuantity(update.message.text)
            context.bot.send_message(chat_id = update.effective_chat.id, text = f"Set the number of invitees to {update.message.text} people success!")
            return ConversationHandler.END
    except:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "请重新输入数字")
        return SETINVITEFRIENDSQUANTITY
def setInviteFriendsAutoClearTime(update:Update,context:CallbackContext):
    sql = runSQL()
    try:
        if type(int(update.message.text)) == int:
            sql.setInviteFriendsAutoClearTime(update.message.text)
            context.bot.send_message(chat_id = update.effective_chat.id, text = f"Set {update.message.text} days as a cycle success!")
            return ConversationHandler.END
    except:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "请重新输入数字")
        return SETINVITEFRIENDSAUTOCLEARTIME
# 输入密码验证
def getTheRight(update:Update,context:CallbackContext):
    sql = runSQL()

    for key,value in keyboard.wordFlow.items():
        if value == update.message.text:
            return ConversationHandler.END

    if update.message.text == sql.password:
        result = sql.insertManager(update.effective_user.id,update.effective_user.first_name)
        context.bot.send_message(chat_id=update.effective_chat.id,text=result)
        results = sql.getAllManager()
        string=""
        for result in results:
            mention = "["+result[1]+"](tg://user?id="+result[0]+")"
            string+=mention+" "
        context.bot.send_message(chat_id=update.effective_chat.id,text=f"目前管理员：{string}",parse_mode="Markdown")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text='输入错误，请重新输入')


def selectGroup(update:Update,context:CallbackContext):
    sql=runSQL()
    if update.message.text == keyboard.goBack:
        context.bot.send_message(chat_id=update.effective_chat.id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(keyboard.wordFlowKeyboardButton))
        return ConversationHandler.END
    if update.message.text == keyboard.homeScreen:
        context.bot.send_message(chat_id=update.effective_chat.id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(keyboard.wordFlowKeyboardButton))
        return ConversationHandler.END

    results = sql.getAllJoinGroupIdAndTitle()
    for result in results:
        if update.message.text in result[1] + f" ({result[0]})":
            sql.updateUseGroup(update.message.from_user.id,result[1],result[0])
            context.bot.send_message(chat_id=update.effective_chat.id,text=f"chose {result[1]}",reply_markup=ReplyKeyboardMarkup(keyboard.workKeyboardButton))
            return ADMINWORK
    return SELECTGROUP

# 管理面板 > 功能
def adminWork(update:Update,context:CallbackContext):
    sql=runSQL()
    chat_id = sql.getUseGroupId(update.message.from_user.id)
    lastMsgId = sql.getLastGroupMessageId(chat_id)
    # msg清除
    if update.message.text == keyboard.groupMsgClear:
        def start_clearmsg(context: CallbackContext):
            new_message_id = int(lastMsgId)
            while new_message_id > -1:
                try:
                    context.bot.delete_message(chat_id=chat_id, message_id=new_message_id)
                except Exception as error:
                    print(f'Message_id does not exist: {new_message_id} - {error}')
                    new_message_id = new_message_id - 1
        context.job_queue.run_once(start_clearmsg,1, context='')
    # 用戶設置
    if update.message.text == keyboard.userSet:
        ...
    # 禁言系统
    if update.message.text == keyboard.banToAllPost:
        ...

    # 主画面
    if update.message.text == keyboard.homeScreen:
        context.bot.send_message(chat_id=update.effective_chat.id,text="What con this bot do?\nPlease tap on START",reply_markup=ReplyKeyboardMarkup(keyboard.wordFlowKeyboardButton))
        return ConversationHandler.END
    
    return ADMINWORK


def joinGroup(update:Update,context:CallbackContext):
    sql = runSQL()
    for member in update.message.new_chat_members:
        if member.username == sql.botusername:
            mention = "["+update.message.from_user.first_name+"](tg://user?id="+str(update.message.from_user.id)+")"
            string=f'{mention} 將BOT加入群组 {update.message.chat.title} id:{update.message.chat.id}'
            context.bot.send_message(chat_id=5036779522,text=string,parse_mode="Markdown")

            link = context.bot.export_chat_invite_link(update.effective_chat.id)
            sql.insertJoinGroup(update.message.from_user.id,update.message.from_user.first_name,update.message.chat.id,update.message.chat.title,link)
        else:
            inviteId=str(update.message.from_user.id)
            inviteAccount = update.message.from_user.first_name
            beInvitedId = str(member.id)
            beInvitedAccoun = member.username
            beInvited = json.dumps({beInvitedId:beInvitedAccoun})
            invitationStartDate = datetime.datetime.now()
            invitationDate = sql.inviteFriendsAutoClearTime
            invitationEndDate = invitationStartDate + datetime.timedelta(days=int(invitationDate))
            sql.insertInvitationLimit(update.message.chat.id,update.message.chat.title,inviteId,inviteAccount,beInvited,invitationStartDate,invitationEndDate,invitationDate)

            
def leftGroup(update:Update,context:CallbackContext):
    sql=runSQL()
    if update.message.left_chat_member.username == sql.botusername:
        sql.deleteJoinGroup(update.message.chat.id)
        mention = "["+update.message.from_user.first_name+"](tg://user?id="+str(update.message.from_user.id)+")"
        string=f'{mention} 將BOT移除群组 {update.message.chat.title} id:{update.message.chat.id}'
        context.bot.send_message(chat_id=5036779522,text=string,parse_mode="Markdown")

def channel(update: Update, context: CallbackContext):
    sql = runSQL()
    type = update.my_chat_member.chat.type
    if update.my_chat_member.new_chat_member.user.username == sql.botusername:
        if type == 'channel':
            channelUsername = update.my_chat_member.chat.username
            channelId=update.my_chat_member.chat.id
            channelTitle=update.my_chat_member.chat.title
            userId=update.my_chat_member.from_user.id
            userName=update.my_chat_member.from_user.first_name
            if userName == 'Channel':
                sql.deleteJoinChannel(channelId)
            else:
                link = f'https://t.me/{channelUsername}'
                sql.insertJoinChannel(userId,userName,channelId,channelTitle,link)

START,WORKFLOW,GETTHERIGHT,ADMINWORK,SELECTGROUP,CHANGEPASSWORD,SETINVITEFRIENDSQUANTITY,SETINVITEFRIENDSAUTOCLEARTIME = range(8)

init.dispatcher.add_handler(
    ConversationHandler(
        entry_points=[CommandHandler('start', start),CallbackQueryHandler(choose),MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)],
        states={
            START:[CommandHandler('start', start)],
            WORKFLOW: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)],
            CHANGEPASSWORD: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=changePassword)],
            SETINVITEFRIENDSQUANTITY: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=setInviteFriendsQuantity)],
            SETINVITEFRIENDSAUTOCLEARTIME: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=setInviteFriendsAutoClearTime)],
            SELECTGROUP: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=selectGroup)],
            GETTHERIGHT: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=getTheRight)],
            ADMINWORK: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=adminWork)],
        },fallbacks=[CommandHandler('start', start),CallbackQueryHandler(choose),MessageHandler(filters=Filters.text & (~ Filters.command), callback=wordFlow)]))

init.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, joinGroup))
init.dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, leftGroup))
init.dispatcher.add_handler(ChatMemberHandler(channel, ChatMemberHandler.MY_CHAT_MEMBER))

def run():
    init.updater.start_polling()
    init.updater.idle()
    init.updater.stop()