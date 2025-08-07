import streamlit as st
import config
import openai_utils
import st_utils
import chat_engine

st_utils.init_st()

if "assistant_id" not in st.session_state:
    assigned = st_utils.allocate_assistant()
    if assigned is None:
        st.error("All assistants are busy. Please try again later.")
        st.stop()
    st.session_state.assistant_id = assigned


if "selected_station" not in st.session_state:
    st.error("No station selected. Please go back to the main page.")
    st.stop()

station_name = st.session_state.selected_station

client = openai_utils.get_client(config.api_key)
if not chat_engine.initialize_session(client, config.base_csv_path, station_name):
    st.error(f"No data available for station: {station_name}")
    if st.button("← Select another station"):
        st_utils.free_assistant()
        st.switch_page("app.py")
    st.stop()
else:
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

        chat_engine.handle_user_input(client, st.session_state.assistant_id, user_input)



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
