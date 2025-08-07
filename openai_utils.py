import time
from openai import OpenAI
from PIL import Image
from io import BytesIO
import config

def get_client(api_key):
    return OpenAI(api_key=api_key)

def ensure_valid_file(client, fid):
    try:
        client.files.retrieve(fid)
        return True
    except:
        return False

def upload_file(client, path):
    uploaded = client.files.create(file=open(path, "rb"), purpose="assistants")
    print("Uploaded File:", uploaded.id)
    return uploaded

def create_thread(client):
    return client.beta.threads.create()

def delete_old_files(client, keep_id):
    for f in client.files.list().data:
        if f.id != keep_id:
            client.files.delete(f.id)
            print(f"Deleted file {f.id}")

def get_all_files():
    client = get_client(config.api_key)
    return client.files.list().data

def send_message(client, thread_id, user_input, file_id=None, first=False):
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input,
        attachments=[{
            "file_id": file_id,
            "tools": [{"type": "code_interpreter"}]
        }] if first else None
    )

def run_assistant(client, thread_id, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run.status == "completed":
            return run
        time.sleep(1)

def get_latest_response(client, thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
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

    return reply_text.strip(), image_data
