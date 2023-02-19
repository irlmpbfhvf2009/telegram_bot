###### BOT說明
>[bot使用方法](#bot使用方法)  
[开启监听频道权限](#开启监听频道权限)  

###### 開發事項  
>[py常用指令](#py常用指令)  
[py檔案](#py檔案)  
[SQL](#SQLITE3)  
[功能進度](#功能進度)  

#### 更新資訊

###### 1.6.4
* 優化介面
* 廣告功能調整(發送第四次廣告,前三次訊息刪除)
* 資料表advertiseRecord (groupId,messageId)
* 統整vite網頁畫面
* config判斷 token檢查
###### 1.6.3
* 完成 UI介面
* 全域logger
* 優化程式碼
###### 1.6.2
* tkinter UI介面
* multiprocessing 多核心運算
* 定義版本號
###### 1.6.1
* API新增
* 查詢、修改config群組
###### 1.6.0
* 侦测机器人所在群组有无权限
* 侦测机器人所在频道有无权限
* 定义3种lor.warning  

        'NoneType' object is not subscriptable       机器人无订阅频道(故无法启动订阅发言权功能)  
        Message can't be deleted                     机器人在群组无足够权限删除消息  
        Not enough rights to manage chat invite link 机器人在群组无足够权限取得邀请连结  



## 开启监听频道权限  
>1.首先我们TG找到BotFather 打开跟他的会话窗口，发送 /setprivacy  
2.点选Disable
<picture>
  <img alt="Shows mode." src="https://img-blog.csdnimg.cn/img_convert/6ed7818985d811d5445ff88cc88b029b.png">
</picture>  



## bot使用方法
>config.ini 填入Token  
run main.py 執行機器人  



## py常用指令
> pip install -r requirements.txt 載入必要的lib  
pyi-makespec -F -w -i tkinter/bot.ico main.py 生成spec檔  
pyi-makespec -F -w main.py 生成spec檔  
pyinstaller main.spec


## py檔案
>main.py  主容器  
app.py  網頁容器  
bot.py bot輪詢  
utils.py  工具類  
_button.py  內聯鍵盤  
_config.py  組態設定  
_sql.py  資料庫處理  
_dirs.py  資料檢查  



## SQLITE3
SCHEMAS:telegram-bot.db
#### TABLE : config  組態設定
###### column: key,value
>password(密碼)  
botuserName 機器人用戶名  
inviteFriendsAutoClearTime 邀請好友記錄清除日期  
inviteFriendsSet 邀請好友發言權開關  
followChannelSet 關注頻道發言權開關  
inviteFriendsQuantity 邀請好友數量  
description 描述  

#### TABLE : invitationLimit 邀請好友紀錄
groupId 群組id,  
groupTitle 群組名稱,  
inviteId 邀請人ID,  
inviteAccount 邀請人帳號,  
beInvited 被邀請人JSON,  
invitationStartDate 邀請日期,  
invitationEndDate 過期日期,  
invitationDate X日清除一次
#### TABLE : manager 管理員
userId 用戶id,  
userName 用戶名稱,  
useGroupTitle 使用的群組名稱,  
useGroupId 使用的群組id,  
isManager 判斷是否為管理員
#### TABLE : lastGroupMessageId 紀錄最後訊息id
groupId 群組id,  
lastMessageId 訊息id
#### TABLE : joinGroup 機器人管理的群組
userId 用戶id,  
userName 用戶名稱,  
groupId 群組id,  
groupTitle 群組名稱,  
link 邀請連結
#### TABLE : joinChannel 機器人管理的頻道
userId 用戶id,  
userName 用戶名稱,  
channelId 頻道id,  
channelTitle 頻道名稱,  
link 邀請連結
#### TABLE : inviteToMakeMoney 邀請好友賺獎金( 邀请6位成员，赚取1.2元未结算，已经结算0元，满100元请联系@xx结算。)
userId 用戶id,  
userName 用戶名稱,  
groupId 群組id,  
groupTitle 群組名稱,  
beInvited 被邀請人JSON,  
outstandingAmount 未結算金額,  
settlementAmount 總結算金額
#### TABLE : joinGroupRecord 入群紀錄
userId 用戶id,  
userName 用戶名稱,  
groupId 群組id,  
groupTitle 群組名稱,  
invite 邀請人,  
joinGroupTime 入群時間



## 功能進度
- [ ] 设置每天禁言时间  
- [x] 删除指定时间内的重复发言，设置间隔时间发广告。  
- [x] 设置邀请指定人数后才能发言,设置几天数为一个周期。 您@用户：您需要邀请2位好友后可以正常发言  
- [x] 设置关注指定频道成员才能发言。没有达标甚至提醒内容。 您@用户：您需要关注频道 @xx 后可以正常发言  
- [ ] 分析当日，昨天新进成员 流失成员，被邀请成员，活跃度成员  
- [x] 增加提示信息控制 xx秒自动删除掉  
