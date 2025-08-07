import streamlit as st
import openai
import time
import pandas as pd
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv; load_dotenv()
import os

api_key = st.secrets["OPENAI_API_KEY"]
assistant_id = st.secrets["ASSISTANT_ID"]


client = openai.OpenAI(api_key=api_key)

csv_path = "all_small.csv"
station_name = "Dooen 2"

def ensure_valid_file(fid):
    try:
        client.files.retrieve(fid)
        return True
    except:
        return False

if "thread_id" not in st.session_state or "file_id" not in st.session_state or not ensure_valid_file(st.session_state.file_id):
    df = pd.read_csv(csv_path)
    df = df[df["station"] == station_name]
    df.to_csv("filtered.csv", index=False)

    start_date = df["DateTime"].min()
    end_date = df["DateTime"].max()
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date

    uploaded = client.files.create(file=open("filtered.csv","rb"), purpose="assistants")
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
    st.session_state.file_id = uploaded.id
    st.session_state.chat_history = []

    print("Thread:", thread.id)
    print("File:", uploaded.id)

    for f in client.files.list().data:
        if f.id != uploaded.id:
            client.files.delete(f.id)
            print("Deleted old file", f.id)

st.title(f"AgriBot — Station: {station_name}")

if not st.session_state.chat_history:
    st.markdown(
        f"Hi, I am your AgriBot. I have the station data for the period "
        f"**{st.session_state.start_date}** to **{st.session_state.end_date}**. "
        f"Ask me any question based on that."
    )

for entry in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(entry["user"])
    with st.chat_message("assistant"):
        st.markdown(entry["assistant"])
        if entry.get("image"):
            st.image(entry["image"])

user_input = st.chat_input("Ask your question")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    loading_slot = st.empty()
    loading_slot.markdown("⏳ AgriBot is thinking...")

    first_message = len(st.session_state.chat_history) == 0
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input,
        attachments=[{
            "file_id": st.session_state.file_id,
            "tools": [{"type": "code_interpreter"}]
        }] if first_message else None
    )

    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )
        if run.status == "completed":
            break
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
    m = next(m for m in messages.data if m.role == "assistant")

    reply_text = ""
    image_data = None

    for c in m.content:
        if c.type == "text":
            reply_text += c.text.value + "\n"
        elif c.type == "image_file":
            raw = client.files.with_raw_response.retrieve_content(c.image_file.file_id)
            if raw.status_code == 200:
                image_data = Image.open(BytesIO(raw.content))

    loading_slot.empty()

    with st.chat_message("assistant"):
        if image_data:
            st.image(image_data)
        st.markdown(reply_text)

    st.session_state.chat_history.append({
        "user": user_input,
        "assistant": reply_text,
        "image": image_data
    })
