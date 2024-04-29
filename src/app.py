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

from speak.speak_handler import SpeakingHandler

load_dotenv()

# TTS
if "audio" not in st.session_state:
    st.session_state["audio"] = None

# Init
initial_ai_msg = "Hello, I am a bot. How can I help you?"
last_ai_msg = ""
page_title = "Ankit's streaming RAG"
speakingHandler = SpeakingHandler()

# Defaults
default_tts_voice = 3

# app config
st.set_page_config(page_title=page_title, page_icon="🤖")
st.title(page_title)

# ------------------------------------------------------- Sidebar
st.sidebar.header('Model settings')
llm_temperature = st.sidebar.slider(
    "🎨 Temperature", 
    min_value=0.1, max_value=1.0, step=0.1, 
    value=0.5
)
llm_max_tokens = st.sidebar.number_input(
    "🪀 Max tokens", 
    value=2000, 
    min_value=10, step=100
)

st.sidebar.header('Speech settings')
voice_gen_type = st.sidebar.selectbox(
   "Voice generator",
   key="voice_gen_type",
   options=("OpenAI", "MacOS"),
   index=0,
   placeholder="Select voice generator",
)
tts_speed = st.sidebar.slider(
    "🏎️ Speed", 
    key="tts_speed", 
    min_value=0.25, max_value=4.0, step=0.05, 
    value=1.0
)
# text = st.text_area("Your text", value = DEFAULT_TEXT, max_chars=4096, height=250)
st.sidebar.radio(
    "🗣️ Voice", 
    options=["alloy", "echo", "fable", "onyx", "nova", "shimmer"], 
    key="tts_voice", 
    horizontal = True, 
    index=default_tts_voice, 
    help="Previews can be found [here](https://platform.openai.com/docs/guides/text-to-speech/voice-options)")

# speakingHandler.settings_save(voice=tts_voice, speed=tts_speed)

# if st.sidebar.button("📣 Reset"):
#     default_tts_voice = 3

# prompt
template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

def get_response(user_query, chat_history):

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(
        streaming=True,
        temperature=llm_temperature, 
        max_tokens=llm_max_tokens,
        callbacks=[
            speakingHandler,

            # TODO ------------------ use another callback? for displaying text
            # https://gist.github.com/goldengrape/84ce3624fd5be8bc14f9117c3e6ef81a
            
            # No. write_stream should work. 
            # Sleep is the issue. Do it in a thread.
        ]
    )
    
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
        with st.spinner("Generating response..."):
            response = st.write_stream(
                get_response(
                    user_query, 
                    st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(content=response))
