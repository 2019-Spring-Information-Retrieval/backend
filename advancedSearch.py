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
<<<<<<< HEAD

advancedSearch("a spider bite a man")

#print(advancedSearch("the"))
=======
print(advancedSearch("the"))

>>>>>>> 292308d6d798a1dbc54e6548a7a2221c1787fd94
