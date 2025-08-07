import pandas as pd

def load_and_filter_data(csv_path, station_name):
    df = pd.read_csv(csv_path)
    return df[df["station"] == station_name]

def save_filtered_csv(df, out_path="filtered.csv"):
    df.to_csv(out_path, index=False)

def get_date_range(df):
    return df["DateTime"].min(), df["DateTime"].max()
