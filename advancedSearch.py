import queryWorker
import mongodbWorker
import rankWorker
import bson.json_util


def advancedSearch(query: str):
    q = queryWorker.QueryWorker()
    words, index2docs = q.output(query)
    m = mongodbWorker.MongodbWorker()
    r = rankWorker.RankWorker(m)
    r.input(words, index2docs)
    docs = r.output()
    return docs


print(bson.json_util.dumps(advancedSearch("the")))

