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
import whisper

# https://github.com/theevann/streamlit-audiorecorder
from audiorecorder import audiorecorder

# https://github.com/stefanrmmr/streamlit-audio-recorder
# from st_audiorec import st_audiorec

# My classes
from speak.speak_handler import SpeakingHandler

# Config
page_title = "Ankit's assistant"
bot_avatar = "https://img.freepik.com/premium-photo/drawing-robot-with-helmet-gloves-generative-ai_733139-11125.jpg"
human_avatar = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvnitFAIH_gCZg3Nq_65oi87usR1duVCT3epuTLWbjmA&s"
default_tts_voice = 0 # alloy
initial_ai_msg = "Hello Ankit. How can I help you today?"

# Init
last_ai_msg = ""
speakingHandler = SpeakingHandler()
load_dotenv()
# TTS ----- not sure if needed
if "audio" not in st.session_state:
    st.session_state["audio"] = None

# TEMPORARY HACK to disable SSL for whisper to work
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# STT (Whisper)
whisper_model = whisper.load_model("base") # base works just fine
stt_audio_filepath = "output/stt_audio.wav"

# ------------------------------------------------------- App 
st.set_page_config(
    page_title=page_title, 
    page_icon="🧞‍♂️",
    initial_sidebar_state="auto", # or expanded or collapsed
    layout="wide",
)
st.title(page_title)

# Tabs
chat_tab, analysis_tab, settings_tab = st.tabs(["💬  Chat", "🧐  Analyze", "⚙️ Settings"])

st.sidebar.header('📋 TODO')

now_box = st.sidebar.container(border=True)
next_box = st.sidebar.container(border=True)
later_box = st.sidebar.container(border=True)
with now_box:
    st.subheader("Now")

    st.checkbox(
        "[Feature] URL scraper",
        key="task6")
    st.checkbox(
        "[Bug] Session state doesn't save",
        key="task1")

    st.markdown(" ")
with next_box:
    st.subheader("Next")
    
    st.checkbox(
        "[Aesthetic] Chat window height should fill the screen height",
        key="task4")
    st.checkbox(
        "[Bug] AI text disappears if interrupted",
        key="task2")
    st.checkbox(
        "[Feature] Ollama API",
        key="task5")
    
    st.markdown(" ")
with later_box:
    st.subheader("Later")

    st.checkbox(
        "[Feature] PDF upload",
        key="task7")
    
    st.checkbox(
        "[Feature] Pause/play button: for Audio",
        key="task3")
    st.checkbox(
        "[Feature] Pause/play button: for Text",
        key="task8")
    
    st.markdown(" ")

# ------------------------------------------------------- Sidebar

llm_settings = settings_tab.expander('LLM', expanded = True)
llm_temperature = llm_settings.slider(
    "🎨 Temperature", 
    min_value=0.1, max_value=1.0, step=0.1, 
    value=0.5
)
llm_max_tokens = llm_settings.number_input(
    "🛑 Token limit", 
    value=2000, 
    min_value=10, step=100
)
# st.sidebar.markdown("""---""")
speech_settings = settings_tab.expander('Speech', expanded = True)
speech_settings.selectbox(
   "Voice generator",
   key="voice_gen_type",
   options=("OpenAI", "MacOS"),
   index=0,
   placeholder="Select voice generator",
)
speech_settings.slider(
    "🏎️ Speed", 
    key="tts_speed", 
    min_value=0.25, max_value=4.0, step=0.05, 
    value=1.0
)
# text = st.text_area("Your text", value = DEFAULT_TEXT, max_chars=4096, height=250)
speech_settings.radio(
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


def call_langchain(user_query, chat_history):

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(
        streaming=True,
        temperature=llm_temperature, 
        max_tokens=llm_max_tokens,
        callbacks=[speakingHandler]
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
        AIMessage(content=initial_ai_msg),
    ]



# ------------------------  Structure of the chat tab
chat_feed_container = chat_tab.container(border=True, height=300)

# chat_input_column, mic_button_column = chat_tab.columns([5, 1])
input_box_container = chat_tab.container(height=None, border=False)
mic_button_container = chat_tab.container(height=None, border=False)

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with chat_feed_container.chat_message("AI", avatar=bot_avatar):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with chat_feed_container.chat_message("Human", avatar=human_avatar):
            st.write(message.content)

def send_text_to_bot(text_message):
    st.session_state.chat_history.append(HumanMessage(content=text_message))

    with chat_feed_container.chat_message("Human", avatar=human_avatar):
        st.markdown(text_message)

    with chat_feed_container.chat_message("AI", avatar=bot_avatar):
        # with st.spinner("Generating response..."):
        response = st.write_stream(
            call_langchain(
                text_message, 
                st.session_state.chat_history))

        st.session_state.chat_history.append(
            AIMessage(content=response))

# user input
user_query = input_box_container.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    send_text_to_bot(user_query)

# Recording
# TODO --- Bring down to the bottom.
# For continuous stream, see: https://github.com/whitphx/streamlit-stt-app/blob/main/app_deepspeech.py

with mic_button_container:
    audio = audiorecorder(start_prompt = "", stop_prompt = "", show_visualizer = False)

if len(audio) > 0:
    # To play audio in frontend:
    # st.audio(audio.export().read())  

    # To save audio to a file, use pydub export method:
    audio.export(stt_audio_filepath, format="wav")
    # To get audio properties, use pydub AudioSegment properties:
    # st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

    # STT
    result = whisper_model.transcribe(stt_audio_filepath)
    # Text to 'user_query'
    send_text_to_bot(result["text"])
