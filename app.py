import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import config
import uuid

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.set_page_config(
    page_icon="🤖",
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
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=8,
        color="blue",
        fill=True,
        fill_color="cyan",
        fill_opacity=0.7,
        popup=row["site"],
        tooltip=row["site"]
    ).add_to(m)

map_data = st_folium(m, width=700, height=500)

if map_data.get("last_object_clicked_popup"):
    station = map_data["last_object_clicked_popup"]
    st.session_state.selected_station = station
    st.switch_page("pages/chatbot.py")

with st.expander("🛠️ Diagnostics"):
    st.write("Session ID:", st.session_state.get("session_id"))
    st.write("Assistant ID:", st.session_state.get("assistant_id"))
    st.write("File ID:", st.session_state.get("file_id"))

    all_pool = config.assistant_pool
    used_ids = st.session_state.get("used_assistants", [])
    current_id = st.session_state.get("assistant_id")
    current_session = st.session_state.get("session_id")

    st.write("🔴 Used assistants:")
    for name, aid in all_pool.items():
        if aid in used_ids:
            label = f"{name} ({aid})"
            if aid == current_id:
                label += f" ← session {current_session}"
            st.write(label)

    free = [name for name, aid in all_pool.items() if aid not in used_ids]
    st.write("🟢 Free assistants:", free)
