import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
import os
import base64
import time
from pathlib import Path

from utils.tts import make_tts_file

load_dotenv()

# TTS
if "audio" not in st.session_state:
    st.session_state["audio"] = None

# Init
initial_ai_msg = "Hello, I am a bot. How can I help you?"
last_ai_msg = initial_ai_msg
page_title = "Ankit's streaming RAG"

# app config
st.set_page_config(page_title=page_title, page_icon="🤖")
st.title(page_title)

# Sidebar
st.sidebar.write(last_ai_msg)
llm_temperature = st.sidebar.slider("Temperature", min_value=0.1, max_value=1.0, step=0.1, value=0.5)


llm_max_tokens = st.sidebar.number_input("Max tokens", value=2000, min_value=10)

# text = st.text_area("Your text", value = DEFAULT_TEXT, max_chars=4096, height=250)
voice = st.sidebar.radio("Voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], horizontal = True, index=3, help="Previews can be found [here](https://platform.openai.com/docs/guides/text-to-speech/voice-options)")

# if st.sidebar.button("📣 Say it"):
#     text_to_speech(last_ai_msg, voice)

# prompt
template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

def get_response(user_query, chat_history):

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(
        temperature=llm_temperature, 
        max_tokens=llm_max_tokens,
        callbacks=[])
    
    # Create Langchain
    chain = prompt | llm | StrOutputParser()
    
    # Invoke the chain
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

    
# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))

        # Call TTS function here
        make_tts_file(response, voice)

    st.session_state.chat_history.append(AIMessage(content=response))

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

autoplay_audio("tts_audio.mp3")
