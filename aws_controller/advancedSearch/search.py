import queryWorker
import rankWorker
import pprint
import DatabaseDAO
import bson.json_util


def search(query: str):
    dao = DatabaseDAO.DatabaseDAO()

    q = queryWorker.QueryWorker()
    words, index2docs = q.output(dao, query)
    r = rankWorker.RankWorker(dao)
    r.input(words, index2docs)
    docs = r.output()

    return docs


print(search("the"))

# pprint.pprint(search("the"))

