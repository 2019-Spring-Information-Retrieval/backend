import queryWorker
import mongodbWorker
import rankWorker


def advancedSearch(query:str):
	q = queryWorker.QueryWorker()
	words, index2docs = q.output(query)
	m = mongodbWorker()
	r = rankWorker.RankWorker(m)
	r.input(qwords, index2docs)
    docs = r.output()
    return docs