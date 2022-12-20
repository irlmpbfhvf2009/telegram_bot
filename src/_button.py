from telegram import InlineKeyboardMarkup, InlineKeyboardButton ,KeyboardButton
import json

class Keyboard:
    def __init__(self):
        with open("./json/keyBoardButton.json", 'r', encoding="utf-8") as f:
            keyBoardDict = json.load(f)
        with open("./json/inlinekeyboardbutton.json", 'r', encoding="utf-8") as f:
            inlinekeyboardDict = json.load(f)

        self.wordFlowKeyboardButton=[[KeyboardButton(keyBoardDict['wordFlow']['howToAddMeToYourGroup']),KeyboardButton(keyBoardDict['wordFlow']['managementPanel'])],
                            [KeyboardButton(keyBoardDict['wordFlow']['commandsList']),KeyboardButton(keyBoardDict['wordFlow']['supportGroup'])],
                            [KeyboardButton(keyBoardDict['wordFlow']['adminUser'])]]
                            

        self.workKeyboardButton=[
                            [KeyboardButton(keyBoardDict['work']['userSet'])],
                            [KeyboardButton(keyBoardDict['work']['banToAllPost']),KeyboardButton(keyBoardDict['work']['groupMsgClear'])],
                            [KeyboardButton(keyBoardDict['work']['adSettings']),KeyboardButton(keyBoardDict['work']['analysisDay'])],
                            [KeyboardButton(keyBoardDict['work']['homeScreen'])]
                        ]
                                
        self.keyboardButtonGoBack = [KeyboardButton(keyBoardDict['common']['goBack'])]

        self.adminUserMenu=InlineKeyboardMarkup([
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['findAllAdmin'], callback_data=inlinekeyboardDict['adminUser']['cd_findAllAdmin'])],
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['getTheRight'], callback_data=inlinekeyboardDict['adminUser']['cd_getTheRight'])],
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['adminExit'], callback_data=inlinekeyboardDict['adminUser']['cd_adminExit'])]])


        self.wordFlow = keyBoardDict['wordFlow']
        self.howToAddMeToYourGroup = keyBoardDict['wordFlow']['howToAddMeToYourGroup']
        self.managementPanel = keyBoardDict['wordFlow']['managementPanel']
        self.commandsList = keyBoardDict['wordFlow']['commandsList']
        self.supportGroup = keyBoardDict['wordFlow']['supportGroup']
        self.adminUser = keyBoardDict['wordFlow']['adminUser']
        self.homeScreen = keyBoardDict['work']['homeScreen']
        self.banToAllPost = keyBoardDict['work']['banToAllPost']
        self.userSet = keyBoardDict['work']['userSet']
        self.groupMsgClear= keyBoardDict['work']['groupMsgClear']

        self.goBack= keyBoardDict['common']['goBack']

        self.cd_findAllAdmin=inlinekeyboardDict['adminUser']['cd_findAllAdmin']
        self.cd_getTheRight=inlinekeyboardDict['adminUser']['cd_getTheRight']
        self.cd_adminExit=inlinekeyboardDict['adminUser']['cd_adminExit']