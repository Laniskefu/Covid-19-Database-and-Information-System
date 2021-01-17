import pymysql
import datetime

class Database:
    def __init__(self, h=None, u=None, k=None, p=None):
        #self.db = pymysql.connect("localhost", "root", "", "world_v2")
        self.db = pymysql.connect(host="114.116.228.13",user="Ubuntu",password="123456",database="world_v2", port=3306)
        self.cursor = self.db.cursor()

    def prepare(self, sql):
        return self.cursor.execute(sql)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def update(self):
        self.db.commit()

    def close(self):
        self.db.close()

if __name__=="__main__":
    world = Database()
    print(world.prepare('truncate table data'))
    print(world.update())
    world.close()


