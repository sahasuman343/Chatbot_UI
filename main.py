"""
SCM Chatbot - A Streamlit-based chatbot application with user authentication and feedback collection.

This module implements a chatbot interface with the following features:
- User authentication (regular users and admin)
- Chat history tracking
- Feedback collection and analytics
- Session management
- Persistent storage of chat logs
"""

import streamlit as st
import uuid
import json
import os
from datetime import datetime, timedelta
import time
from collections import defaultdict
st.set_page_config(
    page_title="SCM Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Basic styling for better UI
st.markdown("""
<style>
    /* Base styles */
    .stButton button {
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .stChatMessage[data-testid="stChatMessage"] {
        background-color: #000000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        border-radius: 15px;
        padding: 1.2rem;
        color: #ffffff;
    }
    
    /* Ensure markdown text is visible on dark background */
    .stChatMessage[data-testid="stChatMessage"] p,
    .stChatMessage[data-testid="stChatMessage"] li,
    .stChatMessage[data-testid="stChatMessage"] code {
        color: #ffffff;
    }
    
    /* User message styling */
    .stChatMessage[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
        background-color: #4CAF50;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
        background-color: #2196F3;
    }
    
    /* Headers and metrics */
    h1, h2, h3 {
        padding: 0.5rem 0;
        color: #87CEEB;
        display: inline-block;
    }
    
    .stMetric {
        background-color: #000000;
        padding: 1rem;
        border-radius: 5px;
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
    }
    
    /* Sidebar button hover effects */
    [data-testid="stSidebar"] .stButton button {
        transition: all 0.3s ease;
        background-color: #000000;
        border: 1px solid #e0e0e0;
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #e0e0e0;
        transform: translateY(-2px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Active sidebar button state */
    [data-testid="stSidebar"] .stButton button:active {
        transform: translateY(0);
        box-shadow: none;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .stSpinner {
        animation: pulse 1.5s infinite;
    }
    
    /* Feedback animation */
    @keyframes feedback-pop {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .stFeedback:active {
        animation: feedback-pop 0.3s ease;
    }
    
    /* Tooltip styling */
    [data-tooltip]:hover:before {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 0.5rem;
        background: rgba(0,0,0,0.8);
        color: white;
        border-radius: 4px;
        font-size: 0.8rem;
        white-space: nowrap;
        z-index: 1000;
    }
    
    /* Back to top button */
    .back-to-top {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #000000;
        color: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        opacity: 0.7;
        transition: opacity 0.3s;
        z-index: 1000;
    }
    
    .back-to-top:hover {
        opacity: 1;
    }
    
    /* Success message styling */
    .stSuccess {
        border-radius: 10px;
        padding: 1rem;
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Error message styling */
    .stError {
        border-radius: 10px;
        padding: 1rem;
        background: linear-gradient(45deg, #f44336, #e53935);
        color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)



# --- Simulated Assistant Response Stream ---
def chat_stream(prompt: str) -> str:
    """
    Simulate a streaming chat response.
    
    Args:
        prompt (str): The user's input message
        
    Yields:
        str: Characters of the response one at a time
    """
    response = f'You said, "{prompt}" ...interesting.'
    for char in response:
        yield char
        time.sleep(0.02)

# --- Feedback persistence ---
def save_feedback(index: int) -> None:
    """
    Save user feedback for a specific message.
    
    Args:
        index (int): Index of the message in chat history
    """
    st.session_state.chat_history[index]["feedback"] = st.session_state[f"feedback_{index}"]
    save_chat_to_json()

# --- Paths and User Config ---
with open("users.json", "r") as f:
    USERS = json.load(f)

CHAT_LOG_DIR = "chat_logs"
os.makedirs(CHAT_LOG_DIR, exist_ok=True)

# --- Save chat to JSON file ---
def save_chat_to_json() -> None:
    """
    Save the current chat session to a JSON file.
    
    The file is saved in the CHAT_LOG_DIR with format:
    chat_{username}_{session_id}.json
    """
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
def get_all_session_previews() -> list:
    """
    Get previews of all chat sessions.
    
    Returns:
        list: List of dictionaries containing session previews with keys:
            - username: User who created the session
            - session_id: Unique session identifier
            - preview: First user message in the session
            - full_data: Complete session data
            - filename: Name of the session file
    """
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

def get_user_session_previews(username: str) -> list:
    """
    Get previews of chat sessions for a specific user.
    
    Args:
        username (str): Username to filter sessions for
        
    Returns:
        list: List of session previews for the specified user
    """
    return [s for s in get_all_session_previews() if s["username"] == username]

# --- Feedback Summary Utilities ---
def get_feedback_summaries() -> tuple:
    """
    Get overall and session-wise feedback summaries.
    
    Returns:
        tuple: (overall_stats, sessionwise_stats)
            - overall_stats: Dict with total positive/negative feedback counts
            - sessionwise_stats: Dict with feedback stats per session
    """
    overall = {"positive": 0, "negative": 0}
    sessionwise = {}
    for filename in os.listdir(CHAT_LOG_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(CHAT_LOG_DIR, filename)
            with open(filepath, "r") as f:
                data = json.load(f)
            pos, neg = 0, 0
            for msg in data.get("chat_history", []):
                if msg.get("role") == "assistant":
                    if msg.get("feedback") == 1:
                        pos += 1
                    elif msg.get("feedback") == 0:
                        neg += 1
            overall["positive"] += pos
            overall["negative"] += neg
            sessionwise[data["session_id"]] = {
                "username": data["username"],
                "timestamp": data.get("timestamp", ""),
                "positive": pos,
                "negative": neg,
                "preview": next((msg["message"] for msg in data["chat_history"] if msg["role"] == "user"), "No message"),
                "full_data": data
            }
    return overall, sessionwise

# --- Sidebar: Admin Chat Sessions + Feedback Summary ---
def render_sidebar_admin_feedback() -> tuple:
    """
    Render the admin feedback section in the sidebar.
    
    Returns:
        tuple: (overall_stats, sessionwise_stats) from get_feedback_summaries()
    """
    st.sidebar.markdown("## 📝 Feedback Summary")
    overall, sessionwise = get_feedback_summaries()

    # Overall feedback summary button
    if st.sidebar.button("Overall Feedback Summary", key="overall_feedback"):
        st.session_state.selected_feedback_summary = "overall"

    # Session-wise feedback summary
    st.sidebar.markdown("### Session-wise Feedback")
    for session_id, info in sessionwise.items():
        label = f"{info['username']} ({info['timestamp'][:10]})"
        if st.sidebar.button(label, key=f"session_{session_id}", use_container_width=True):
            st.session_state.selected_feedback_summary = session_id

    return overall, sessionwise

# --- Sidebar: User Sessions (Today + Past 7 Days) ---
def render_sidebar_chat_history_users() -> None:
    """
    Render the user's chat history in the sidebar.
    
    Shows today's sessions and sessions from the past 7 days.
    """
    # New chat button at the top
    if st.sidebar.button("🆕 Start New Chat", help="Click to start a new chat session", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.rerun()
    
    st.sidebar.markdown("## 💬 Your Chat Sessions")
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
if "selected_feedback_summary" not in st.session_state:
    st.session_state.selected_feedback_summary = "overall"

# --- Login ---
if st.session_state.username == "":
    st.title("Login")
    col1, col2 = st.columns(2)
    with col1:
        is_admin = st.checkbox("Login as admin")
    with col2:
        st.markdown("### Welcome!")
    
    username_input = st.text_input("Username", placeholder="Enter your username")
    password_input = st.text_input("Password", type="password", placeholder="Enter your password") if is_admin else None
    
    if st.button("Login", use_container_width=True):
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
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.username}!")
        st.markdown("---")
        
        if st.session_state.username == "admin":
            overall_feedback, sessionwise_feedback = render_sidebar_admin_feedback()
        else:
            render_sidebar_chat_history_users()
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.username = ""
            st.session_state.session_id = ""
            st.session_state.chat_history = []
            st.session_state.selected_feedback_summary = "overall"
            st.rerun()

# --- Admin Feedback Dashboard with Feedback Summary ---
if st.session_state.username == "admin":
    st.title("Admin Feedback Dashboard")
    
    # Show feedback summary based on sidebar selection
    selected = st.session_state.get("selected_feedback_summary", "overall")
    if selected == "overall":
        st.subheader("Overall Feedback Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Positive Feedback", overall_feedback["positive"])
        with col2:
            st.metric("Negative Feedback", overall_feedback["negative"])
    else:
        info = sessionwise_feedback[selected]
        st.subheader(f"Session Feedback: {info['username']}")
        st.caption(f"Session from: {info['timestamp'][:19]}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Positive Feedback", info["positive"])
        with col2:
            st.metric("Negative Feedback", info["negative"])
        
        st.markdown("### Chat History")
        for i, msg in enumerate(info["full_data"]["chat_history"]):
            with st.chat_message(msg["role"]):
                st.markdown(msg["message"])
                if msg["role"] == "assistant":
                    feedback = msg.get("feedback", "No Feedback")
                    st.caption(f"Feedback: {'👍' if feedback == 1 else '👎' if feedback == 0 else '❓'}")

# --- Regular Chat View ---
elif st.session_state.username:
    st.title("SCM Chatbot")
    
    # Add back to top button
    st.markdown("""
        <div class="back-to-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
            ↑
        </div>
    """, unsafe_allow_html=True)
    
    st.success(f"Welcome back, {st.session_state.username}! (Session ID: `{st.session_state.session_id}`)")
    
    # Chat container with improved styling
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            with st.chat_message(message["role"]):
                st.markdown(message["message"])
                if message["role"] == "assistant":
                    st.session_state[f"feedback_{i}"] = message.get("feedback")
                    col1, col2 = st.columns([6, 1])
                    with col2:
                        st.feedback(
                            "thumbs",
                            key=f"feedback_{i}",
                            disabled=message.get("feedback") is not None,
                            on_change=save_feedback,
                            args=[i],
                        )
    
    # Chat input with tooltip
    user_input = st.chat_input("💭 Type your message here...", key="chat_input")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = st.write_stream(chat_stream(user_input))
        st.session_state.chat_history.append({"role": "assistant", "message": response})
        col1, col2 = st.columns([6, 1])
        with col2:
            st.feedback(
                "thumbs",
                key=f"feedback_{len(st.session_state.chat_history) - 1}",
                on_change=save_feedback,
                args=[len(st.session_state.chat_history) - 1],
            )
        save_chat_to_json()
