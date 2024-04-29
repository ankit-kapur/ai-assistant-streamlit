# TTS via OpenAI
from pathlib import Path

from openai import OpenAI

# Open AI init
client = OpenAI() # api_key=st.secrets["OPENAI_API_KEY"]

def make_tts_file(text, voice):
    speech_file_path = Path("tts_audio.mp3")
    response = client.audio.speech.create(
      model="tts-1",
      voice=voice,
      input=text
    )
    response.stream_to_file(speech_file_path)