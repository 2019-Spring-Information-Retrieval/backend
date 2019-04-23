from typing import List, Dict
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from collections import defaultdict
from functools import reduce
from pymongo import MongoClient

np.set_printoptions(precision=5)


def getFinalScore(scores: List[float], names: List[str]=None):
    weights = {'freq-plot': 0.79, 'freq-script': 0.63,
               'freq-title': 0.88, 'post-script': 0.63, 'post-plot': 0.51}

    cur_weight = [weights[n] for n in names]
    new_weight = [w / sum(cur_weight) for w in cur_weight]

    results = 0
    for ix, score in enumerate(scores):
        results += new_weight[ix] * score
    return results


class RankWorker(object):
    """docstring for RankWorker
    """

    def __init__(self):
        self.index2docs = {}  # indextype : {word:{docid:freq}}
        self.doc2vecs = {}  # indextype : {doc: feature matrix}
        self.docs2score = {}
        self.ix_to_doc = {}
        self.doc_to_ix = {}
        self.word_to_ix = {}
        self.qwords = []
        self.index_ids = None
        self.limit_docs = None

    def input(self, qwords: List, index2docs: Dict, limit: int=None):
        """
        """
        # print(index2docs)
        self.index2docs = index2docs
        self.qwords = qwords
        self.index_ids = list(index2docs.keys())
        if limit is not None:
            self.limit_docs = limit

    def precheck(self)->bool:
        """
            whether the index2docs is larger than 0
        """
        flag = True
        self.word2index()
        self.docs2index()

        if len(self.index2docs) <= 0:
            flag = False
        elif len(self.qwords) == 0:
            flag = False
        elif max([len(self.index2docs[idx]) for idx in self.index_ids]) == 0:
            flag = False
        elif len(self.word_to_ix) == 0:
            flag = False
        elif len(self.doc_to_ix) == 0:
            flag = False

        return flag

    def word2index(self):
        for w in self.qwords:
            if w not in self.word_to_ix:
                self.word_to_ix[w] = len(self.word_to_ix)

    def docs2index(self):
        """
        """
        # 统计所有出现过的文档
        for idx in self.index_ids:
            for wd in self.word_to_ix.keys():  # for every query word
                if wd not in self.index2docs[idx]:
                    continue
                for d in self.index2docs[idx][wd].keys():  # for every doc id
                    if d not in self.doc_to_ix:
                        self.doc_to_ix[d] = len(self.doc_to_ix)
        # 反向索引
        self.ix_to_doc = {ix: doc for doc, ix in self.doc_to_ix.items()}

    def docs2feature(self, index: str):
        """

        """
        # 建立倒排索引下的 文档-词汇频率 矩阵
        doc2wordfreq = [[0] * len(self.word_to_ix)
                        for _ in range(len(self.doc_to_ix))]
        for wd, docDict in self.index2docs[index].items():
            for did, freq in docDict.items():
                x = self.doc_to_ix[did]
                y = self.word_to_ix[wd]
                doc2wordfreq[x][y] = freq
        self.doc2vecs[index] = doc2wordfreq

    def docs2position(self, index: str):
        # 出现位置初始化为-1，当真有出现的时候，会直接覆盖出现位置的list
        word_doc_post = [[[-1] for __ in range(
            len(self.doc_to_ix))] for ___ in range(len(self.word_to_ix))]

        for wd in self.word_to_ix.keys():
            for doc in self.doc_to_ix.keys():
                if wd not in self.index2docs[index]:
                    continue
                if doc not in self.index2docs[index][wd]:
                    continue
                word_doc_post[self.word_to_ix[wd]][self.doc_to_ix[
                    doc]] = self.index2docs[index][wd][doc]
        self.doc2vecs[index] = word_doc_post

    def alignment(self, word_doc_post)->Dict:
        # N = len(self.word_to_ix)  # word
        # M = len(self.doc_to_ix)  # doc
        def comb(place1, place2, coda=' '):
            return [str(p1) + coda + str(p2) for p1 in place1 for p2 in place2]
        # 算分 这里是 直接算距离的方法
        docs_score = [0] * len(self.doc_to_ix)  # {}
        baseline = np.array([i + 1 for i in range(len(self.qwords))])  # 1 by N

        for doc in self.doc_to_ix.keys():
            j = self.doc_to_ix[doc]
            places = [word_doc_post[self.word_to_ix[w]][j]
                      for w in self.qwords]
            vectors = reduce(comb, places)  # length = H
            comb_to_plcs = np.array([list(map(int, vec.split()))
                                     for vec in vectors])  # H by N
            scores = np.dot(baseline, comb_to_plcs.T)  # 1 by H
            docs_score[j] = np.max(scores)  # softmax(scores))  # 1
        mean = sum(docs_score) / len(self.doc_to_ix)
        diff = max(docs_score) - min(docs_score)

        docs_to_score = {doc: (
            docs_score[self.doc_to_ix[doc]] - mean + 1) / (diff + 1) for doc in self.doc_to_ix.keys()}

        return docs_to_score

    def freqRanking(self, index: str):
        self.docs2feature(index)

        freqs = [0 for _ in range(len(self.doc_to_ix))]
        for ix, vals in enumerate(self.doc2vecs[index]):
            freqs[ix] = sum(vals) / len(vals)
        mean = sum(freqs) / len(freqs)
        diff = max(freqs) - min(freqs)
        scores = [(f - mean + 1) / (diff + 1) for f in freqs]

        for ix, s in enumerate(scores):
            self.docs2score[self.ix_to_doc[ix]].append(s)

    def invertRanking(self, index: str):
        self.docs2feature(index)

        tfidf = TfidfTransformer()
        tfidfmat = tfidf.fit_transform(self.doc2vecs[index])
        for ix, vec in enumerate(tfidfmat.toarray()):
            if np.square(vec).sum() != 0:
                score = np.sum(vec) / np.square(vec).sum()
            else:
                score = 0
            self.docs2score[self.ix_to_doc[ix]].append(score)

    def positionRanking(self, index: str):
        self.docs2position(index)

        docs_score = self.alignment(self.doc2vecs[index])
        for did in self.doc_to_ix:
            self.docs2score[did].append(docs_score[did])

    def ranking(self)->List:
        """ The core of this class!
            0. 将检索结果转化成特征向量
            1. 计算不同特征的得分
            2. 计算加权和
            3. 排序
        """
        # 文档-分数 字典
        self.docs2score = defaultdict(list)
        index_names = []

        if len(self.qwords) > 1:
            if 'freq-plot' in self.index_ids:
                self.invertRanking('freq-plot')
                index_names.append('freq-plot')
            if 'freq-script' in self.index_ids:
                self.invertRanking('freq-script')
                index_names.append('freq-script')
            if 'post-plot' in self.index_ids:
                self.positionRanking('post-plot')
                index_names.append('post-plot')
            if 'post-plot' in self.index_ids:
                self.positionRanking('post-script')
                index_names.append('post-script')

        else:
            if 'freq-plot' in self.index_ids:
                self.freqRanking('freq-plot')
                index_names.append('freq-plot')
            if 'freq-script' in self.index_ids:
                self.freqRanking('freq-script')
                index_names.append('freq-script')

        # 2. 合计总分
        scoring = []
        ranking = []
        for doc, scores in self.docs2score.items():
            ranking.append(doc)
            scoring.append(getFinalScore(scores, index_names))

        # 3. 根据总分排序
        inds = np.argsort(scoring)
        ranking = np.array(ranking)
        ranking = ranking[inds]

        return ranking[::-1]

    def getDocs(self, docIDs: List)->List:
        """
            get the original docs from database
            docsIDs: the docs id that need to obtain from database
        """
        # 是否限制最大检索数量
        nums = len(docIDs)
        if self.limit_docs is not None and nums > self.limit_docs:
            nums = self.limit_docs

        LOCAL_URL = "mongodb+srv://jack:jackmongodb@cluster0-uagde.mongodb.net"
        mc = MongoClient(LOCAL_URL)
        db = mc['IMDBData']
        c = db['Movies']
        docs = [c.find_one({'imdbID': docIDs[i]}) for i in range(nums)]

        return [d for d in docs if d is not None]

    def output(self)->List:
        """
            return the original docs 
        """
        docs = []
        # 1. 检查输入是否合理
        if self.precheck() is False:
            return docs

        # 2. 排序
        docIDs = self.ranking()
        # 获得对应文档
        docs = self.getDocs(docIDs)
        return docs
