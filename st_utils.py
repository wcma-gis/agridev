import streamlit as st
import base_ulits
import config

def print_assistant_status():
    all_assistants = set(config.assistant_pool.values())
    used = set(st.session_state.get("used_assistants", []))
    free = all_assistants - used

    print("🟢 Free assistants:", len(list(free)), list(free))
    print("🔴 Used assistants:", len(list(used)), list(used))

def allocate_assistant():
    for name, aid in config.assistant_pool.items():
        used = st.session_state.get("used_assistants", [])
        if aid not in used:
            print(f"Allocated: {aid}")
            st.session_state.used_assistants = used + [aid]
            print_assistant_status()
            return aid
    return None

def free_assistant():
    if "assistant_id" in st.session_state and "used_assistants" in st.session_state:
        st.session_state.used_assistants = [
            aid for aid in st.session_state.used_assistants
            if aid != st.session_state.assistant_id
        ]
        print(f"Free: {st.session_state.assistant_id}")
        del st.session_state.assistant_id
        print_assistant_status()

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
        free_assistant()
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
