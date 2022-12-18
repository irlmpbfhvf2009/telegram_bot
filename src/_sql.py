
import pymysql


class SQL:
    def __init__(self,host,user,password,db,port):
        # sql參數
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port

    def connct_db(self):#定义连接数据库的方法
        try:#try+except 捕获异常
            global db#global把db对象，设置为全局变量
            #connect方法连接数据库，实例变量作为参数传入
            db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port)
            global cursor#global把cursor方法创建游标对象对象，设置为全局变量
            cursor=db.cursor()#cursor方法创建游标对象
        except Exception as e:#连接数据库事变是会任意捕获异常
            print('数据库连接失败', e)

    def creatTable(self,sql):
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

    def select(self,sql):#定义查询方法，sql为形参，用例传递sql语句
        try:
            cursor.execute(sql)#通过游标对象，调用execute执行方法，查询sql语句
            print(cursor.fetchall())#通过游标获取，表数据内容，并打印
        except Exception as e:
            print(e)
            db.rollback()

    def update(self,sql):
        try:
            cursor.execute(sql)#通过游标执行查询语句
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

    def delete(self,sql):
        try:
            cursor.execute(sql)#通过游标执行查询语句
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

    def insert(self,sql,data):
        try:
            cursor.execute(sql, tuple(data.values()))#通过游标执行查询语句
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()