import pymongo


class PSearch():
    """
    combine search_position_script() from search_position_script.py
    """

    def search_position(self, query):
        results = {}
        client = pymongo.MongoClient(
            "mongodb+srv://jack:jackmongodb@cluster0-uagde.mongodb.net")
        db = client['IMDBData']
        collection = db['Movies_1']
        for word in query:
            query = {word: {"$exists": True}}
            cursor = collection.find(query, {"_id": 0})
            for i in cursor:
                results.update(i)
            return results

    def search_position_script(self, query):
        results = {}
        client = pymongo.MongoClient(
            "mongodb+srv://jack:jackmongodb@cluster0-uagde.mongodb.net")
        #client = pymongo.MongoClient("mongodb://jack:jackmongodb@cluster0-shard-00-00-uagde.mongodb.net:27017,cluster0-shard-00-01-uagde.mongodb.net:27017,cluster0-shard-00-02-uagde.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
        db = client['IMDBData']
        collection = db['Movie_5']

        # cursor = db.collection.find(query, {"_id": 0})
        for word in query:
            # each_word = stems[0]
            query = {word: {"$exists": True}}
            cursor = collection.find(query, {"_id": 0})

            for i in cursor:
                results.update(i)

            return results


def main(args):
    index = PSearch()
    query = ["man"]
    results = index.search_position(query)

    print(results)


if __name__ == "__main__":
    import sys

    main(sys.argv)
