import pymongo
from inverted_index import Index


class Search(Index):

    def __init__(self):
        super().__init__()

    def search_inverted(self, query):
        results = {}
        client = pymongo.MongoClient(
            "mongodb+srv://jack:jackmongodb@cluster0-uagde.mongodb.net")
        db = client['IMDBData']
        collection = db['Movies_2']

        for word in query:
            tokens = self.tokenize(word)
            stems = self.stemming(tokens)

            query = {stems[0]: {"$exists": True}}
            cursor = collection.find(query, {"_id": 0})

            for i in cursor:
                results.update(i)

        return results
    def search_script(self,query):
        results = {}

        client = pymongo.MongoClient(
            "mongodb+srv://jack:jackmongodb@cluster0-uagde.mongodb.net")
        db = client['IMDBData']
        collection = db['Movie_3']

        for word in query:
            tokens = self.tokenize(word)
            stems = self.stemming(tokens)

            query = {stems[0]: {"$exists": True}}
            cursor = collection.find(query,{"_id":0})

            for i in cursor:
                results.update(i)

        return results

    def search_title(self,query):
        results = {}

        client = pymongo.MongoClient("mongodb://jack:jackmongodb@cluster0-shard-00-00-uagde.mongodb.net:27017,cluster0-shard-00-01-uagde.mongodb.net:27017,cluster0-shard-00-02-uagde.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
        db = client['IMDBData']
        collection = db['Movies_6']

        for word in query:
            tokens = self.tokenize(word)
            stems = self.stemming(tokens)

            query = {stems[0]: {"$exists": True}}
            cursor = collection.find(query,{"_id":0})

            for i in cursor:
                results.update(i)

        return results

def main(args):
    query = ["summer"]
    results = Search().search_inverted(query)
    results1 = Search().search_script(query)
    results2 = Search().search_title(query)
    print(results2)
    # print(results)
    # print(results1)


if __name__ == "__main__":
    import sys
    main(sys.argv)
