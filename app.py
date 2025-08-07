import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import config

st.set_page_config(
    page_title="AgriBot - Home",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

st.title("Select a Station")

df = pd.read_csv(config.station_csv_path)

center_lat = df["lat"].mean()
center_lon = df["lon"].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

for _, row in df.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        icon=folium.DivIcon(html=f"""<div style="font-size: 10pt">{row["site"]}</div>"""),
        popup=row["site"]
    ).add_to(m)

map_data = st_folium(m, width=700, height=500)

if map_data.get("last_object_clicked_popup"):
    station = map_data["last_object_clicked_popup"]
    st.session_state.selected_station = station
    st.switch_page("pages/chatbot.py")

