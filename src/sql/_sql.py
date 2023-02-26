import sqlite3,json,time
from decimal import Decimal

'''
sqlite3數據操作封裝
'''
class DBHP():
    def __init__(self,db_name="telegram-bot.db"):
        self.conn = sqlite3.connect(db_name if db_name else 'CattleSpider.db')
        self.cursor = self.conn.cursor()

        # config
        self.password = self.getPassword()
        self.botusername = self.getBotusername()
        self.inviteFriendsAutoClearTime = self.getInviteFriendsAutoClearTime()
        self.inviteFriendsSet = self.getInviteFriendsSet()
        self.followChannelSet =self.getFollowChannelSet()
        self.inviteFriendsQuantity = self.getInviteFriendsQuantity()
        self.deleteSeconds = self.getDeleteSeconds()
        self.invitationBonusSet = self.getInvitationBonusSet()
        self.inviteMembers = self.getInviteMembers()
        self.inviteEarnedOutstand = self.getInviteEarnedOutstand()
        self.inviteSettlementBonus = self.getInviteSettlementBonus()
        self.contactPerson = self.getContactPerson()
        # channel
        self.channelTitle = self.getChannelTitle()
        self.channelLink = self.getChannelLink()


        # create config table
        self.create_tables("config",['key', 'value'])
        # create invitationLimit table
        self.create_tables("invitationLimit",['groupId','groupTitle','inviteId','inviteAccount','beInvited','invitationStartDate','invitationEndDate','invitationDate'])
        # create manager table
        self.create_tables("manager",['userId', 'userName','firstName','useGroupTitle','useGroupId','isManager'])
        # create lastGroupMessageId table
        self.create_tables("lastGroupMessageId",['groupId','lastMessageId'])
        # create joinGroup table
        self.create_tables("joinGroup",['userId','userName','groupId','groupTitle','link'])
        # create joinChannel table
        self.create_tables("joinChannel",['userId','userName','channelId','channelTitle','link'])
        # create joinGroupRecord table
        self.create_tables("joinGroupRecord",['userId','userName','groupId','groupTitle','inviteId','inviteName','joinGroupTime'])
        # create inviteToMakeMoney table
        self.create_tables("inviteToMakeMoney",['userId','userName','groupId','groupTitle','beInvited','outstandingAmount','settlementAmount'])
        # create billingSession table
        self.create_tables("billingSession",['key','value'])
        # create advertise table
        self.create_tables("advertise",['userId','groupId','groupTitle','advertiseSerialNumber','advertiseContent','advertiseTime'])
        # create advertiseRecord table
        self.create_tables("advertiseRecord",['groupId','advertiseMessageId'])

        self.initConfig("password","12356")
        self.initConfig("botuserName","")
        self.initConfig("inviteFriendsAutoClearTime","3")
        self.initConfig("inviteFriendsSet","True")
        self.initConfig("followChannelSet","True")
        self.initConfig("inviteFriendsQuantity","2")
        self.initConfig("deleteSeconds","6")

        # 邀請獎金
        self.initConfig("invitationBonusSet","True")
        self.initConfig("inviteMembers","6")
        self.initConfig("inviteEarnedOutstand","1.2")
        self.initConfig("inviteSettlementBonus","100")
        #self.initConfig("contactPerson","{\"contactPersonId\":\"986843522\",\"contactPersonUsername\":\"@kk\"}")
        self.initConfig("contactPerson","@aa")
        self.initBillingSession("userId","")
        self.initBillingSession("groupId","")

        self.alter_tables("inviteToMakeMoney","firstName")
        self.alter_tables("manager","firstName")
        self.alter_tables("advertise","advertiseSerialNumber")



    def initConfig(self,key,value):
        if self.getConfigKey(key) is None:
            data=[{"key":key,"value":value}]
            self.insert_data("config",data)

    def initBillingSession(self,key,value):
        if self.getBillingSessionKey(key) is None:
            data=[{"key":key,"value":value}]
            self.insert_data("billingSession",data)

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

    def alter_tables(self,table_name:str,col:list)->bool:
        try:
            sql = f"ALTER TABLE {table_name} ADD COLUMN {col};"
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



    # CRUD - config
    def getPassword(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'password'")
        for result in results:
            return result[1]
    def getBotusername(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'botuserName'")
        for result in results:
            return result[1]
    def getInviteFriendsAutoClearTime(self):
        sql=f"SELECT value FROM config WHERE key = 'inviteFriendsAutoClearTime'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]
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


    def getDeleteSeconds(self):
        sql=f"SELECT value FROM config WHERE key = 'deleteSeconds'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]
    def getConfigKey(self,key):
        sql=f"SELECT * FROM config WHERE key = '{key}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]
    def getBillingSessionKey(self,key):
        sql=f"SELECT * FROM billingSession WHERE key = '{key}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]
    def getInviteFriendsQuantity(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'inviteFriendsQuantity'")
        for result in results:
            return result[1]

    def getContactPerson(self):
        results = self.select_all_tasks(f"SELECT value FROM config where key = 'contactPerson'")
        for result in results:
            return result[0]
        
    def editConfig(self,key,value):
        sql=f"UPDATE config SET value='{value}' where key='{key}'"
        self.update(sql)
    def editContactPerson(self,contactPerson):
        sql=f"UPDATE config SET value='{contactPerson}' where key='contactPerson'"
        self.update(sql)
    def editPassword(self,password):
        sql=f"UPDATE config SET value='{password}' where key='password'"
        self.update(sql)
    def editInviteFriends(self,inviteFriendsSet):
        sql=f"UPDATE config SET value='{inviteFriendsSet}' where key='inviteFriendsSet'"
        self.update(sql)
    def editFollowChannel(self,followChannelSet):
        sql=f"UPDATE config SET value='{followChannelSet}' where key='followChannelSet'"
        self.update(sql)
    def editInviteFriendsQuantity(self,inviteFriendsQuantity):
        sql=f"UPDATE config SET value='{inviteFriendsQuantity}' where key='inviteFriendsQuantity'"
        self.update(sql)
    def editInviteFriendsAutoClearTime(self,day):
        sql=f"UPDATE config SET value='{day}' where key='inviteFriendsAutoClearTime'"
        self.update(sql)
    def editBotusername(self,botuserName):
        sql=f"UPDATE config SET value = '{botuserName}' WHERE key = 'botuserName'"
        self.update(sql)
    def editDeleteSeconds(self,deleteSeconds):
        sql=f"UPDATE config SET value = '{deleteSeconds}' WHERE key = 'deleteSeconds'"
        self.update(sql)
        

   # CRUD - manager
    def getAllManager(self):
        sql="SELECT * FROM manager where isManager = 'True'"
        results = self.select_all_tasks(sql)
        return results

    def getManegerFirstName(self):
        sql="SELECT firstName FROM manager where isManager = 'True'"
        results = self.select_all_tasks(sql)
        return results

    def exitManager(self,userId):
        if self.getManager(userId) is None:
            return "尚未取得权限"
        else:
            self.update(f"UPDATE manager SET isManager = 'False' WHERE userId = '{userId}'")
            return '退出成功'
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
    def getUseGroupTitle(self,userId):
        sql=f"SELECT useGroupTitle FROM manager WHERE userId = '{userId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]
    def updateManegerFirstName(self,userId,firstName):
        sql=f"UPDATE manager SET firstName = '{firstName}' WHERE userId = '{userId}'"
        self.update(sql)

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

    def insertManager(self,userId,userName,firstName):
        data=[
            {"userId":str(userId),"userName":userName,"firstName":firstName,"useGroupTitle":"","useGroupId":"","isManager":True}
        ]
        if self.getManager(userId) is None:
            self.insert_data("manager",data)
            return "输入正确，已成功添加"
        else:
            if self.getIsManager(userId) == "True":
                return "管理员账户已存在"
            else:
                self.enterIsManager(userId)
                self.updateManegerFirstName(userId,firstName)
                return "输入正确，已成功添加"

    # CRUD - joinGroup
    def getAllJoinGroupIdAndTitle(self):
        sql=f"SELECT groupId,groupTitle FROM joinGroup"
        results = self.select_all_tasks(sql)
        return results

    def getGroupTitle(self,groupId):
        sql=f"SELECT groupTitle FROM joinGroup where groupId='{groupId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]

    def getJoinGroupLink(self,groupId):
        sql=f"SELECT link FROM joinGroup where groupId='{groupId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result
    def getJoinGroupId(self,groupId):
        sql=f"SELECT * FROM joinGroup WHERE groupId = '{groupId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result[0]
    def insertJoinGroup(self,userId,userName,groupId,groupTitle,link):
        data=[
            {"userId":str(userId),"userName":userName,"groupId":str(groupId),"groupTitle":groupTitle,"link":link}
        ]
        if self.getJoinGroupId(groupId) is None:
            self.insert_data("joinGroup",data)

    def existJoinGroupId(self,groupId):
        results = self.select_all_tasks(f"SELECT groupId FROM joinGroup where groupId = '{groupId}'")
        if results == []:
            return False
        else:
            for result in results:
                if str(result[0]) == str(groupId):
                    return True
                else:
                    return False

    def updateJoinGroup(self,groupId,groupTitle,link):
        data=[
            {"userId":"","userName":"","groupId":str(groupId),"groupTitle":groupTitle,"link":link}
        ]
        if self.existJoinGroupId(groupId) == False:
            self.insert_data("joinGroup",data)
    
    def deleteJoinGroup(self,groupId):
        self.delete(f"delete from joinGroup where groupId = '{groupId}'")

    # CRUD - joinChannel

    def getJoinChannelLink(self,channelId):
        sql=f"SELECT link FROM joinChannel where channelId='{channelId}'"
        results = self.select_all_tasks(sql)
        for result in results:
            return result
    def getAllJoinChannelIdAndTitle(self):
        sql=f"SELECT channelId,channelTitle FROM joinChannel"
        results = self.select_all_tasks(sql)
        return results
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

    def existJoinChannelId(self,channelId):
        results = self.select_all_tasks(f"SELECT channelId FROM joinChannel where channelId = '{channelId}'")
        if results == []:
            return False
        else:
            for result in results:
                if str(result[0]) == str(channelId):
                    return True
                else:
                    return False

    def updateJoinChannel(self,channelId,channelTitle,link):
        data=[
            {"userId":"","userName":"","channelId":str(channelId),"channelTitle":channelTitle,"link":link}
        ]
        if self.existJoinChannelId(channelId) == False:
            self.insert_data("joinChannel",data)
            
    def deleteJoinChannel(self,channelId):
        self.delete(f"delete from joinChannel where channelId = '{channelId}'")

    # CRUD - lastGroupMessageId

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

    # CRUD - invitationLimit
    def AutoClearinviteFriends(self,time):
        results = self.select_all_tasks("SELECT * FROM invitationLimit")
        for result in results:
            endTime = result[6]
            if endTime < time:
                self.update(f"UPDATE invitationLimit SET beInvited='',invitationStartDate='',invitationEndDate='',invitationDate='{self.inviteFriendsAutoClearTime}' where inviteId = '{result[2]}' AND groupId='{result[0]}' ")

    def getInvitationEndDate(self,inviteId,groupId):
        results = self.select_all_tasks(f"SELECT invitationEndDate FROM invitationLimit where inviteId = '{inviteId}' AND groupId = '{groupId}'")
        return results

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
            if result[0] == '':
                JSON_data = {}
            else:
                JSON_data = json.loads(result[0])
        for key,value in json.loads(data[0]['beInvited']).items():
            JSON_data[key] = value
        self.update(f"UPDATE invitationLimit SET beInvited = '{json.dumps(JSON_data)}',invitationStartDate='{invitationStartDate}',invitationEndDate='{invitationEndDate}',invitationDate='{invitationDate}' WHERE inviteId = '{inviteId}' AND groupId = '{groupId}'")

    def messageLimitToInviteFriends(self,userId,groupId):
        results = self.select_all_tasks(f"SELECT beInvited FROM invitationLimit where inviteId = '{userId}' AND groupId = '{groupId}'")
        for result in results:
            if result[0] =='':
                return False
            JSON_data=json.loads(result[0])
            lenBeInvited = len(JSON_data)
            if lenBeInvited >= int(self.inviteFriendsQuantity):
                return True
        return False

    def getDynamicInviteFriendsQuantity(self,userId):
        results = self.select_all_tasks(f"SELECT beInvited FROM invitationLimit where inviteId = '{userId}'")
        if results == []:
            return 0
        for result in results:
            if result[0] == '':
                return self.inviteFriendsQuantity
            JSON_data=json.loads(result[0])
            lenBeInvited = len(JSON_data)
            return lenBeInvited

    # CRUD - joinGroupRecord


    def getInvitationBonusSet(self):
        results = self.select_all_tasks(f"SELECT value FROM config where key = 'invitationBonusSet'")
        for result in results:
            return result[0]
    def getInviteMembers(self):
        results = self.select_all_tasks(f"SELECT value FROM config where key = 'inviteMembers'")
        for result in results:
            return result[0]
    def getInviteEarnedOutstand(self):
        results = self.select_all_tasks(f"SELECT value FROM config where key = 'inviteEarnedOutstand'")
        for result in results:
            return result[0]
    def getInviteSettlementBonus(self):
        results = self.select_all_tasks(f"SELECT value FROM config where key = 'inviteSettlementBonus'")
        for result in results:
            return result[0]


    def insertJoinGroupRecord(self,userId,userName,groupId,groupTitle,inviteId,inviteName,joinGroupTime):
        data=[
            {"userId":userId,"userName":userName,"groupId":groupId,"groupTitle":groupTitle,"inviteId":inviteId,"inviteName":inviteName,"joinGroupTime":joinGroupTime}
        ]
        if self.existJoinRecord(userId,groupId) == False:
            self.insert_data("joinGroupRecord",data)

    def existJoinRecord(self,userId,groupId):
        results = self.select_all_tasks(f"SELECT * FROM joinGroupRecord where userId = '{userId}' AND groupId = '{groupId}'")
        if results == []:
            return False
        else:
            for result in results:
                if str(result[0]) == str(userId) and str(result[2]) == str(groupId):
                    return True
                else:
                    return False


    def editInvitationBonusSet(self,invitationBonusSet):
        sql=f"UPDATE config SET value='{invitationBonusSet}' where key='invitationBonusSet'"
        self.update(sql)
    def editInviteMembers(self,inviteMembers):
        sql=f"UPDATE config SET value='{inviteMembers}' where key='inviteMembers'"
        self.update(sql)
    def editInviteEarnedOutstand(self,inviteEarnedOutstand):
        sql=f"UPDATE config SET value='{inviteEarnedOutstand}' where key='inviteEarnedOutstand'"
        self.update(sql)
    def editInviteSettlementBonus(self,inviteSettlementBonus):
        sql=f"UPDATE config SET value='{inviteSettlementBonus}' where key='inviteSettlementBonus'"
        self.update(sql)

    # CRUD - inviteToMakeMoney
    def existInviteToMakeMoney(self,userId,groupId):
        results = self.select_all_tasks(f"SELECT * FROM inviteToMakeMoney where userId = '{userId}' AND groupId = '{groupId}'")
        if results == []:
            return False
        else:
            for result in results:
                if str(result[0]) == str(userId) and str(result[2]) == str(groupId):
                    return True
                else:
                    return False

    def existJoinRecordTotInviteToMakeMoney(self,inviteId,groupId,userId):
        results = self.select_all_tasks(f"SELECT * FROM joinGroupRecord where userId = '{userId}' AND groupId = '{groupId}' AND inviteId ='{inviteId}'")
        if results == []:
            return False
        else:
            for result in results:
                if str(result[0]) == str(userId) and str(result[2]) == str(groupId) and str(result[4])== str(inviteId):
                    return True
                else:
                    return False

    def insertInviteToMakeMoney(self,userId,userName,groupId,groupTitle,beInvited,beInvitedId,firstName):

        data=[
            {"userId":userId,"userName":userName,"groupId":groupId,"groupTitle":groupTitle,"beInvited":beInvited,"outstandingAmount":"0","settlementAmount":"0","firstName":firstName}
        ]
        if self.existJoinRecordTotInviteToMakeMoney(userId,groupId,beInvitedId)==True:
            self.updateInviteToMakeMoneyFirstName(userId,groupId,firstName)
            return
        if self.existInviteToMakeMoney(userId,groupId) == False:
            self.insert_data("inviteToMakeMoney",data)
        else:
            self.updateInviteToMakeMoneyBeInvited(userId,groupId,data)
            self.updateInviteToMakeMoneyOutstandingAmount(userId,groupId)
            self.updateInviteToMakeMoneyFirstName(userId,groupId,firstName)

    def updateInviteToMakeMoneyBeInvited(self,userId,groupId,data):
        results = self.select_all_tasks(f"SELECT beInvited FROM inviteToMakeMoney where userId = '{userId}' AND groupId = '{groupId}'")
        for result in results:
            if result[0] == '':
                JSON_data = {}
            else:
                JSON_data = json.loads(result[0])
        for key,value in json.loads(data[0]['beInvited']).items():
            JSON_data[key] = value
        self.update(f"UPDATE inviteToMakeMoney SET beInvited = '{json.dumps(JSON_data)}' WHERE userId = '{userId}' AND groupId = '{groupId}'")
    
    def updateInviteToMakeMoneyOutstandingAmount(self,userId,groupId):
        bouns = self.bounsCount(userId,groupId)
        #results = self.select_all_tasks(f"SELECT * FROM joinGroupRecord where groupId = '{groupId}'")
        self.update(f"UPDATE inviteToMakeMoney SET outstandingAmount = '{bouns}' WHERE userId = '{userId}' AND groupId = '{groupId}'")
    def updateInviteToMakeMoneyFirstName(self,userId,groupId,firstName):
        self.update(f"UPDATE inviteToMakeMoney SET firstName = '{firstName}' WHERE userId = '{userId}' AND groupId = '{groupId}'")


    def bounsCount(self,userId,groupId):
        inviteEarnedOutstand = self.inviteEarnedOutstand
        inviteMembers = int(self.inviteMembers)
        beInvitedLen =int(self.getInviteToMakeMoneyBeInvitedLen(userId,groupId))
        if beInvitedLen < inviteMembers:
            return "0"
        elif beInvitedLen == inviteMembers:
            return inviteEarnedOutstand
        elif beInvitedLen > inviteMembers:
            bouns = Decimal('0')
            while(beInvitedLen >= inviteMembers): 
                beInvitedLen=beInvitedLen-inviteMembers
                bouns+=Decimal(inviteEarnedOutstand)
        return str(bouns)

    def editInviteToMakeMoneyBeInvited(self,userId,groupId,data):
        self.update(f"UPDATE inviteToMakeMoney SET beInvited = '{data}' WHERE userId = '{userId}' AND groupId = '{groupId}'")
    
    def getInviteToMakeMoney(self,groupId):
        results = self.select_all_tasks(f"SELECT * FROM inviteToMakeMoney where groupId = '{groupId}'")
        return results
    def getInviteToMakeMoneyUserName(self,userName):
        results = self.select_all_tasks(f"SELECT * FROM inviteToMakeMoney where firstName = '{userName}'")
        return results
    def getOutstandingAmount(self,userId,groupId):
        results = self.select_all_tasks(f"SELECT outstandingAmount FROM inviteToMakeMoney where userId = '{userId}' AND groupId = '{groupId}'")
        for result in results:
            return result[0]
    def getInviteToMakeMoneyBeInvitedLen(self,userId,groupId):
        results = self.select_all_tasks(f"SELECT beInvited FROM inviteToMakeMoney where userId = '{userId}' AND groupId = '{groupId}'")
        for result in results:
            return len(json.loads(result[0]))
        if results == []:
            return 0

    def updateInviteToMakeMoneyLeftGroup(self,beInvitedId,groupId):
        results = self.getInviteToMakeMoney(groupId)
        for result in results:
            beInvited = json.loads(result[4])
            for key,value in json.loads(result[4]).items():
                if str(key) == str(beInvitedId):
                    del beInvited[key]
                    self.editInviteToMakeMoneyBeInvited(result[0],result[2],json.dumps(beInvited))
                    self.updateInviteToMakeMoneyOutstandingAmount(result[0],result[2])
    
    def getSettlementAmount(self,userId,groupId):
        results = self.select_all_tasks(f"SELECT settlementAmount FROM inviteToMakeMoney where userId = '{userId}' AND groupId = '{groupId}'")
        for result in results:
            return result[0]
    
    def getInviteToMakeMoneyEarnBonus(self,userId,groupId):
        results = self.select_all_tasks(f"SELECT * FROM inviteToMakeMoney where groupId = '{groupId}' AND userId = '{userId}'")
        return results

    def earnBonus(self,userId,groupId,price):
        results = self.getInviteToMakeMoneyEarnBonus(userId,groupId)
        p = str(price)
        for result in results:
            outstandingAmount = Decimal(result[5]) - Decimal(p)
            settlementAmount = Decimal(result[6]) + Decimal(p)
            beInvited="{}"
            self.update(f"UPDATE inviteToMakeMoney SET outstandingAmount = '{outstandingAmount}' WHERE userId = '{userId}' AND groupId = '{groupId}'")
            self.update(f"UPDATE inviteToMakeMoney SET settlementAmount = '{settlementAmount}' WHERE userId = '{userId}' AND groupId = '{groupId}'")
            self.update(f"UPDATE inviteToMakeMoney SET beInvited = '{beInvited}' WHERE userId = '{userId}' AND groupId = '{groupId}'")
   
    # CRUD - billingSession
    def setBillingSessionUserId(self,userId):
        self.update(f"UPDATE billingSession SET value = '{userId}' WHERE key = 'userId'")
    def setBillingSessionGroupId(self,groupId):
        self.update(f"UPDATE billingSession SET value = '{groupId}' WHERE key = 'groupId'")
    def getBillingSessionUserId(self):
        results = self.select_all_tasks(f"SELECT value FROM billingSession where key = 'userId'")
        for result in results:
            return result[0]

    def getBillingSessionGroupId(self):
        results = self.select_all_tasks(f"SELECT value FROM billingSession where key = 'groupId'")
        for result in results:
            return result[0]

    # CRUD - advertise
    def getAdvertise(self,groupId):
        results = self.select_all_tasks(f"SELECT * FROM advertise where groupId = '{groupId}'")
        return results
    
    def deleteAdvertiseForGroupId(self,groupId):
        self.delete(f"delete from advertise where groupId = '{groupId}'")
    
        
    def getAdvertiseContent(self,groupId):
        results = self.select_all_tasks(f"SELECT advertiseContent FROM advertise where groupId = '{groupId}'")
        return results
        # for result in results:
        #     return result[0]

    def getAdvertiseTime(self,groupId):
        results = self.select_all_tasks(f"SELECT advertiseTime FROM advertise where groupId = '{groupId}'")
        if results == []:
            return 0
        for result in results:
            return result[0]
        
    def getAdvertiseSerialNumbere(self,groupId):
        results = self.select_all_tasks(f"SELECT advertiseSerialNumber FROM advertise where groupId = '{groupId}'")
        return results

    # def existGroupIdAdvertise(self,groupId):
    #     results = self.select_all_tasks(f"SELECT * FROM advertise where groupId = '{groupId}'")
    #     if results == []:
    #         return False
    #     else:
    #         for result in results:
    #             if str(result[1]) == str(groupId):
    #                 return True
    #             else:
    #                 return False


    # ("advertise",['userId','groupId','groupTitle','advertiseSerialNumber','advertiseContent','advertiseTime'])

    def insertAdvertise(self,userId,groupId,groupTitle,advertiseContent,advertiseTime):
        advertiseSerialNumber = str(int(time.time()))
        data=[
            {"userId":userId,"groupId":groupId,"groupTitle":groupTitle,"advertiseSerialNumber":advertiseSerialNumber,"advertiseContent":advertiseContent,"advertiseTime":advertiseTime}
        ]
        # if self.existGroupIdAdvertise(groupId) == False:
        self.insert_data("advertise",data)

    def updateAdvertise(self,groupId,advertiseContent,advertiseTime):
        self.update(f"UPDATE advertise SET advertiseContent = '{advertiseContent}' ,advertiseTime = '{advertiseTime}' WHERE groupId = '{groupId}'")
    
    def updateAdvertiseTime(self,groupId,advertiseTime):
        self.update(f"UPDATE advertise SET advertiseTime = '{advertiseTime}' WHERE groupId = '{groupId}'")
        
    def updateAdvertiseContent(self,groupId,advertiseContent):
        self.update(f"UPDATE advertise SET advertiseContent = '{advertiseContent}' WHERE groupId = '{groupId}'")

    # CRUD - advertiseRecord
    def insertAdvertiseRecord(self,groupId,advertiseMessageId):
        data=[
            {"groupId":groupId,"advertiseMessageId":advertiseMessageId}
        ]
        self.insert_data("advertiseRecord",data)
        
    def getAdvertiseRecord(self,groupId):
        results = self.select_all_tasks(f"SELECT advertiseMessageId FROM advertiseRecord where groupId = '{groupId}'")
        return results
        
    def deletetAdvertiseRecord(self,groupId):
        self.delete(f"delete from advertiseRecord where groupId = '{groupId}'")
        
    # destroy
    def destroy(self):
        self.delete("delete from advertise")
        self.delete("delete from billingSession")
        self.delete("delete from config")
        self.delete("delete from invitationLimit")
        self.delete("delete from inviteToMakeMoney")
        self.delete("delete from joinChannel")
        self.delete("delete from joinGroup")
        self.delete("delete from joinGroupRecord")
        self.delete("delete from lastGroupMessageId")
        self.delete("delete from manager")