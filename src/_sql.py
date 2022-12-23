import sqlite3
import json

'''
sqlite3數據操作封裝
'''
class DBHP():
    def __init__(self,db_name=None):
        self.conn = sqlite3.connect(db_name if db_name else 'CattleSpider.db')
        self.cursor = self.conn.cursor()

        configTable = self.create_tables("config",['key', 'value'])
        if configTable == True:
            data=[
                {"key":"password","value":"12356"},
                {"key":"botuserName","value":""},
                {"key":"inviteFriendsAutoClearTime","value":"3"},
                {"key":"inviteFriendsSet","value":"True"},
                {"key":"followChannelSet","value":"True"},
                {"key":"inviteFriendsQuantity","value":"2"},
                {"key":"description","value":"1设置每天禁言时间段\n2删除指定时间内的重复发言，设置间隔时间发广告。\n3设置邀请指定人数后才能发言,设置几天数为一个周期。\n4设置关注指定频道成员才能发言。没有达标甚至提醒内容。 \n5分析当日，昨天新进成员 流失成员，被邀请成员，活跃度成员\n您@用户：您需要邀请2位好友后可以正常发言  （2使用红色字）\n您@用户：您需要关注频道 @xx 后可以正常发言  （跳转频道删除掉）\n增加提示信息控制 xx秒自动删除掉"}
            ]
            self.insert_data("config",data)

        # create invitationLimit table
        self.create_tables("invitationLimit",['groupId','groupTitle','inviteId','inviteAccount','beInvited','invitationStartDate','invitationEndDate','invitationDate'])
        # create manager table
        self.create_tables("manager",['userId', 'userName','useGroupTitle','useGroupId','isManager'])
        # create lastGroupMessageId table
        self.create_tables("lastGroupMessageId",['groupId','lastMessageId'])
        # create joinGroup table
        self.create_tables("joinGroup",['userId','userName','groupId','groupTitle','link'])
        # create joinChannel table
        self.create_tables("joinChannel",['userId','userName','channelId','channelTitle','link'])

        self.inviteFriendsQuantity = self.getInviteFriendsQuantity()
        self.token = self.getToken()
        self.password = self.getPassword()
        self.botusername = self.getBotName()
        self.description = self.getDescription()
        self.channelTitle = self.getChannelTitle()
        self.channelLink = self.getChannelLink()
        self.inviteFriendsAutoClearTime = self.getInviteFriendsAutoClearTime()

    def tables_in_sqlite_db(self):
        self.cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [
            v[0] for v in self.cursor.fetchall()
            if v[0] != "sqlite_sequence"
        ]
        self.cursor.close()
        return tables
    '''
    創建表格
    @:param table_name 表名
    @:param field_list 字段列表,例如：["name","age","gender"]
    @:return 
    '''
    def create_tables(self,table_name:str,field_list:list)->bool:
        try:
            fields=",".join([field+" TEXT" for field in field_list])
            sql = f"CREATE TABLE {table_name} ({fields});"
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception:
            return False
    '''
    插入數據，根據傳入的數據類型進行判斷，自動選擇插入方式
    @:param table_name 表名
    @:param data 要插入的數據
    '''
    def insert_data(self,table_name:str,data)->bool:
        try:
            if isinstance(data,list):
                for item in data:
                    keys = ",".join(list(item.keys()))
                    values = ",".join([f"'{x}'" for x in list(item.values())])
                    sql = f"INSERT INTO {table_name} ({keys}) VALUES ({values});"
                    self.cursor.execute(sql)
            elif isinstance(data,dict):
                keys = ",".join(list(data.keys()))
                values = ",".join([f"'{x}'" for x in list(data.values())])
                sql = f"INSERT INTO {table_name} ({keys}) VALUES ({values});"
                self.cursor.execute(sql)
            return True
        except Exception as ex:
            return False
        finally:
            self.conn.commit()

    # 更新数据
    def update(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()

    # 删除数据
    def delete(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return '退出成功'
    '''
    查詢數據
    @:param 要查詢的sql語句
    '''
    def select_all_tasks(self,sql:str)->list:
        try:
            self.cursor = self.conn.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            return []

    '''
    關閉數據庫連接
    '''
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as ex:
            raise Exception("關閉數據庫連接失敗")

    def getAllManager(self):
        sql="SELECT * FROM manager where isManager = 'True'"
        results = self.select_all_tasks(sql)
        return results

    def exitManager(self,userId):
        if self.getManager(userId) is None:
            return "尚未取得权限"
        else:
            self.update(f"UPDATE manager SET isManager = 'False' WHERE userId = '{userId}'")
            return '退出成功'

    def getInviteFriendsAutoClearTime(self):
        sql=f"SELECT value FROM config WHERE key = 'inviteFriendsAutoClearTime'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]

    def getManager(self,userId):
        sql=f"SELECT * FROM manager WHERE userId = '{userId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result

    def getManagerName(self,userId):
        sql=f"SELECT * FROM manager WHERE userId = '{userId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[1]

    def getIsManager(self,userId):
        sql=f"SELECT isManager FROM manager WHERE userId = '{userId}'"
        results = self.select_all_tasks(sql)
        if results == []:
            return "False"
        for result in results:
            return result[0]

    def enterIsManager(self,userId):
        sql=f"UPDATE manager SET isManager = 'True' WHERE userId = '{userId}'"
        self.update(sql)

    def updateUseGroup(self,userId,groupTitle,groupId):
        sql=f"UPDATE manager SET useGroupTitle='{groupTitle}',useGroupId = '{groupId}' WHERE userId = '{userId}'"
        self.update(sql)

    def getUseGroupId(self,userId):
        sql=f"SELECT useGroupId FROM manager WHERE userId = '{userId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]

    def updatePassword(self,newPassword):
        sql=f"UPDATE config SET value='{newPassword}' where key='password'"
        self.update(sql)

    def getInviteFriendsSet(self):
        sql=f"SELECT value FROM config WHERE key = 'inviteFriendsSet'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]
    def getFollowChannelSet(self):
        sql=f"SELECT value FROM config WHERE key = 'followChannelSet'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]

    def openInviteFriends(self):
        sql=f"UPDATE config SET value='{True}' where key='inviteFriendsSet'"
        self.update(sql)
    def closeInviteFriends(self):
        sql=f"UPDATE config SET value='{False}' where key='inviteFriendsSet'"
        self.update(sql)
    def openFollowChannel(self):
        sql=f"UPDATE config SET value='{True}' where key='followChannelSet'"
        self.update(sql)
    def closeFollowChannel(self):
        sql=f"UPDATE config SET value='{False}' where key='followChannelSet'"
        self.update(sql)
    def setInviteFriendsQuantity(self,quantity):
        sql=f"UPDATE config SET value='{quantity}' where key='inviteFriendsQuantity'"
        self.update(sql)
    def setInviteFriendsAutoClearTime(self,day):
        sql=f"UPDATE config SET value='{day}' where key='inviteFriendsAutoClearTime'"
        self.update(sql)

    # insertManager
    def insertManager(self,userId,userName):
        data=[
            {"userId":str(userId),"userName":userName,"useGroupTitle":"","useGroupId":"","isManager":True}
        ]
        if self.getManager(userId) is None:
            self.insert_data("manager",data)
            return "输入正确，已成功添加"
        else:
            if self.getIsManager(userId) == "True":
                return "管理员账户已存在"
            else:
                self.enterIsManager(userId)
                return "输入正确，已成功添加"

    def getAllJoinGroupIdAndTitle(self):
        sql=f"SELECT groupId,groupTitle FROM joinGroup"
        results = self.select_all_tasks(sql)
        return results

    def getAllJoinChannelIdAndTitle(self):
        sql=f"SELECT channelId,channelTitle FROM joinChannel"
        results = self.select_all_tasks(sql)
        return results

    def getJoinGroupLink(self,groupId):
        sql=f"SELECT link FROM joinGroup where groupId='{groupId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result

    def getJoinChannelLink(self,channelId):
        sql=f"SELECT link FROM joinChannel where channelId='{channelId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result

    def getJoinGroupId(self,groupId):
        sql=f"SELECT * FROM joinGroup WHERE groupId = '{groupId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]

    def getJoinChannelId(self,channelId):
        sql=f"SELECT * FROM joinChannel WHERE channelId = '{channelId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result

    def getChannelId(self):
        sql=f"SELECT channelId FROM joinChannel"
        results = self.select_all_tasks(sql)
        for result in results:
            return result
    def getChannelTitle(self):
        sql=f"SELECT channelTitle FROM joinChannel"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]
    def insertJoinChannel(self,userId,userName,channelId,channelTitle,link):
        data=[
            {"userId":str(userId),"userName":userName,"channelId":str(channelId),"channelTitle":channelTitle,"link":link}
        ]
        if self.getJoinChannelId(channelId) is None:
            self.delete(f"delete from joinChannel")
            self.insert_data("joinChannel",data)

    def getChannelLink(self):
        sql=f"SELECT link FROM joinChannel"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]
    def insertJoinGroup(self,userId,userName,groupId,groupTitle,link):
        data=[
            {"userId":str(userId),"userName":userName,"groupId":str(groupId),"groupTitle":groupTitle,"link":link}
        ]
        if self.getJoinGroupId(groupId) is None:
            self.insert_data("joinGroup",data)
    
    def deleteJoinGroup(self,groupId):
        self.delete(f"delete from joinGroup where groupId = '{groupId}'")

    def deleteJoinChannel(self,channelId):
        self.delete(f"delete from joinChannel where channelId = '{channelId}'")

    def getLastGroupMessageId(self,groupId):
        sql=f"SELECT lastMessageId FROM lastGroupMessageId WHERE groupId = '{groupId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]

    def insertLastGroupMessageId(self,groupId,lastMessageId):
        data=[
            {"groupId":str(groupId),"lastMessageId":str(lastMessageId)}
        ]
        if self.getLastGroupMessageId(groupId) is None:
            self.insert_data("lastGroupMessageId",data)
        else:
            self.update(f"UPDATE lastGroupMessageId SET lastMessageId = '{lastMessageId}' WHERE groupId = '{groupId}'")

    def updateConfig(self,botusername):
        sql=f"UPDATE config SET value = '{botusername}' WHERE key = 'botuserName'"
        self.update(sql)
        
    def getToken(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'token'")
        for result in results:
            return result[1]

    def getDescription(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'description'")
        for result in results:
            return result[1]

    def getPassword(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'password'")
        for result in results:
            return result[1]

    def getBotName(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'botuserName'")
        for result in results:
            return result[1]

    def getInviteFriendsQuantity(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'inviteFriendsQuantity'")
        for result in results:
            return result[1]

    def AutoClearinviteFriends(self):
        results = self.select_all_tasks("SELECT * FROM invitationLimit")
        for result in results:
            if result[5]>result[6] == True:
                self.delete(f"delete from invitationLimit where inviteId = '{result[2]}'")

    def insertInvitationLimit(self,groupId,groupTitle,inviteId,inviteAccount,beInvited,invitationStartDate,invitationEndDate,invitationDate):
        data=[
            {"groupId":groupId,"groupTitle":groupTitle,"inviteId":inviteId,"inviteAccount":inviteAccount,"beInvited":beInvited,"invitationStartDate":invitationStartDate,"invitationEndDate":invitationEndDate,"invitationDate":invitationDate}
        ]
        if self.existInviteIdAndGroupId(inviteId,groupId) == False:
            self.insert_data("invitationLimit",data)
        else:
            self.updateBeInvited(inviteId,groupId,data,invitationStartDate,invitationEndDate,invitationDate)

    def getInvitationLimit(self):
        results = self.select_all_tasks("SELECT * FROM invitationLimit")
        for result in results:
            return result

    def existInviteIdAndGroupId(self,inviteId,groupId):
        results = self.select_all_tasks(f"SELECT * FROM invitationLimit where inviteId = '{inviteId}' AND groupId = '{groupId}'")
        if results == []:
            return False
        else:
            for result in results:
                if str(result[0]) == str(groupId) and str(result[2]) == str(inviteId):
                    return True
                else:
                    return False

    def updateBeInvited(self,inviteId,groupId,data,invitationStartDate,invitationEndDate,invitationDate):
        results = self.select_all_tasks(f"SELECT beInvited FROM invitationLimit where inviteId = '{inviteId}' AND groupId = '{groupId}'")
        for result in results:
            JSON_data = json.loads(result[0])
        for key,value in json.loads(data[0]['beInvited']).items():
            JSON_data[key] = value
        self.update(f"UPDATE invitationLimit SET beInvited = '{json.dumps(JSON_data)}',invitationStartDate='{invitationStartDate}',invitationEndDate='{invitationEndDate}',invitationDate='{invitationDate}' WHERE inviteId = '{inviteId}' AND groupId = '{groupId}'")

    def messageLimitToInviteFriends(self,userId):
        results = self.select_all_tasks(f"SELECT beInvited FROM invitationLimit where inviteId = '{userId}'")
        for result in results:
            JSON_data=json.loads(result[0])
            lenBeInvited = len(JSON_data)
            if lenBeInvited >= int(self.inviteFriendsQuantity):
                return True
        return False

    def getDynamicInviteFriendsQuantity(self,userId):
        results = self.select_all_tasks(f"SELECT beInvited FROM invitationLimit where inviteId = \"{userId}\"")
        if results == []:
            return self.inviteFriendsQuantity
        for result in results:
            JSON_data=json.loads(result[0])
            lenBeInvited = len(JSON_data)
            return lenBeInvited
