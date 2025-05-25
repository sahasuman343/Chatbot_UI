import streamlit as st
import uuid
import json
import os
import atexit
from datetime import datetime

st.set_page_config(page_title="Chatbot")

# Directory to store chat logs
CHAT_LOG_DIR = "chat_logs"
os.makedirs(CHAT_LOG_DIR, exist_ok=True)

# Function to save chat to JSON file
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
        print(f"Saved chat to {filepath}")

def find_chat_files():
    """Find all chat JSON files in the chat log directory."""
    chat_files = []
    for filename in os.listdir(CHAT_LOG_DIR):
        # Ensure the file is for the current user
        
        chat_files.append(os.path.join(CHAT_LOG_DIR, filename))
    return chat_files


def update_sidebar():
    st.sidebar.title(f"Hi {st.session_state.username}!")


# Register to save on app teardown
# atexit.register(save_chat_to_json)

# Initialize session state
if "username" not in st.session_state:
    st.session_state.username = ""


# Streamlit app UI
st.title("SCM Chatbot")

# Username input
# if st.session_state.username == "":
#     st.session_state.username = st.text_input("Enter your username to begin:")

if st.session_state.username == "":
    username_input = st.text_input("Enter your username to begin:")
    if st.button("Start Chat") and username_input.strip():
        st.session_state.username = username_input.strip()
        st.rerun()


# Show chat only after username is provided
if st.session_state.username:
    st.toast(f"Welcome, {st.session_state.username} 👋")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["message"])

    # User input
    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Simple echo response
        response = f"Echo: {user_input}"
        st.session_state.chat_history.append({"role": "assistant", "message": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        # Save chat history to JSON file
        save_chat_to_json()
else:
    st.warning("Please enter your username to access the chatbot.")
