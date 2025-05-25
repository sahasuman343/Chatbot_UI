import streamlit as st
import uuid
import json
import os
from datetime import datetime, timedelta
import time
from collections import defaultdict, Counter

st.set_page_config(page_title="SCM Chatbot")

# --- Simulated Assistant Response Stream ---
def chat_stream(prompt):
    response = f'You said, "{prompt}" ...interesting.'
    for char in response:
        yield char
        time.sleep(0.02)

# --- Feedback persistence ---
def save_feedback(index):
    st.session_state.chat_history[index]["feedback"] = st.session_state[f"feedback_{index}"]
    save_chat_to_json()

# --- Paths and User Config ---
with open("users.json", "r") as f:
    USERS = json.load(f)

CHAT_LOG_DIR = "chat_logs"
os.makedirs(CHAT_LOG_DIR, exist_ok=True)

# --- Save chat to JSON file ---
def save_chat_to_json():
    if st.session_state.get("username") and st.session_state.get("chat_history"):
        filename = f"chat_{st.session_state.username}_{st.session_state.session_id}.json"
        filepath = os.path.join(CHAT_LOG_DIR, filename)
        data = {
            "username": st.session_state.username,
            "session_id": st.session_state.session_id,
            "timestamp": datetime.now().isoformat(),
            "chat_history": st.session_state.chat_history,
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

# --- Session Preview Loaders ---
def get_all_session_previews():
    previews = []
    for filename in os.listdir(CHAT_LOG_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(CHAT_LOG_DIR, filename)
            with open(filepath, "r") as f:
                data = json.load(f)
                if data["chat_history"]:
                    first_user_msg = next((msg["message"] for msg in data["chat_history"] if msg["role"] == "user"), "No message")
                    previews.append({
                        "username": data["username"],
                        "session_id": data["session_id"],
                        "preview": first_user_msg,
                        "full_data": data,
                        "filename": filename
                    })
    return previews

def get_user_session_previews(username):
    return [s for s in get_all_session_previews() if s["username"] == username]

# --- Sidebar: Admin Chat Sessions ---
def render_sidebar_chat_history_admin():
    st.sidebar.markdown("## 💬 All Chat Sessions")
    sessions = get_all_session_previews()
    for s in sessions:
        label = f"{s['username']}: {s['preview'][:30]}"
        if st.sidebar.button(label, key=s["session_id"], use_container_width=True, help="Click to load this chat session"):
            st.session_state.session_id = s["session_id"]
            st.session_state.chat_history = s["full_data"]["chat_history"]
            st.rerun()

# --- Sidebar: User Sessions (Today + Past 7 Days) ---
def render_sidebar_chat_history_users():
    st.sidebar.markdown("## 💬 Your Chat Sessions")

    if st.sidebar.button("🆕 Start New Chat", help="Click to start a new chat session", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.rerun()

    sessions = get_user_session_previews(st.session_state.username)
    today = datetime.now().date()
    past_7_days = today - timedelta(days=7)

    today_sessions, recent_sessions = [], []

    for s in sessions:
        session_time = datetime.fromisoformat(s["full_data"]["timestamp"]).date()
        if session_time == today:
            today_sessions.append(s)
        elif session_time >= past_7_days:
            recent_sessions.append(s)

    if today_sessions:
        st.sidebar.markdown("### 📅 Today")
        for s in today_sessions:
            label = f"{s['preview'][:40]}"
            if st.sidebar.button(label, key="today_" + s["session_id"], use_container_width=True):
                st.session_state.session_id = s["session_id"]
                st.session_state.chat_history = s["full_data"]["chat_history"]
                st.rerun()

    if recent_sessions:
        st.sidebar.markdown("### 🗓 Past 7 Days")
        for s in recent_sessions:
            label = f"{s['preview'][:40]}"
            if st.sidebar.button(label, key="past_" + s["session_id"], use_container_width=True):
                st.session_state.session_id = s["session_id"]
                st.session_state.chat_history = s["full_data"]["chat_history"]
                st.rerun()

# --- Session State Defaults ---
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = ""

# --- Login ---
if st.session_state.username == "":
    st.title("🔐 SCM Chatbot Login")
    is_admin = st.checkbox("Login as admin")

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password") if is_admin else None

    if st.button("Login"):
        username = username_input.strip()
        password = password_input.strip() if is_admin else None

        if is_admin:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.username = username
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.chat_history = []
                st.rerun()
            else:
                st.error("Invalid admin credentials.")
        else:
            if username and username.lower() != "admin":
                st.session_state.username = username
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.chat_history = []
                st.rerun()
            else:
                st.error("Invalid username.")

# --- Sidebar & Logout ---
if st.session_state.username:
    if st.session_state.username == "admin":
        render_sidebar_chat_history_admin()
    else:
        render_sidebar_chat_history_users()

    st.sidebar.markdown("---")
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.username = ""
            st.session_state.session_id = ""
            st.session_state.chat_history = []
            st.rerun()

# --- Admin Feedback Dashboard ---
if st.session_state.username == "admin":
    st.title("🛠 Admin Feedback Dashboard")

    all_sessions = get_all_session_previews()
    user_list = sorted(set(s["username"] for s in all_sessions))
    selected_user = st.selectbox("Filter by user", ["All"] + user_list)

    filtered_sessions = all_sessions if selected_user == "All" else get_user_session_previews(selected_user)

    session_ids = [s["session_id"] for s in filtered_sessions]
    selected_session_id = st.selectbox("Select a session", session_ids)

    selected_session = next(s for s in filtered_sessions if s["session_id"] == selected_session_id)
    st.subheader(f"Session by `{selected_session['username']}`")

    thumbs_up = sum(1 for m in selected_session["full_data"]["chat_history"] if m["role"] == "assistant" and m.get("feedback") == 1)
    thumbs_down = sum(1 for m in selected_session["full_data"]["chat_history"] if m["role"] == "assistant" and m.get("feedback") == 0)

    st.metric("👍 Positive Feedback", thumbs_up)
    st.metric("👎 Negative Feedback", thumbs_down)

    st.markdown("### Chat with Feedback")
    for i, msg in enumerate(selected_session["full_data"]["chat_history"]):
        with st.chat_message(msg["role"]):
            st.markdown(msg["message"])
            if msg["role"] == "assistant":
                feedback = msg.get("feedback", "No Feedback")
                st.caption(f"Feedback: {feedback}")

# --- Regular Chat View ---
elif st.session_state.username:
    st.title("🤖 SCM Chatbot")
    st.success(f"Hello, {st.session_state.username} (Session ID: `{st.session_state.session_id}`)")

    for i, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.markdown(message["message"])
            if message["role"] == "assistant":
                st.session_state[f"feedback_{i}"] = message.get("feedback")
                st.feedback(
                    "thumbs",
                    key=f"feedback_{i}",
                    disabled=message.get("feedback") is not None,
                    on_change=save_feedback,
                    args=[i],
                )

    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                response = st.write_stream(chat_stream(user_input))
                st.session_state.chat_history.append({"role": "assistant", "message": response})
                st.feedback(
                    "thumbs",
                    key=f"feedback_{len(st.session_state.chat_history) - 1}",
                    on_change=save_feedback,
                    args=[len(st.session_state.chat_history) - 1],
                )

        save_chat_to_json()
