from telegram import InlineKeyboardMarkup, InlineKeyboardButton ,KeyboardButton
import json

class Keyboard:
    def __init__(self):
        with open("./json/keyBoardButton.json", 'r', encoding="utf-8") as f:
            keyBoardDict = json.load(f)
        with open("./json/inlinekeyboardbutton.json", 'r', encoding="utf-8") as f:
            inlinekeyboardDict = json.load(f)
        self.wordFlowKeyboardButton=[
                            [KeyboardButton(keyBoardDict['wordFlow']['howToAddMeToYourGroup']),KeyboardButton(keyBoardDict['wordFlow']['managementPanel'])],
                            [KeyboardButton(keyBoardDict['wordFlow']['howToAddMeToYourChannel']),KeyboardButton(keyBoardDict['wordFlow']['supportGroup'])],
                            [KeyboardButton(keyBoardDict['wordFlow']['adminUser'])]
                        ]
                            

        self.workKeyboardButton=[
                            [KeyboardButton(keyBoardDict['work']['userSet'])],
                            [KeyboardButton(keyBoardDict['work']['banToAllPost']),KeyboardButton(keyBoardDict['work']['groupMsgClear'])],
                            [KeyboardButton(keyBoardDict['work']['adSettings']),KeyboardButton(keyBoardDict['work']['analysisDay'])],
                            [KeyboardButton(keyBoardDict['work']['homeScreen'])]
                        ]
                                
        self.keyboardButtonGoBack = [
                            KeyboardButton(keyBoardDict['common']['goBack'])
                        ]

        self.adminUserMenu=InlineKeyboardMarkup([
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['paramSet'], callback_data=inlinekeyboardDict['adminUser']['cd_paramSet'])],
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['findAllAdmin'], callback_data=inlinekeyboardDict['adminUser']['cd_findAllAdmin'])],
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['getTheRight'], callback_data=inlinekeyboardDict['adminUser']['cd_getTheRight'])],
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['adminExit'], callback_data=inlinekeyboardDict['adminUser']['cd_adminExit'])]
            ])

        self.paramSettingMenu=InlineKeyboardMarkup([
                [InlineKeyboardButton(inlinekeyboardDict['paramSetting']['passwordCheck'], callback_data=inlinekeyboardDict['paramSetting']['cd_passwordCheck'])],
                [InlineKeyboardButton(inlinekeyboardDict['paramSetting']['passwordChange'], callback_data=inlinekeyboardDict['paramSetting']['cd_passwordChange'])],
                [InlineKeyboardButton(inlinekeyboardDict['paramSetting']['openInviteFriends'], callback_data=inlinekeyboardDict['paramSetting']['cd_openInviteFriends'])],
                [InlineKeyboardButton(inlinekeyboardDict['paramSetting']['closeInviteFriends'], callback_data=inlinekeyboardDict['paramSetting']['cd_closeInviteFriends'])],
                [InlineKeyboardButton(inlinekeyboardDict['paramSetting']['setInviteFriendsQuantity'], callback_data=inlinekeyboardDict['paramSetting']['cd_setInviteFriendsQuantity'])],
                [InlineKeyboardButton(inlinekeyboardDict['paramSetting']['setInviteFriendsAutoClearTime'], callback_data=inlinekeyboardDict['paramSetting']['cd_setInviteFriendsAutoClearTime'])],
                [InlineKeyboardButton(inlinekeyboardDict['paramSetting']['openFollowChannel'], callback_data=inlinekeyboardDict['paramSetting']['cd_openFollowChannel'])],
                [InlineKeyboardButton(inlinekeyboardDict['paramSetting']['closeFollowChannel'], callback_data=inlinekeyboardDict['paramSetting']['cd_closeFollowChannel'])]
            ])

        self.wordFlow = keyBoardDict['wordFlow']
        self.howToAddMeToYourGroup = keyBoardDict['wordFlow']['howToAddMeToYourGroup']
        self.howToAddMeToYourChannel = keyBoardDict['wordFlow']['howToAddMeToYourChannel']
        self.managementPanel = keyBoardDict['wordFlow']['managementPanel']
        self.supportGroup = keyBoardDict['wordFlow']['supportGroup']
        self.adminUser = keyBoardDict['wordFlow']['adminUser']
        self.paramSet = keyBoardDict['wordFlow']['paramSet']
        self.homeScreen = keyBoardDict['work']['homeScreen']
        self.banToAllPost = keyBoardDict['work']['banToAllPost']
        self.userSet = keyBoardDict['work']['userSet']
        self.groupMsgClear= keyBoardDict['work']['groupMsgClear']

        self.goBack= keyBoardDict['common']['goBack']

        self.cd_paramSet=inlinekeyboardDict['adminUser']['cd_paramSet']
        self.cd_findAllAdmin=inlinekeyboardDict['adminUser']['cd_findAllAdmin']
        self.cd_getTheRight=inlinekeyboardDict['adminUser']['cd_getTheRight']
        self.cd_adminExit=inlinekeyboardDict['adminUser']['cd_adminExit']
        self.cd_passwordCheck=inlinekeyboardDict['paramSetting']['cd_passwordCheck']
        self.cd_passwordChange=inlinekeyboardDict['paramSetting']['cd_passwordChange']
        self.cd_openInviteFriends=inlinekeyboardDict['paramSetting']['cd_openInviteFriends']
        self.cd_closeInviteFriends=inlinekeyboardDict['paramSetting']['cd_closeInviteFriends']
        self.cd_openFollowChannel=inlinekeyboardDict['paramSetting']['cd_openFollowChannel']
        self.cd_closeFollowChannel=inlinekeyboardDict['paramSetting']['cd_closeFollowChannel']
        self.cd_setInviteFriendsQuantity=inlinekeyboardDict['paramSetting']['cd_setInviteFriendsQuantity']
        self.cd_setInviteFriendsAutoClearTime=inlinekeyboardDict['paramSetting']['cd_setInviteFriendsAutoClearTime']