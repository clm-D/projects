
import pymysql


class MyMySql(object):
    def __init__(self, dbname):
        self.host = 'localhost'
        self.part = 3306
        self.user = 'root'
        self.password = '1234'
        self.dbname = dbname
        self.charset = 'utf8'
        # 连接数据库
        self.connect()

    def connect(self):
        # 连接数据库和获取游标
        self.db = pymysql.connect(host=self.host, port=self.part, user=self.user,
                                  password=self.password, db=self.dbname, charset=self.charset)
        self.cursor = self.db.cursor()

    def run(self, sql):
        ret = None
        try:
            ret = self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
        finally:
            return ret

    def close(self):
        self.cursor.close()
        self.db.close()

    def insert(self, sql):
        return self.run(sql)

    def update(self, sql):
        return self.run(sql)

    def delete(self, sql):
        return self.run(sql)

    def search(self, sql):
        ret = None
        try:
            ret = self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
        finally:
            return ret

    def read_one(self, sql):
        ret = None
        try:
            self.cursor.execute(sql)
            # 获取得到数据
            ret = self.cursor.fetchone()
        except Exception as e:
            print('查询失败')
        finally:
            self.close()
        return ret

    def read_many(self, sql):
        ret = None
        try:
            self.cursor.execute(sql)
            # 获取得到数据
            ret = self.cursor.fetchall()
        except Exception as e:
            print('查询失败')
        finally:
            self.close()
        return ret