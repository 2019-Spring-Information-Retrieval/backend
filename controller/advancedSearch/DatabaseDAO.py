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

dao = DatabaseDAO()

dao.connectToDatabase()


# print(dao.getOneMovie("Albela"))
# print(dao.getMovieFromTo(1,5))
# print(dao.getMovieFromTo("Drama",1,5))
# pprint.pprint(dao.getTopRated(10))

