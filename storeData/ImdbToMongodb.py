import requests
import pymongo
import pandas as pd

# key: fe53f97e


class ImdbToMongoDB:
    def __init__(self, key):
        self.url = "http://www.omdbapi.com/?apikey=" + key + "&i="
        self.client = pymongo.MongoClient("mongodb+srv://jack:jackmongodb@cluster0-uagde.mongodb.net")

    def readMovieFile(self, num):
        df = pd.read_csv("movieFragments/movieData" + str(num) + ".csv")
        return df['tconst'].values.tolist()

    def imdbAPI(self, id):
        return requests.get(self.url + id + "&plot=full").json()

    def sendToMongoDB(self):
        db = self.client['IMDBData']
        collection = db['Movies']

        for i in range(35000, 207581, 5000):
            print("------------------------------------")
            print("I am sending the movieData" + str(i) + ".csv file")
            movieIDList = self.readMovieFile(i)
            count = 0
            movies = []
            for id in movieIDList:
                try:
                    movie = self.imdbAPI(id)
                    movies.append(movie)
                    if count % 1000 == 0:
                        print(count)
                    count = count + 1
                except:
                    print("This id:" + id + " results problem.")

            collection.insert_many(movies)


# test = ImdbToMongoDB(key)
# test.sendToMongoDB()