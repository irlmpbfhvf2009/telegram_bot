
import sqlite3
 
'''
sqlite3数据操作简易封装
'''
class DBHP():
 
    def __init__(self,db_name=None):
        self.conn = sqlite3.connect(db_name if db_name else 'CattleSpider.db')
        self.cursor = self.conn.cursor()
 
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
            print("创建表出错，错误信息：",str(ex))
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
    def query_data(self,sql:str)->list:
        try:
            self.conn.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as ex:
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
 
data=[
    {"name":"张三","age":"23"},
    {"name":"张三","age":"23"},
    {"name":"张三","age":"23"}
]

db=DBHP(db_name="telegram-bot.db")
db.create_tables("tudi_2011",['正文标题', '公告编号', '发布时间', '行政区', '获取出让文件开始时间', '获取出让文件截止时间', '获取出让文件地点', '提交书面申请开始时间', '提交书面申请截止时间', '提交书面申请地点', '保证金截止时间', '确认投标或竞买资格时间', '土地使用权挂牌活动地址', '地块名称', '各地块挂牌时间', '宗地编号', '宗地总面积', '宗地坐落', '出让年限', '容积率', '建筑密度', '绿化率', '建筑限高', '主要用途', '投资强度', '保证金', '估价报告备案号', '起始价', '加价幅度', '挂牌开始时间', '挂牌截止时间', '明细用途', '联系地址', '联系人', '联系电话', '开户单位', '开户银行', '开户账号', '类型', '土地使用权拍卖时间', '土地使用权拍卖地址', '投标保证金截止时间', '土地使用权招标开始时间', '土地使用权招标截止时间', '土地使用权招标地址', '土地使用权开标时间', '土地使用权开标地址'])
db.insert_data("stu",data)
for item in db.query_data("select * from stu"):
    print(item)
db.close()