import queryWorker
import mongodbWorker
import rankWorker
import pprint

import bson.json_util


def advancedSearch(query: str):
    q = queryWorker.QueryWorker()
    words, index2docs = q.output(query)
    m = mongodbWorker.MongodbWorker()
    r = rankWorker.RankWorker(m)
    r.input(words, index2docs)
    docs = r.output()


    return docs




#print(advancedSearch("the"))

pprint.pprint(advancedSearch("man, a"))

