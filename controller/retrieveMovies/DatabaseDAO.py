import pymongo
import bson.json_util
import pprint

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

    def getManyMovies(self, query, number):
        if self.cacheDb['Movies'].count_documents({'Title': {"$regex": '^' + query , '$options':'i'}}) < int(number):
            return bson.json_util.dumps(self.cacheDb['Movies'].find({'Title': {"$regex": '^' + query, '$options':'i' }}))
        return bson.json_util.dumps(self.cacheDb['Movies'].find({'Title': {"$regex": '^' + query, '$options':'i'}}).limit(int(number)))

    def getMovieFromTo(self, genre, start, end):
        return bson.json_util.dumps(self.cacheDb['Movies'].find({'Genre': {"$regex": ".*" + genre + ".*"}}).skip(int(start)).limit(int(end)))

    def getTopRated(self, num):
        return bson.json_util.dumps(self.cacheDb['Movies'].find({"imdbRating": {"$lt": 10.0}}).sort([("imdbRating", -1), ("imdbVotes", -1)]).limit(int(num)))

    def countAll(self, genre):
        return self.cacheDb['Movies'].count_documents({'Genre': {"$regex": ".*" + genre + ".*"}})

    def convert(self):
        self.cacheDb['Movies'].find_one()

dao = DatabaseDAO()

dao.connectToDatabase()



# print(dao.getOneMovie("Albela"))
# print(dao.getMovieFromTo(1,5))
# print(dao.getMovieFromTo("Drama",1,5))
# pprint.pprint(dao.getTopRated(10))


