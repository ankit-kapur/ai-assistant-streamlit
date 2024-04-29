import base64
import time
from langchain.callbacks.base import BaseCallbackHandler
from openai import OpenAI
from pathlib import Path
import eyed3
import streamlit as st

from os import system

# Open AI init
openai_client = OpenAI()

class SpeakingHandler(BaseCallbackHandler):
    def __init__(self):
        self.new_sentence = ""
        self.sentence_index = -1

    # @Override from Langchain
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print("token = " + token)

        # Empty token comes at both the START and END of the whole response.
        if token == "":
             print("Empty token. Returning.")
             self.reset()
             return

        self.new_sentence += token

        if not self.new_sentence or self.new_sentence == "":
             print("🚨 🚨 🚨 Empty sentence ---- should not happen")
             return

        # Sentence?
        if token in ".:!?。：！？\n":
            # Synthesize the new sentence
            speak_this = self.new_sentence
            self.sentence_index += 1

            
            print("📣 ---------- Generating TTS!" + 
                  f"\n\tsentence #{self.sentence_index} = (" + speak_this + ")")
            
            if "MacOS" == st.session_state.voice_gen_type:
                # Ask OS to speak
                system('say ' + speak_this)
            elif "OpenAI" == st.session_state.voice_gen_type:
                self.openai_speak_sentence(speak_this)
            
            self.new_sentence = ""
            
    # @Override from Langchain
    def on_llm_end(self, response, **kwargs) -> None:
        print("ENDDDDDDDDDD ")
        self.new_sentence = ""

    def reset(self):
        print("⛱️ Reset")
        self.sentence_index = -1
        self.new_sentence = ""
    
    def openai_speak_sentence(self, sentence):
        response = self.call_openai_tts(sentence)
        self.make_tts_file(response)
        self.play_audio_file()

    def play_audio_file(self):
        if self.sentence_index == -1:
            print("\t\t Empty speak request. self.sentence_index = " + self.sentence_index)
            return
        filepath = self.get_audio_file_path()
        with open(filepath, "rb") as f:
            print("\t 🔈 🔈 🔈 Reading audio file --- " + filepath)
            data = f.read()
            audio_base64 = base64.b64encode(data).decode()
            audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'

            print("\t Setting markdown")
            st.markdown(audio_tag, unsafe_allow_html=True)

            # TODO ------ Sleep is causing text display to pause too.
            number_of_seconds = eyed3.load(filepath).info.time_secs
            print("\t Sleeping " + str(number_of_seconds) + " seconds")
            time.sleep(number_of_seconds)

    def call_openai_tts(self, text):
        voice = st.session_state.tts_voice
        speed = st.session_state.tts_speed

        # API call
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            speed=speed,
        )
        return response

    def make_tts_file(self, response):
        # TODO: Change to stream
        # https://community.openai.com/t/streaming-from-text-to-speech-api/493784/14
        speech_file_path = Path(self.get_audio_file_path())
        response.stream_to_file(speech_file_path)
    
    def get_audio_file_path(self):
        return f'output/tts_audio_{self.sentence_index}.mp3'