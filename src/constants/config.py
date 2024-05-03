
# Chat
page_title = "Ankit's assistant"
initial_ai_msg = "Hello Ankit. How can I help you today?"
bot_avatar = "https://img.freepik.com/premium-photo/drawing-robot-with-helmet-gloves-generative-ai_733139-11125.jpg"
human_avatar = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvnitFAIH_gCZg3Nq_65oi87usR1duVCT3epuTLWbjmA&s"


# prompt
chat_prompt_template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

# TTS / STT
default_tts_voice = 0 # alloy
stt_audio_filepath = "output/stt_audio.wav"