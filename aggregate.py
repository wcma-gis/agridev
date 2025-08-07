import os
import pandas as pd

all_data = []
for station in os.listdir("data"):
    station_path = os.path.join("data", station)
    file_path = os.path.join(station_path, "sensor-data.csv")
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        df["station"] = station
        all_data.append(df)

if all_data:
    pd.concat(all_data).to_csv("all.csv", index=False)
