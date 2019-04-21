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
        return Search()  # .search_inverted(words)

    def positionIndex(self)->Dict:
        """
            using inverted zone index of each word
        """
        return PSearch()  # .search_position(words)

    def titleFreqIndex(self, words: List[str])->Dict:
        """
            return the title index
        """
        return None

    def titlePostIndex(self, words: List[str])->Dict:
        """
            return the title index
        """
        return None

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
        # print(words)
        wordidx = self.wordIndex()
        index2docs['freq-script'] = wordidx.search_script(words)
        index2docs['freq-plot'] = wordidx.search_inverted(words)
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
