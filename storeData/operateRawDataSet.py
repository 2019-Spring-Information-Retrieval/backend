import pandas as pd

df = pd.read_csv("title.basics.csv", na_values=[r'\N'])
df1= df.loc[df['titleType'] == "movie"]

df1 = df1[['tconst', 'titleType', 'startYear']]

s = pd.Series(df1.startYear)
s.replace(r"\N", "0")

df1 = df1[df1.startYear >= 2000]
df1 = df1[df1.startYear <= 2021]

print(df1.describe())
print(df1)

df1.to_csv("moviesData.csv", index=False)







