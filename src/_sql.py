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
                {"key":"token","value":"5855785269:AAH9bvPpYudd2wSAvMnBTiKakCeoB92_Z_8"},
                {"key":"password","value":"RYANGOD"},
                {"key":"botuserName","value":"CCP1121_BOT"},
                {"key":"description","value":"1设置每天禁言时间段\n2删除指定时间内的重复发言，设置间隔时间发广告。\n3设置邀请指定人数后才能发言,设置几天数为一个周期。\n4设置关注指定频道成员才能发言。没有达标甚至提醒内容。 \n5分析当日，昨天新进成员 流失成员，被邀请成员，活跃度成员\n您@用户：您需要邀请2位好友后可以正常发言  （2使用红色字）\n您@用户：您需要关注频道 @xx 后可以正常发言  （跳转频道删除掉）\n增加提示信息控制 xx秒自动删除掉"}
            ]
            self.insert_data("config",data)

        # invitationLimit table
        self.create_tables("invitationLimit",['inviteId', 'inviteAccount','beInvited'])
            
        self.token = self.getToken()
        self.password = self.getPassword()
        self.botusername = self.getBotName()

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
        except Exception as ex:
            #print(str(ex))
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


        

    # getToken
    def getToken(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'token'")
        for result in results:
            return result[1]
        self.close()

    # getPassword
    def getPassword(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'password'")
        for result in results:
            return result[1]
        self.close()

    # getBotName
    def getBotName(self):
        results = self.select_all_tasks("SELECT * FROM config WHERE key = 'botuserName'")
        for result in results:
            return result[1]
        self.close()

    # getInvitationLimit
    def getInvitationLimit(self):
        results = self.select_all_tasks("SELECT * FROM invitationLimit")
        for result in results:
            return result
        self.close()

    # existInviteId
    def existInviteId(self,inviteId):
        results = self.select_all_tasks(f"SELECT inviteId FROM invitationLimit where inviteId = \"{inviteId}\"")
        for result in results:
            if result[0] == inviteId:
                return True
        return False
    
    # updateBeInvited
    def updateBeInvited(self,inviteId,data):
        results = self.select_all_tasks(f"SELECT beInvited FROM invitationLimit where inviteId = \"{inviteId}\"")
        for result in results:
            JSON_data=json.loads(result[0])
        print(JSON_data)

        for key,value in json.loads(data[0]['beInvited']).items():
            JSON_data[key] = value
        print(JSON_data)
        print(json.dumps(JSON_data))
        sql = f"UPDATE invitationLimit SET beInvited = ? WHERE inviteId = '{inviteId}'" 
        print("sql="+sql)
        self.cursor.execute(sql, (str(json.dumps(JSON_data))),)