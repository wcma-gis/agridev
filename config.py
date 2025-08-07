import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]
assistant_id = st.secrets["ASSISTANT_ID"]

csv_path = "all_small.csv"
station_name = "Dooen 2"

filtered_csv = "more_data/filtered.csv"