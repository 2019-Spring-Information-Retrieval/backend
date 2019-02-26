from collection import defualtdict
from typing import List, Dict
from preprocess import Processor


class QueryWorker(object):
    """docstring for QueryWorker
        USAGE:
        from mongodbWorker import MongodbWorker
        mworker = MongodbWorker()

        qworker = QueryWorker(mworker)
        qworker.input(query)
        index2docs = qworker.output()

        -> index2docs is what you need
    """

    def __init__(self, mongodbworker):
        self.mworker = mongodbworker
        self.query = ""
        self.pworker = Processor()

    def input(self, query):
        """
            accept input
        """
        self.query = query
        
    '''
    def preprocess(self)-> List[str]:
        """
            preprocess the query, clean, remove stopwords or not
        """
        words = self.query.split()
        return words
    '''

    def wordIndex(self, words: List[str])->Dict:
        """
            using inverted file index of each word
        """
        words2docs = defualtdict(list)
        for wd in words:
            words2docs[wd] = self.mworker.search_index('word', wd)

        return words2docs

    def zoneIndex(self, words: List[str])->Dict:
        """
            using inverted zone index of each word
        """
        zone2docs = defualtdict(list)
        for wd in words:
            zone2docs[wd] = self.mworker.search_index('zone', wd)

        return zone2docs

    def output(self)->Dict:
        """
            return the doc ids for querying
        """
        index2docs = {}
        words = self.pworker(self.query)

        index2docs['word'] = self.wordIndex(words)
        #index2docs['zone'] = self.zoneIndex(words)
        #index2docs['position'] = self.positionIndex(words)
        # ...

        return index2docs
