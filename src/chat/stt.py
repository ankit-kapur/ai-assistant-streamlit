
import whisper
import streamlit as st
from constants.config import stt_audio_filepath

# https://github.com/theevann/streamlit-audiorecorder
from audiorecorder import audiorecorder

# Alternate libraries
# https://github.com/stefanrmmr/streamlit-audio-recorder
# from st_audiorec import st_audiorec
# For continuous stream, see: https://github.com/whitphx/streamlit-stt-app/blob/main/app_deepspeech.py

def draw_mic(chat_box):
    # STT (Whisper)
    whisper_model = whisper.load_model("base") # base works just fine

    with chat_box.mic_button_container:
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
        chat_box.send_text_to_bot(result["text"])
