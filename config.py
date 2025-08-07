import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]
station_name = "Dooen 2"
base_csv_path = "more_data/all.csv"
filtered_csv = "more_data/filtered.csv"
station_csv_path = "more_data/portal_site_list.csv"

raw_ids = st.secrets["ASSISTANT_ID"]
assistant_pool = {
    f"AgriDev {i}": aid.strip()
    for i, aid in enumerate(raw_ids.split(","))
}
