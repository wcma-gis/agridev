import streamlit as st

def render_title_and_intro(station_name, start_date, end_date):
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
