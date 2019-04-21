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

    def wordIndex(self)->Dict:
        """
            using inverted file index of each word
        """
        return Search()

    def positionIndex(self)->Dict:
        """
            using inverted zone index of each word
        """
        return PSearch()

    def authorIndex(self, words: List[str])->Dict:
        """
            return the  index
        """
        return None

    def output(self, text: str)->Dict:
        """
            return the doc ids for querying
        """
        index2docs = {}
        words = Processor().do(text)
        
        wordidx = self.wordIndex()
        index2docs['freq-script'] = wordidx.search_script(words)
        index2docs['freq-plot'] = wordidx.search_inverted(words)
        index2docs['freq-title'] = wordidx.search_title(words)
        if len(words) > 1:
            postidx = self.positionIndex()
            index2docs['post-plot'] = postidx.search_position(words)
            index2docs['post-script'] = postidx.search_position_script(words)

        return words, index2docs


def main():
    query = 'spider ladygaga'
    words, index2docs = QueryWorker().output(query)
    print(index2docs)

if __name__ == '__main__':
    main()
