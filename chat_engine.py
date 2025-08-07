import streamlit as st
import data_utils
import openai_utils
import st_utils
import config


def initialize_session(client, base_csv_path, station_name):
    if (
        "thread_id" not in st.session_state or
        "file_id" not in st.session_state or
        not openai_utils.ensure_valid_file(client, st.session_state.file_id) or
        st.session_state.get("active_station") != station_name
    ):
        df = data_utils.load_and_filter_data(base_csv_path, station_name)

        print(f"{station_name}: {len(df)}")

        if len(df) == 0:
            return False

        data_utils.save_filtered_csv(df)

        start_date, end_date = data_utils.get_date_range(df)
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date

        uploaded = openai_utils.upload_file(client, config.filtered_csv)
        thread = openai_utils.create_thread(client)

        st.session_state.thread_id = thread.id
        st.session_state.file_id = uploaded.id
        st.session_state.chat_history = []
        st.session_state.active_station = station_name

        if "prev_file_id" in st.session_state and st.session_state.prev_file_id != uploaded.id:
            try:
                client.files.delete(st.session_state.prev_file_id)
            except:
                pass
        st.session_state.prev_file_id = uploaded.id

    return True




def handle_user_input(client, assistant_id, user_input):
    loading_slot = st_utils.render_loading()
    loading_slot.markdown("⏳ AgriBot is thinking...")

    first = len(st.session_state.chat_history) == 0
    openai_utils.send_message(
        client,
        st.session_state.thread_id,
        user_input,
        st.session_state.file_id,
        first
    )

    openai_utils.run_assistant(client, st.session_state.thread_id, assistant_id)
    reply_text, image_data = openai_utils.get_latest_response(client, st.session_state.thread_id)

    loading_slot.empty()
    st_utils.render_assistant_response(reply_text, image_data)

    st.session_state.chat_history.append({
        "user": user_input,
        "assistant": reply_text,
        "image": image_data
    })
