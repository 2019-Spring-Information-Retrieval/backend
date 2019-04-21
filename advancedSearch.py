import queryWorker
# import mongodbWorker
import rankWorker
import pprint

import bson.json_util


def advancedSearch(query: str, limit: int=None):
    q = queryWorker.QueryWorker()
    words, index2docs = q.output(query)
    #m = mongodbWorker.MongodbWorker()
    r = rankWorker.RankWorker()
    r.input(words, index2docs, limit)
    docs = r.output()

    return docs

# print(advancedSearch("the"))
pprint.pprint(advancedSearch("spiderman spider"))
pprint.pprint(advancedSearch("spiderman spider", 20))
