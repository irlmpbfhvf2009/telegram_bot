###### 1.6.1
* 新增網頁API
* 查詢、修改config群組

###### 1.6.0 更新说明
* 侦测机器人所在群组有无权限
* 侦测机器人所在频道有无权限
* 定义3种lor.warning 
        1. 'NoneType' object is not subscriptable       机器人无订阅频道(故无法启动订阅发言权功能)
        2. Message can't be deleted                     机器人在群组无足够权限删除消息
        3. Not enough rights to manage chat invite link 机器人在群组无足够权限取得邀请连结

开启监听频道权限

1.首先我们TG找到BotFather 打开跟他的会话窗口，发送 /setprivacy
<picture>
  <img alt="Shows mode." src="https://img-blog.csdnimg.cn/img_convert/6ed7818985d811d5445ff88cc88b029b.png">
</picture>


2.点选Disable


###### bot 使用方法
>config.ini 填入Token

run main.py 執行機器人


###### py 常用指令
> pip install -r requirements.txt 載入必要的lib
        4.pyinstaller -F .\main.py 打包
        5.pyinstaller -F -i .\1.ico .\main.py 打包
        6.pyinstaller -F .\app.py 打包

_button.py 內連鍵盤封裝

_config.py 建立參數

_sql.py 資料庫處理

_bot.py 機器人輪詢 


SQLITE3　SCHEMAS : telegram-bot.db

TABLE : config  組態設定   


column: key,value

        password(密碼)    

        botuserName(機器人用戶名)

        inviteFriendsAutoClearTime(邀請好友記錄清除日期)     

        inviteFriendsSet(邀請好友發言權開關)

        followChannelSet(關注頻道發言權開關)

        inviteFriendsQuantity(邀請好友數量)

        description(描述)


TABLE : invitationLimit 邀請好友紀錄

column : groupId(群組id),groupTitle(群組名稱),inviteId(邀請人ID),inviteAccount(邀請人帳號),beInvited(被邀請人JSON),invitationStartDate(邀請日期),invitationEndDate(過期日期),invitationDate(X日清除一次)


TABLE : manager 管理員

column : userId(用戶id),userName(用戶名稱),useGroupTitle(使用的群組名稱),useGroupId(使用的群組id),isManager(判斷是否為管理員)


TABLE : lastGroupMessageId 紀錄最後訊息id

column : groupId(群組id),lastMessageId(訊息id)


TABLE : joinGroup 機器人管理的群組

userId(用戶id),userName(用戶名稱),groupId(群組id),groupTitle(群組名稱),link(邀請連結)


TABLE : joinChannel 機器人管理的頻道

userId(用戶id),userName(用戶名稱),channelId(頻道id),channelTitle(頻道名稱),link(邀請連結)


TABLE : inviteToMakeMoney 邀請好友賺獎金(您邀请6位成员，赚取1.2元未结算，已经结算0元，满100元请联系@xx结算。)

userId(用戶id),userName(用戶名稱),groupId(群組id),groupTitle(群組名稱),beInvited(被邀請人JSON),outstandingAmount(未結算金額),settlementAmount(總結算金額)


TABLE : joinGroupRecord 入群紀錄

userId(用戶id),userName(用戶名稱),groupId(群組id),groupTitle(群組名稱),invite(邀請人),joinGroupTime(入群時間)



1. 设置每天禁言时间
(時間段未完成)

2. 删除指定时间内的重复发言，设置间隔时间发广告。 
(已完成)

3. 设置邀请指定人数后才能发言,设置几天数为一个周期。 您@用户：您需要邀请2位好友后可以正常发言  （2使用红色字）
(已完成)

4. 设置关注指定频道成员才能发言。没有达标甚至提醒内容。 您@用户：您需要关注频道 @xx 后可以正常发言  （跳转频道删除掉）
(以完成)

5. 分析当日，昨天新进成员 流失成员，被邀请成员，活跃度成员
(未開發)

增加提示信息控制 xx秒自动删除掉
(已完成)
