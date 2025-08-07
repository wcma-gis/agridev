import pandas as pd

base_csv_path = "../more_data/all.csv"
df = pd.read_csv(base_csv_path)
df = df[df["station"] == "Clearlake"]
print(len(df))