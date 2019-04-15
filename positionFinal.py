#_*_coding= utf-8
import pickle
import pymongo
import pandas as pd

def location_mul(list):
    for lst in list:
        location(lst)
def location(str):
    lines=[]
    data = read()
    movie_dic={}
    result_dic={}
    for movie_id in data:
        index = movie_id
        movie = data[movie_id]
        #print(index)
        docid = index
        #print(docid)
        #print(movie)
        lineText=""
        for text in movie["plot"]:
            lineText = "%s %s"%(lineText,text)
        list=location_index(str,lineText)
        if len(list)>0:
            movie_dic[docid]=list

    result_dic[str] =  movie_dic
    print(result_dic)


def location_index(str,text):
    result=[]
    text.replace('"','').replace("\n","").replace("\r","").replace("\r\n","")
    lists = text.split()
    #print(lists)
    for i in range(len(lists)):
        data = lists[i]
        if data==str :
            result.append(i)
            #if len(result)==0:
            #    result="%s"%(i)
            #else:
             #   result="%s,%s"%(result,i)
    return result


#class positional_search(object):
client = pymongo.MongoClient(
            "mongodb://jack:jackmongodb@cluster0-shard-00-00-uagde.mongodb.net:27017,cluster0-shard-00-01-uagde.mongodb.net:27017,cluster0-shard-00-02-uagde.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
db = client['IMDBData']
collection = db['Movies_1']

    #delf search(self,query):
query = {result_dic[0]: {"$exists": True}}
cursor = collection.Movies_1.find(query)

db.collection.find()

#if __name__ == '__main__':
    #location('Princesses')
    #location('the')
    #location_mul(['tattoo','girl'])
