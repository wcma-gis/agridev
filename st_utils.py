import streamlit as st
import base_ulits

def render_title_and_intro(station_name, start_date, end_date):
    st.set_page_config(
        page_icon="🤖",
        page_title=f"AgriBot - {station_name}",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    start_date = base_ulits.to_readable_date(start_date)
    end_date = base_ulits.to_readable_date(end_date)
    if st.button("← Select another station"):
        st.switch_page("app.py")
    st.title(f"AgriBot — Station: {station_name}")
    if not st.session_state.chat_history:
        st.markdown(
            f"Hi, I am your AgriBot. I have the station data for the period "
            f"**{start_date}** to **{end_date}**. "
            f"Ask me any question based on that."
        )

def render_chat_history():
    for entry in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(entry["user"])
        with st.chat_message("assistant"):
            st.markdown(entry["assistant"])
            if entry.get("image"):
                st.image(entry["image"])

def render_loading():
    return st.empty()

def render_assistant_response(reply_text, image_data):
    with st.chat_message("assistant"):
        if image_data:
            st.image(image_data)
        st.markdown(reply_text)

def init_st():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        button[kind="header"] {display: none;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
