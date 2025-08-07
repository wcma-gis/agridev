import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]
assistant_id = st.secrets["ASSISTANT_ID"]


station_name = "Dooen 2"

base_csv_path = "more_data/all.csv"
filtered_csv = "more_data/filtered.csv"
station_csv_path = "more_data/portal_site_list.csv"