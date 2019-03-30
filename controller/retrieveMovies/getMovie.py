import pymongo
import json
from DBConnection import Conn



class getMovie:
    def __init__(self):
        self.conn = Conn()
        self.db = self.conn.getConn()
        self.coll = self.db['Movies']

    def get(self, title):
        return self.coll.find_one({"Title": title})

    # def get(self):
    #     return self.coll.find({}).limit(20)
test = getMovie()


# print(test.get("Kate & Leopold"))