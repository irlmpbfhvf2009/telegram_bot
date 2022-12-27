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
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['findAllAdmin'], callback_data=inlinekeyboardDict['adminUser']['cd_findAllAdmin'])],
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['passwordCheck'], callback_data=inlinekeyboardDict['adminUser']['cd_passwordCheck'])],
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['passwordChange'], callback_data=inlinekeyboardDict['adminUser']['cd_passwordChange'])],
                [InlineKeyboardButton(inlinekeyboardDict['adminUser']['adminExit'], callback_data=inlinekeyboardDict['adminUser']['cd_adminExit'])]
            ])

        self.inviteFriendsMenu=InlineKeyboardMarkup([
                [InlineKeyboardButton(inlinekeyboardDict['inviteFriends']['openInviteFriends'], callback_data=inlinekeyboardDict['inviteFriends']['cd_openInviteFriends'])],
                [InlineKeyboardButton(inlinekeyboardDict['inviteFriends']['closeInviteFriends'], callback_data=inlinekeyboardDict['inviteFriends']['cd_closeInviteFriends'])],
                [InlineKeyboardButton(inlinekeyboardDict['inviteFriends']['setInviteFriendsQuantity'], callback_data=inlinekeyboardDict['inviteFriends']['cd_setInviteFriendsQuantity'])],
                [InlineKeyboardButton(inlinekeyboardDict['inviteFriends']['deleteMsgForSecond'], callback_data=inlinekeyboardDict['inviteFriends']['cd_deleteMsgForSecond'])],
                [InlineKeyboardButton(inlinekeyboardDict['inviteFriends']['setInviteFriendsAutoClearTime'], callback_data=inlinekeyboardDict['inviteFriends']['cd_setInviteFriendsAutoClearTime'])]
            ])
        self.followChannelMenu=InlineKeyboardMarkup([
                [InlineKeyboardButton(inlinekeyboardDict['followChannel']['openFollowChannel'], callback_data=inlinekeyboardDict['followChannel']['cd_openFollowChannel'])],
                [InlineKeyboardButton(inlinekeyboardDict['followChannel']['closeFollowChannel'], callback_data=inlinekeyboardDict['followChannel']['cd_closeFollowChannel'])],
                [InlineKeyboardButton(inlinekeyboardDict['followChannel']['deleteMsgForSecond'], callback_data=inlinekeyboardDict['followChannel']['cd_deleteMsgForSecond'])]
            ])

        self.InvitationStatisticsSettlementBonusMenu=InlineKeyboardMarkup([
                [InlineKeyboardButton(inlinekeyboardDict['InvitationStatisticsSettlementBonus']['openInvitationBonusSet'], callback_data=inlinekeyboardDict['InvitationStatisticsSettlementBonus']['cd_openInvitationBonusSet'])],
                [InlineKeyboardButton(inlinekeyboardDict['InvitationStatisticsSettlementBonus']['closeInvitationBonusSet'], callback_data=inlinekeyboardDict['InvitationStatisticsSettlementBonus']['cd_closeInvitationBonusSet'])],
                [InlineKeyboardButton(inlinekeyboardDict['InvitationStatisticsSettlementBonus']['setInviteMembers'], callback_data=inlinekeyboardDict['InvitationStatisticsSettlementBonus']['cd_setInviteMembers'])],
                [InlineKeyboardButton(inlinekeyboardDict['InvitationStatisticsSettlementBonus']['setInviteEarnedOutstand'], callback_data=inlinekeyboardDict['InvitationStatisticsSettlementBonus']['cd_setInviteEarnedOutstand'])],
                [InlineKeyboardButton(inlinekeyboardDict['InvitationStatisticsSettlementBonus']['setInviteSettlementBonus'], callback_data=inlinekeyboardDict['InvitationStatisticsSettlementBonus']['cd_setInviteSettlementBonus'])]
            ])

        # wordFlow
        self.wordFlow = keyBoardDict['wordFlow']
        self.howToAddMeToYourGroup = keyBoardDict['wordFlow']['howToAddMeToYourGroup']
        self.howToAddMeToYourChannel = keyBoardDict['wordFlow']['howToAddMeToYourChannel']
        self.managementPanel = keyBoardDict['wordFlow']['managementPanel']
        self.supportGroup = keyBoardDict['wordFlow']['supportGroup']
        self.adminUser = keyBoardDict['wordFlow']['adminUser']
        self.paramSet = keyBoardDict['wordFlow']['paramSet']
        self.inviteFriendsSet = keyBoardDict['wordFlow']['inviteFriendsSet']
        self.followChannelSet = keyBoardDict['wordFlow']['followChannelSet']
        self.InvitationStatisticsSettlementBonus= keyBoardDict['wordFlow']['InvitationStatisticsSettlementBonus']
        self.homeScreen = keyBoardDict['work']['homeScreen']
        self.banToAllPost = keyBoardDict['work']['banToAllPost']
        self.userSet = keyBoardDict['work']['userSet']
        self.groupMsgClear= keyBoardDict['work']['groupMsgClear']

        # adminUser
        self.cd_findAllAdmin=inlinekeyboardDict['adminUser']['cd_findAllAdmin']
        self.cd_adminExit=inlinekeyboardDict['adminUser']['cd_adminExit']
        self.cd_passwordCheck=inlinekeyboardDict['adminUser']['cd_passwordCheck']
        self.cd_passwordChange=inlinekeyboardDict['adminUser']['cd_passwordChange']

        # inviteFriends
        self.cd_openInviteFriends=inlinekeyboardDict['inviteFriends']['cd_openInviteFriends']
        self.cd_closeInviteFriends=inlinekeyboardDict['inviteFriends']['cd_closeInviteFriends']
        self.cd_setInviteFriendsQuantity=inlinekeyboardDict['inviteFriends']['cd_setInviteFriendsQuantity']
        self.cd_setInviteFriendsAutoClearTime=inlinekeyboardDict['inviteFriends']['cd_setInviteFriendsAutoClearTime']
        
        # followChannel
        self.cd_openFollowChannel=inlinekeyboardDict['followChannel']['cd_openFollowChannel']
        self.cd_closeFollowChannel=inlinekeyboardDict['followChannel']['cd_closeFollowChannel']
        self.cd_deleteMsgForSecond=inlinekeyboardDict['followChannel']['cd_deleteMsgForSecond']

        # invitationBonus
        self.cd_openInvitationBonusSet=inlinekeyboardDict['InvitationStatisticsSettlementBonus']['cd_openInvitationBonusSet']
        self.cd_closeInvitationBonusSet=inlinekeyboardDict['InvitationStatisticsSettlementBonus']['cd_closeInvitationBonusSet']
        self.cd_setInviteMembers=inlinekeyboardDict['InvitationStatisticsSettlementBonus']['cd_setInviteMembers']
        self.cd_setInviteEarnedOutstand=inlinekeyboardDict['InvitationStatisticsSettlementBonus']['cd_setInviteEarnedOutstand']
        self.cd_setInviteSettlementBonus=inlinekeyboardDict['InvitationStatisticsSettlementBonus']['cd_setInviteSettlementBonus']


        # common
        self.goBack= keyBoardDict['common']['goBack']