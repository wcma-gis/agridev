import streamlit as st
from config import api_key, assistant_id, csv_path, station_name
import openai_utils
import st_utils
import chat_engine

client = openai_utils.get_client(api_key)
chat_engine.initialize_session(client, csv_path, station_name)

st_utils.render_title_and_intro(
    station_name,
    st.session_state.start_date,
    st.session_state.end_date
)

st_utils.render_chat_history()

user_input = st.chat_input("Ask your question")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    chat_engine.handle_user_input(client, assistant_id, user_input)
