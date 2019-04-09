import pymongo

client = pymongo.MongoClient("mongodb+srv://jack:jackmongodb@cluster0-uagde.mongodb.net")
db = client['IMDBData']
collection = db['Movies_2']
movies = []
collection.insert_many(movies)