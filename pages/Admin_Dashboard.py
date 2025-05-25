import streamlit as st
import os
import json
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="Admin Dashboard", layout="wide")

# Prevent non-admin users from accessing this page
if st.session_state.get("username") != "admin":
    st.error("You are not authorized to view this page.")
    st.stop()


CHAT_LOG_DIR = "chat_logs"
os.makedirs(CHAT_LOG_DIR, exist_ok=True)

st.title("📊 Admin Dashboard")
st.markdown("### Overview of chatbot usage")

# Collect usage data
users = set()
session_count = 0
daily_counts = {}
user_counts = {}

for filename in os.listdir(CHAT_LOG_DIR):
    if filename.endswith(".json"):
        filepath = os.path.join(CHAT_LOG_DIR, filename)
        with open(filepath, "r") as f:
            data = json.load(f)

        users.add(data["username"])
        session_count += 1

        date_key = datetime.fromisoformat(data["timestamp"]).date()
        daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
        user_counts[data["username"]] = user_counts.get(data["username"], 0) + 1

# Display metrics
col1, col2 = st.columns(2)
col1.metric("👤 Total Users", len(users))
col2.metric("💬 Total Sessions", session_count)

# Daily usage (past 7 days)
st.subheader("📅 Daily Session Count (Last 7 Days)")
today = datetime.now().date()
past_7_days = [today - timedelta(days=i) for i in reversed(range(7))]
daily_data = {
    "Date": [d.strftime("%Y-%m-%d") for d in past_7_days],
    "Sessions": [daily_counts.get(d, 0) for d in past_7_days]
}
df_daily = pd.DataFrame(daily_data)
st.bar_chart(df_daily.set_index("Date"))

# Top users
st.subheader("🏆 Top Active Users")
top_users_df = pd.DataFrame(list(user_counts.items()), columns=["Username", "Sessions"])
top_users_df = top_users_df.sort_values(by="Sessions", ascending=False).reset_index(drop=True)
st.table(top_users_df.head(10))
