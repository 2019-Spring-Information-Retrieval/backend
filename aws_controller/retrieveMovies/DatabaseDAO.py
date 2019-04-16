import pymongo
import bson.json_util
import pprint
from bson import ObjectId

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

    def getTopRated(self, num, minVote):
        return bson.json_util.dumps(self.cacheDb['Movies'].find({"imdbRating": {"$lt": 10.1}, "imdbVotes": {"$gt": int(minVote)}}).sort([("imdbRating", -1), ("imdbVotes", -1)]).limit(int(num)))

    def countAll(self, genre):
        return self.cacheDb['Movies'].count_documents({'Genre': {"$regex": ".*" + genre + ".*"}})

    def convert(self):
        doc = self.cacheDb['Movies'].find().limit(64960)
        count = 1
        countError = 0
        for item in doc:
            try:
                item['imdbRating']
            except KeyError:
                countError = countError + 1
                continue


            if (item['imdbRating'] == "N/A"):
                countError = countError + 1
                continue

            try:
                vote = item["imdbVotes"].replace(",", "")
            except:
                countError = countError + 1
                continue
            if (item['imdbVotes'] == "N/A"):
                countError = countError + 1
                continue

            print(count)
            count = count + 1
            print((item['_id']))
            print((item['Title']))
            print("------------")
            self.cacheDb['Movies'].update_one({"_id": item["_id"]},
                                              {"$set":
                                                   {"imdbRating": float(item['imdbRating']),
                                                    "imdbVotes": int(vote)}},
                                              upsert = False)
    def check(self):
        return self.cacheDb['Movies'].find({"_id": ObjectId("5c97cf1112c54d2abe3dca49")})
        # return self.cacheDb['Movies'].find({"_id": { "$lt" : ObjectId("5c97fac912c54d2e52ab7f37")}}).count()

dao = DatabaseDAO()

dao.connectToDatabase()


# dao.convert()
# pprint.pprint(bson.json_util.dumps(dao.check()))

# print(dao.getOneMovie("Albela"))
# print(dao.getMovieFromTo(1,5))
pprint.pprint(dao.getMovieFromTo("Drama",1,5))

# pprint.pprint(dao.getTopRated(10, 2000))


## First convert
# 5c97f29812c54d2e52ab3a08
# Hanging Perverts
# 64960

## Second convert
# 5c97fac912c54d2e52ab800c
# A Painting Lesson
# ------------
# 5c97fac912c54d2e52ab7f29
# Gearheads
# ------------
# 5c97fac912c54d2e52ab7f2d
# Inkaar
# ------------
# 5c97fac912c54d2e52ab7f37
# On the Verge
# ------------
# 5c97fac912c54d2e52ab7f91
# The City of Children
# ------------
#82673

## Third convert
# ------------
# 114018
# 5c982a3b12c54d2e52ad5940
# Kaos
# ------------
# 114019
# 5c982a3b12c54d2e52ad59ec
# Deadly Match
# ------------
# 114020
# 5c982a3b12c54d2e52ad585f
# Devadas
# ------------
# 114021
# 5c982a3b12c54d2e52ad597a
# Tropykaos
# ------------