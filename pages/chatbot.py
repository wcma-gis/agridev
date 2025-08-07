import streamlit as st
import config
import openai_utils
import st_utils
import chat_engine

st_utils.init_st()



if "selected_station" not in st.session_state:
    st.error("No station selected. Please go back to the main page.")
    st.stop()

station_name = st.session_state.selected_station

client = openai_utils.get_client(config.api_key)
if not chat_engine.initialize_session(client, config.base_csv_path, station_name):
    st.error(f"No data available for station: {station_name}")
    if st.button("← Select another station"):
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

        chat_engine.handle_user_input(client, config.assistant_id, user_input)

# with st.expander("🛠️ Diagnostics"):
#     st.write("Session ID:", st.session_state.get("session_id"))
#     st.write("🗂️ File ID (current session):", st.session_state.get("file_id"))
#
#     if st.button("🔄 Refresh file list"):
#         st.session_state._show_files = True
#
#     if st.session_state.get("_show_files"):
#         st.write("📄 All files in account:")
#         files = openai_utils.get_all_files()
#         for f in files:
#             st.write(f"- {f.id} | {f.filename} | {f.created_at}")
