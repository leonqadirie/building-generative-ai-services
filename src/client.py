import requests
import streamlit as st

st.title("FastAPI ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, bytes):
            st.audio(content)
        else:
            st.markdown(content)


if prompt := st.chat_input("Write your prompt in this input field"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        data = {"text": prompt, "model": "tinyllama", "temperature": 0.1}
        response = requests.post(f"http://localhost:8000/generate/text", json=data).text
        st.text(response)
    with st.chat_message("assistant"):
        data = {"prompt": prompt, "model": "tinysd", "output_size": (512, 512)}
        response = requests.post(f"http://localhost:8000/generate/image", json=data).content
        st.text("Here is your generated image")
        st.image(response)
    with st.chat_message("assistant"):
        data = {"prompt": prompt}
        response = requests.post(f"http://localhost:8000/generate/audio", json=data).content
        st.text("Here is your generated audio")
        st.audio(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": "Here is your generated audio"}
    )
