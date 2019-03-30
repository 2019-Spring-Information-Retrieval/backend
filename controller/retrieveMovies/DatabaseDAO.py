import pymongo


class DatabaseDAO:
    def __init__(self):
        self.cacheDb = None

    def connectToDatabase(self):
        if self.cacheDb:
            return self.cacheDb
        client = pymongo.MongoClient("mongodb+srv://jack:jackmongodb@cluster0-uagde.mongodb.net")
        self.cacheDb = client['IMDBData']
        return self.cacheDb

    def getOneMovie(self, title):
        return self.cacheDb['Movies'].find_one({"Title": title})

    def getMovieFromTo(self, start, end):
        return self.cacheDb['Movies'].find().skip(start).limit(end)


dao = DatabaseDAO()
count = 0
# dao.connectToDatabase()
# print(dao.getOneMovie("Albela"))
# print(dao.getMovieFromTo(1,20))