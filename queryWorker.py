#from collection import defualtdict
from typing import List, Dict
from preprocess import Processor
from search_inverted import Search
from search_position import PSearch
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

    def __init__(self, mongodbworker=None):
        pass
        #self.mworker = mongodbworker
        #self.query = ""
        #self.pworker = Processor()
    '''
    def preprocess(self, query:str):
        return Processor().do(query)

    def input(self, query):
        """
            accept input
        """
        self.query = query
    '''
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
        return Search().search_inverted(words)
        #result = do(words)
        '''
        words2docs = defualtdict(list)
        for wd in words:
            words2docs[wd] = self.mworker.search_index('word', wd)
        
        return words2docs
        '''
    def positionIndex(self, words: List[str])->Dict:
        """
            using inverted zone index of each word
        """
        '''
        zone2docs = defualtdict(list)
        for wd in words:
            zone2docs[wd] = self.mworker.search_index('zone', wd)

        return zone2docs
        '''
        return PSearch().search_position(words)

    def output(self, text:str)->Dict:
        """
            return the doc ids for querying
        """
        index2docs = {}
        words = Processor().do(text)
        index2docs['freq-reverse'] = self.wordIndex(words)
        index2docs['positional'] = self.positionIndex(words)
        
        return words, index2docs
