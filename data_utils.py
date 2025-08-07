import pandas as pd
import config
import os

def load_and_filter_data(csv_path, station_name):
    df = pd.read_csv(csv_path)
    return df[df["station"] == station_name]

def save_filtered_csv(df):
    os.makedirs(os.path.dirname(config.filtered_csv), exist_ok=True)
    df.to_csv(config.filtered_csv, index=False)

def get_date_range(df):
    return df["DateTime"].min(), df["DateTime"].max()
