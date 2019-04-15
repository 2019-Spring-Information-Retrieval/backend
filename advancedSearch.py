import queryWorker
import mongodbWorker
import rankWorker


def advancedSearch(query: str):
    q = queryWorker.QueryWorker()
    words, index2docs = q.output(query)
    m = mongodbWorker.MongodbWorker()
    r = rankWorker.RankWorker(m)
    r.input(words, index2docs)
    docs = r.output()
    print(docs)
    return docs

advancedSearch("the")
#print(advancedSearch("the"))

