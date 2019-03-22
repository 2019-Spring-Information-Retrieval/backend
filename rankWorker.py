from typing import List, Dict

INDEX_IDS = ['']
# Tfidf 应该是一个类，因为可能会需要ground fact 统计

from const import LIMIT_DOCS
tfidf = TfidfTransformer()


def getFinalScore(scores: List[float], names: List[str]=None):
    return sum(scores)


class RankWorker(object):
    """docstring for RankWorker
        USAGE:
        from mongodbWorker import MongodbWorker
        mworker = MongodbWorker()

        rworker = RankWorker(mworker)
        rworker.input(qwords,index2docs)
        docs = rworker.output()
    """

    def __init__(self, mongodbworker):
        self.mworker = mongodbworker
        self.index2docs = {}  # indextype : {word:{docid:freq}}
        self.doc2vecs = {}  # indextype : {doc: feature matrix}
        self.docs2score = {}
        self.ix_to_doc = {}
        self.doc_to_ix = {}
        self.word_to_ix = {}

    def input(self, qwords: List, index2docs: Dict):
        '''

        '''
        self.index2docs = index2docs
        self.word_to_ix = {w: ix for ix, w in enumerate(self.qwords)}

    def precheck(self)->bool:
        """
            whether the index2docs is larger than 0
        """
        return len(self.index2docs) > 0

    def docs2feature(self):
        """

        """
        # 统计所有出现过的文档
        for idx in INDEX_IDS:
            for wd in self.index2docs[idx].keys():  # for every query word
                for d in oneIndex[wd].keys():  # for every doc id
                    if d not in self.doc_to_ix:
                        self.doc_to_ix[len(doc_to_ix)] = d
        # 反向索引
        self.ix_to_doc = {ix: doc for doc, ix in self.doc_to_ix.items()}

        # 建立每个索引下的 文档-词汇频率 矩阵
        for idx in INDEX_IDS:
            # 建立文档-词汇频率 矩阵
            doc2wordfreq = np.zeros(
                (len(self.doc_to_ix), len(self.word_to_ix)))
            for wd, docDict in self.index2docs[idx].items():
                for did, freq in docDict.items():
                    x = doc_to_ix[did]
                    y = word_to_ix[wd]
                    doc2wordfreq[x, y] = freq
            self.doc2vecs[idx] = doc2wordfreq

    def ranking(self)->List:
        """ The core of this class!
            0. 将检索结果转化成特征向量
            1. 计算不同特征的得分
            2. 计算加权和
            3. 排序
        """
        # 0. 初始化
        # 获得每个index下的doc vector用于计算
        self.docs2feature()
        # 文档-分数 字典
        docs2score = defaultdict(list)

        # 1. 计算得分
        # 1.1 计算频率上的得分
        if 'freq-reverse' in INDEX_IDS:

            tfidfmat = tfidf.fit_transform(self.doc2vecs[index])
            for ix, vec in enumerate(tfidfmat):
                score = np.sum(vec) / np.square(vec).sum()
                docs2score[self.ix_to_doc[ix]].append(score)

        # 1.2 计算不同位置上的得分？
        # ...

        # 2. 合计总分
        scoring = []
        ranking = []
        for doc, scores in docs2score:
            ranking.append(doc)
            scoring.append(getFinalScore(scores))

        # 3. 根据总分排序
        inds = np.argsort(scoring)
        ranking = ranking[inds]

        return ranking

    def getDocs(self, docIDs: List)->List:
        """
            get the original docs from database
            docsIDs: the docs id that need to obtain from database
        """
        # 是否限制最大检索数量
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
        # 检查输入是否合理
        if self.precheck() is False:
            return docs
        # 排序
        docIDs = self.ranking()
        # 获得对应文档
        docs = self.getDocs(docIDs)

        return docs
