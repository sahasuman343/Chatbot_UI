import streamlit as st
import time
import uuid


def generate_response(prompt, session_id):
    response = f'You said, "{prompt}" ...interesting. session id {session_id}'
    for char in response:
        yield char
        time.sleep(0.02)

st.title("ChatGPT-like clone")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(generate_response(prompt, st.session_state.session_id))
    st.session_state.messages.append({"role": "assistant", "content": response})
