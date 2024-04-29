import base64
import time
from langchain.callbacks.base import BaseCallbackHandler
from openai import OpenAI
from pathlib import Path
import eyed3
import streamlit as st
# Open AI init
client = OpenAI()

class SpeakingHandler(BaseCallbackHandler):
    def __init__(self):
            self.new_sentence = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print("New token received = " + token)
        if token == "":
             print("Empty token. Returning.")
             return

        self.new_sentence += token

        if not self.new_sentence:
             print("🚨 🚨 🚨 Empty sentence")
             return

        # Check if the new token forms a sentence.
        if token in ".:!?。：！？\n":
            # Synthesize the new sentence
            speak_this = self.new_sentence
            self.new_sentence = ""

            voice = st.session_state.tts_voice
            speed = st.session_state.tts_speed

            print("🏆 ---------- Generating TTS!" + "\n\tsentence = {" + speak_this + "}")
            
            self.make_tts_file(speak_this, voice, speed)
            self.speak_sentence()


    def on_llm_end(self, response, **kwargs) -> None:
        print("ENDDDDDDDDDD ")
        self.new_sentence = ""

    def speak_sentence(self):
        filepath = "output/tts_audio.mp3"
        with open(filepath, "rb") as f:
            print("\t Reading audio file")
            data = f.read()
            audio_base64 = base64.b64encode(data).decode()
            audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'

        print("\t Setting markdown")
        st.markdown(audio_tag, unsafe_allow_html=True)

        # TODO ------ Sleep is causing text display to pause too.
        number_of_seconds = eyed3.load(filepath).info.time_secs
        print("\tSleeping " + str(number_of_seconds) + " seconds")
        time.sleep(number_of_seconds)

    def make_tts_file(self, text, voice, tts_speed):
        speech_file_path = Path("output/tts_audio.mp3")
        response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        speed=tts_speed,

        # TODO: Change to stream
        # https://community.openai.com/t/streaming-from-text-to-speech-api/493784/14
        )
        response.stream_to_file(speech_file_path)