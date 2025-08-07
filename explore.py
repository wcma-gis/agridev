import pandas as pd


df = pd.read_csv("all.csv")
cols = df.columns

print("\n".join([c for c in cols]))

station = "Dooen 2"
df = pd.read_csv("all.csv")
df = df[df["station"] == station]
print(len(df))

first_date = df["DateTime"].min()
last_date = df["DateTime"].max()

print(first_date)
print(last_date)
