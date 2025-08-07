import pandas as pd

base_csv_path = "all.csv"
df = pd.read_csv(base_csv_path)
df = df[df["station"] == "Dooen 2"]
df.to_csv("all_small.csv", index=False)