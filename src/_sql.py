import sqlite3
 
'''
sqlite3数据操作简易封装
'''
class DBHP():
    def __init__(self,db_name=None):
        self.conn = sqlite3.connect(db_name if db_name else 'CattleSpider.db')
        self.cursor = self.conn.cursor()

    def tables_in_sqlite_db(self):
        self.cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [
            v[0] for v in self.cursor.fetchall()
            if v[0] != "sqlite_sequence"
        ]
        self.cursor.close()
        return tables
    '''
    创建表格
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
    插入数据，根据传入的数据类型进行判断，自动选者插入方式
    @:param table_name 表名
    @:param data 要插入的数据
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
    查询数据
    @:param 要查询的sql语句
    '''
    def select_all_tasks(self,sql:str)->list:
        try:
            self.cursor = self.conn.execute(sql)
            results = self.cursor.fetchall()
            self.cursor.fetchone()
            return results
        except:
            return []

    '''
    关闭数据库连接
    '''
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as ex:
            raise Exception("关闭数据库连接失败")

class sql:
    def __init__(self):
        self.db = DBHP(db_name="telegram-bot.db")
        self.token = self.getToken()
        self.password = self.getPassword()
        self.botusername = self.getBotName()

        # config table
        configTable = self.db.create_tables("config",['key', 'value'])
        if configTable == True:
            data=[
                {"key":"token","value":"5855785269:AAH9bvPpYudd2wSAvMnBTiKakCeoB92_Z_8"},
                {"key":"password","value":"RYANGOD"},
                {"key":"botuserName","value":"CCP1121_BOT"}
            ]
            self.db.insert_data("config",data)
        
        # show tables
    def showTables(self):
        print(self.db.tables_in_sqlite_db())

        # getToken
    def getToken(self):
        results = self.db.select_all_tasks("SELECT * FROM config WHERE key = 'token'")
        for result in results:
            return result[1]
        self.db.close()

        # getPassword
    def getPassword(self):
        results = self.db.select_all_tasks("SELECT * FROM config WHERE key = 'password'")
        for result in results:
            return result[1]
        self.db.close()

        # getBotName
    def getBotName(self):
        results = self.db.select_all_tasks("SELECT * FROM config WHERE key = 'botuserName'")
        for result in results:
            return result[1]
        self.db.close()
