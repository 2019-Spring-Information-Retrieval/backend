from typing import List

TOPN = 300


class RankWorker(object):
    """docstring for RankWorker
        USAGE:
        from mongodbWorker import MongodbWorker
        mworker = MongodbWorker()

        rworker = RankWorker(mworker)
        rworker.input(index2docs)
        docs = rworker.output()
    """

    def __init__(self, mongodbworker, limitOrNot: bool=False):
        self.mworker = mongodbworker
        self.limit = limitOrNot
        self.index2docs = {}

    def input(self, index2docs:Dict):
        self.index2docs = index2docs

    def precheck(self)->bool:
        """
            whether the index2docs is larger than 0
        """
        flag = False
        if len(self.index2docs) > 0:
            flag = True
        return flag

    def ranking(self)->List:
        """ The core of this class!
            different docs from different types of index, 
            combine them and calculate the order.

            using self.index2docs here
        """
        docIDs = []
        # e.g., doc contain every term should always order first

        # e.g., consider term in title first, then overview, then review

        # e.g., the last the movie, the first the order

        # ...

        return docIDs

    def getDocs(self, docIDs: List)->List:
        """
            get the original docs from database
        """
        if self.limit is True:
            docIDs = docIDs[:TOPN]

        docs = [self.mworker.search('doc', did) for did in docIDs]

        return docs

    def output(self)->List:
        """
            return the original docs 
        """
        docs = []

        if self.precheck() is False:
            return docs

        docIDs = self.ranking()

        docs = self.getDocs(docIDs)

        return docs
