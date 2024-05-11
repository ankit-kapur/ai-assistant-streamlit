from app.sidebar import draw_sidebar
import streamlit as st
from dotenv import load_dotenv
import os
import base64
import time
from pathlib import Path

# Local packages
from app.tabs.analyze import AnalyzeBox
from constants.config import page_title
from app.tabs.chat import ChatBox
from app.tabs.settings import SettingsBox

# Init
load_dotenv()

# TEMPORARY HACK for whisper STT to work # TODO --- setup SSL
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# ------------------------------------------------------- App 
st.set_page_config(
    page_title=page_title, 
    page_icon="🧞‍♂️",
    initial_sidebar_state="auto", # or expanded or collapsed or auto
    layout="wide",
)
st.title(page_title)

# Tabs
chat_tab, analyze_tab, settings_tab = st.tabs(["💬  Chat", "🧐  Analyze", "⚙️ Settings"])

settings_box = SettingsBox()
settings_box.draw(settings_tab)

chat_box = ChatBox()
chat_box.draw(chat_tab)

analyze_box = AnalyzeBox()
analyze_box.draw(analyze_tab)

draw_sidebar()