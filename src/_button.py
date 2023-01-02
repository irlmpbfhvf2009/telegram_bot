from telegram import InlineKeyboardMarkup, InlineKeyboardButton ,KeyboardButton
import json

class Keyboard:
    def __init__(self):
        # wordFlow
        self.wordFlowKeyboardButton=[
                            [KeyboardButton("如何将我添加到您的群组"),KeyboardButton("管理面板")],
                            [KeyboardButton("如何将我添加到您的频道"),KeyboardButton("支援团队列表")],
                            [KeyboardButton("管理员设置")]
                        ]
        self.wordFlow = {
                            "howToAddMeToYourGroup":"如何将我添加到您的群组",
                            "howToAddMeToYourChannel":"如何将我添加到您的频道",
                            "managementPanel":"管理面板",
                            "supportGroup":"支援团队列表",
                            "adminUser":"管理员设置",
                            "paramSet":"参数设定",
                            "inviteFriendsSet":"邀请好友发言权",
                            "followChannelSet":"关注频道发言权"
                            }

        self.howToAddMeToYourGroup = "如何将我添加到您的群组"
        self.howToAddMeToYourChannel = "如何将我添加到您的频道"
        self.managementPanel = "管理面板"
        self.supportGroup = "支援团队列表"
        self.adminUser = "管理员设置"
        self.paramSet = "参数设定"
        self.inviteFriendsSet = "邀请好友发言权"
        self.followChannelSet = "关注频道发言权"

        # work
        self.workKeyboardButton=[
                            [KeyboardButton("邀请统计结算奖金")],
                            [KeyboardButton("用戶设置(未开发)"),KeyboardButton("禁言功能(未开放)"),KeyboardButton("分析当日(未开发)")],
                            [KeyboardButton("群组信息清空(未开放)"),KeyboardButton("广告设置(未开放)")],
                            [KeyboardButton("主画面")]
                        ]
        self.homeScreen = "主画面"
        self.userSet = "用戶设置(未开发)"
        self.banToAllPost = "禁言功能(未开放)"
        self.groupMsgClear= "群组信息清空(未开放)"
        self.adSettings= "广告设置(未开放)"
        self.analysisDay= "分析当日(未开发)"
        self.InvitationStatisticsSettlementBonus= "邀请统计结算奖金"


        # common
        self.keyboardButtonGoBack = [KeyboardButton("返回")]
        self.goBack= "返回"


        # adminUser
        self.adminUserMenu=InlineKeyboardMarkup([
                [InlineKeyboardButton("查看所有管理员", callback_data="cd_findAllAdmin")],
                [InlineKeyboardButton("查看密码", callback_data="cd_passwordCheck")],
                [InlineKeyboardButton("修改密码", callback_data="cd_passwordChange")],
                [InlineKeyboardButton("登出管理员", callback_data="cd_exit")]
            ])
        
        self.cd_findAllAdmin="cd_findAllAdmin"
        self.cd_passwordCheck="cd_passwordCheck",
        self.cd_passwordChange="cd_passwordChange"
        self.cd_adminExit="cd_exit"


        # inviteFriends and followChannel
        self.inviteFriendsMenu=InlineKeyboardMarkup([
                [InlineKeyboardButton("开启 [邀请好友限制发言]", callback_data="cd_openInviteFriends")],
                [InlineKeyboardButton("关闭 [邀请好友限制发言]", callback_data="cd_closeInviteFriends")],
                [InlineKeyboardButton("开启 [关注频道限制发言]", callback_data="cd_openFollowChannel")],
                [InlineKeyboardButton("关闭 [关注频道限制发言]", callback_data="cd_closeFollowChannel")],
                [InlineKeyboardButton("设定 [邀请指定人数]", callback_data="cd_setInviteFriendsQuantity")],
                [InlineKeyboardButton("设定 [未达标自动删除系统消息(秒)]", callback_data="cd_deleteMsgForSecond")],
                [InlineKeyboardButton("设定 [几天数为一个周期(0为不重置)]", callback_data="cd_setInviteFriendsAutoClearTime")],
            ])
        self.cd_openInviteFriends="cd_openInviteFriends"
        self.cd_closeInviteFriends="cd_closeInviteFriends"
        self.cd_setInviteFriendsQuantity="cd_setInviteFriendsQuantity"
        self.cd_setInviteFriendsAutoClearTime="cd_setInviteFriendsAutoClearTime"
        self.cd_openFollowChannel="cd_openFollowChannel"
        self.cd_closeFollowChannel="cd_closeFollowChannel"
        self.cd_deleteMsgForSecond="cd_deleteMsgForSecond"


        # invitationBonus
        self.InvitationStatisticsSettlementBonusMenu=InlineKeyboardMarkup([
                [InlineKeyboardButton("开启 [邀请奖金功能]", callback_data="cd_openInvitationBonusSet")],
                [InlineKeyboardButton("关闭 [邀请奖金功能]", callback_data="cd_closeInvitationBonusSet")],
                [InlineKeyboardButton("设定 [每邀请(n人)以赚取奖金]", callback_data="cd_setInviteMembers")],
                [InlineKeyboardButton("设定 [邀请达标赚取(n元)奖金]", callback_data="cd_setInviteEarnedOutstand")],
                [InlineKeyboardButton("设定 [满(n元)结算奖金]", callback_data="cd_setInviteSettlementBonus")],
                [InlineKeyboardButton("设定 [联系人]", callback_data="cd_setContactPerson")]
            ])

        self.cd_openInvitationBonusSet="cd_openInvitationBonusSet"
        self.cd_closeInvitationBonusSet="cd_closeInvitationBonusSet"
        self.cd_setInviteMembers="cd_setInviteMembers"
        self.cd_setInviteEarnedOutstand="cd_setInviteEarnedOutstand"
        self.cd_setInviteSettlementBonus="cd_setInviteSettlementBonus"
        self.cd_setContactPerson="cd_setContactPerson"
