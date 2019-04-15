import pymongo
from inverted_index import Index
import bson.json_util

class Search(Index):
    def __init__(self):
        super().__init__()

    def search_inverted(self,query):
        results = {}

        client = pymongo.MongoClient("mongodb+srv://jack:jackmongodb@cluster0-uagde.mongodb.net")
        db = client['IMDBData']
        collection = db['Movies_2']
        print(collection.count())
        return
        for word in query:
            tokens = self.tokenize(word)
            stems = self.stemming(tokens)

            query = {stems[0]: {"$exists": True}}
            cursor = collection.find(query,{"_id":0})

            for i in cursor:
                results.update(i)

        return results

def main(args):
    search = Search()
    query = ["man","whale"]
    results = search.search_inverted(query)

    # print(results)


if __name__ == "__main__":
    import sys

    main(sys.argv)
