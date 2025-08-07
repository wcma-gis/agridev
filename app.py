import streamlit as st
import config
import openai_utils
import st_utils
import chat_engine

client = openai_utils.get_client(config.api_key)
chat_engine.initialize_session(client, config.csv_path, config.station_name)

st_utils.render_title_and_intro(
    config.station_name,
    st.session_state.start_date,
    st.session_state.end_date
)

st_utils.render_chat_history()

user_input = st.chat_input("Ask your question")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    chat_engine.handle_user_input(client, config.assistant_id, user_input)
