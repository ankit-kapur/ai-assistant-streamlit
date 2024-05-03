import streamlit as st

# Local packages
from constants.config import default_tts_voice

class SettingsBox:
    def draw(self, settings_tab):

        # ------------------------------------------------------- LLM Settings
        llm_settings = settings_tab.expander('LLM', expanded = True)
        llm_temperature = llm_settings.slider(
            "🎨 Temperature", 
            min_value=0.1, max_value=1.0, step=0.1, 
            value=0.5,
            key = "llm_temperature"
        )
        llm_max_tokens = llm_settings.number_input(
            "🛑 Token limit", 
            value=2000, 
            min_value=10, step=100,
            key = "llm_max_tokens"
        )

        # ------------------------------------------------------- TTS Settings
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