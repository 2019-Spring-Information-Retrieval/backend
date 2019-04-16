import pprint

import mongodbWorker
import queryWorker
import rankWorker


def search(query: str):
    q = queryWorker.QueryWorker()
    words, index2docs = q.output(query)
    m = mongodbWorker.MongodbWorker()
    r = rankWorker.RankWorker(m)
    r.input(words, index2docs)
    docs = r.output()
    return docs


# print(advancedSearch("the"))

pprint.pprint(search("spider man"))
