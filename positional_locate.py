#_*_coding= utf-8
import pickle

def read():
    picklefile = open('movie_to_story.pickle','rb')

    data = pickle.load(picklefile,encoding='iso-8859-1')
    return data


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

        result=[]
        lineText=""
        for text in movie["plot"]:
            lineText = "%s %s"%(lineText,text)
        list=location_index(str,lineText)
        if len(list)>0:
            result.append(list)
        if len(result)>0:
            movie_dic[docid]=result

    result_dic[str] =  movie_dic
    print(result_dic)


def location_index(str,text):
    result=""
    text.replace('"','').replace("\n","").replace("\r","").replace("\r\n","")
    lists = text.split()
    #print(lists)
    for i in range(len(lists)):
        data = lists[i]
        if data==str :
            if len(result)==0:
                result="%s"%(i)
            else:
                result="%s,%s"%(result,i)
    return result




if __name__ == '__main__':
    #location('Princesses')
    #location('the')
    location_mul(['man','the'])
