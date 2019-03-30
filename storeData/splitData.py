import pandas as pd

df = pd.read_csv("moviesData.csv")

lastIndex = 0
for i in range(5000, 207581, 5000):
    if i == 205000:
        tmp = df[i:]
        tmp.to_csv("movieData" + str(i) + ".csv", index=False)
        break
    tmp = df[lastIndex : i]
    tmp.to_csv("movieData" + str(i) + ".csv", index=False)
    lastIndex = i
