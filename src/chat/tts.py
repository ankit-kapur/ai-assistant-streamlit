
import streamlit as st


# My classes
from speak.speak_handler import SpeakingHandler

speakingHandler = SpeakingHandler()


# TTS init ----- not sure if needed
if "audio" not in st.session_state:
    st.session_state["audio"] = None