1. 设置每天禁言时间段 

2. 删除指定时间内的重复发言，设置间隔时间发广告。

3. 设置邀请指定人数后才能发言,设置几天数为一个周期。,

4. 设置关注指定频道成员才能发言。没有达标甚至提醒内容。 

5. 分析当日，昨天新进成员 流失成员，被邀请成员，活跃度成员

您@用户：您需要邀请2位好友后可以正常发言  （2使用红色字）

您@用户：您需要关注频道 @xx 后可以正常发言  （跳转频道删除掉）

增加提示信息控制 xx秒自动删除掉

SQLITE3
SCHEMAS : telegram-bot.db

TABLE 
config            組態設定     key   value
invitationLimit   邀请好友紀錄 inviteId(邀請人ID)  inviteAccount(邀請人帳號) beInvitedId(被邀請人ID)beInvitedAccoun(被邀請人帳號)
        