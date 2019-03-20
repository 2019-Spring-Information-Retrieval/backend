from typing import List, Dict

INDEX_IDS = ['']
# Tfidf 应该是一个类，因为可能会需要ground fact 统计
from score import Tfidf
from const import LIMIT_DOCS


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
        self.index2docs = {}  # indextype : {word:{docid:freq}}
        self.doc2vecs = {}  # indextype : {doc: feature vector}
        self.docs2score = {}

    def input(self, input: Dict):
        self.index2docs = input

    def precheck(self)->bool:
        """
            whether the index2docs is larger than 0
        """
        flag = False
        if len(self.index2docs) > 0:
            flag = True
        return flag

    def docs2feature(self):

        qwords = {w: ix for ix, w in enumerate(
            list(self.index2docs[INDEX_IDS[0]].keys()))}
        _word2vec = [0 for _ in range(len(qwords))]

        for idx in INDEX_IDS:
            # 每个doc的词语向量
            docDict = {}
            for wd in self.index2docs[idx].keys():
                docs = set(oneIndex[wd].keys())
                for d in docs:
                    if d not in docDict:
                        docDict[d] = deepcopy(_word2vec)
                    docDict[d][qwords[wd]] += 1
            self.doc2vecs[idx] = docDict

    def ranking(self, )->List:
        """ The core of this class!
            different docs from different types of index, 
            combine them and calculate the order.

            using self.index2docs here
        """
        # 0. 获得每个index下的doc vector用于计算
        self.docs2feature()

        # 1. 计算单项分数
        self.docs2score = defaultdict(list)
        for index in:
            for doc in self.[index]:
                score =
                [doc].append(score)

        # 2. 计算总分
        scores = []  # np.array
        ranks = []  # np.array

        inds = np.argsort(scores)
        ranks = ranks[inds]

        return docIDs

    def getDocs(self, docIDs: List)->List:
        """
            get the original docs from database
            docsIDs: the docs id that need to obtain from database
        """
        if LIMIT_DOC:
            nums = LIMIT_DOC
        else:
            nums = len(docIDs)
        docs = [self.mworker.search('doc', docIDs[i]) for i in range(nums)]

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
