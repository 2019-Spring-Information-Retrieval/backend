from typing import List
from pymongo import MongoClient

'''
words_coltion = db.words = db['words']
zones_coltion = db.zones
position_coltion = db.position
'''

LOCAL_URL = "mongodb+srv://jack:jackmongodb@cluster0-uagde.mongodb.net"

COLLECTIONS = {'freq-reverse': 'Movies'}


class MongodbWorker(object):
    """docstring for MongodbWorker
        USAGE:
        # search
        from mongodbWorker import MongodbWorker
        mworker = MongodbWorker()
        resultDict = mworker.search_index('word', ['lady','bird'])

        # insert
        result = mworker.insert('word',[{'key':'lady','doc1':3,'doc2':10},{'key':'bird','doc1':1,'doc3':100}]) 
        if result is False:
            print('fail!')
        else:
            print('success!')
    """

    def __init__(self, url=LOCAL_URL):
        self.db = MongoClient(url)['IMDBData'].Movies

    def _getCollection(self, collection):
        """
        """
        # if the assgined collection exists or not
        if collection not in COLLECTIONS.keys():
            print('name of collection is wrong!')
            return False
        else:
            # get the collection
            return self.db[collection]

    def search_index(self, coltion: str, terms: List, regrex: bool=False, advRegrex: bool=None):
        """
            Now this search function only fit word_index 
        """
        result = {}

        # get collection
        c = self._getCollection(coltion)
        if c is False:
            return result

        # LIKE function
        if regrex is True:
            if advRegrex is not None:
                if advRegrex is True:
                    def _regrex(word): return '/^' + word + '$/'
                else:
                    def _regrex(word): return '/^' + word + '/'
            else:
                def _regrex(word): return '/^' + word + '$/'
            terms = [_regrex(t) for t in terms]

        # get data
        result = {t: c.find_many(t) for t in terms}

        return result

    def insert(self, collection: str, doc: List):
        """
            this insert support inserting data under every situation
        """
        # get collection
        c = self._getCollection(collection)
        if c is False:
            return False

        # insert many
        if type(doc) == list:
            c.insert_many(doc)
        else:
            print('type of doc(s) is wrong!')
            return False

        return True
