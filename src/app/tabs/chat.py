import os
import base64
import time
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from chat.langchain import call_langchain

from chat.stt import draw_mic
from constants.config import initial_ai_msg, human_avatar, bot_avatar

class ChatBox:

    def draw(self, chat_tab):

        # ------------------------  Structure of the chat tab
        self.chat_feed_container = chat_tab.container(border=True, height=500)

        # chat_input_column, mic_button_column = chat_tab.columns([5, 1])
        self.input_box_container = chat_tab.container(height=None, border=False)
        self.mic_button_container = chat_tab.container(height=None, border=False)

        # Init chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(content=initial_ai_msg),
            ]

        # conversation
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with self.chat_feed_container.chat_message("AI", avatar=bot_avatar):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with self.chat_feed_container.chat_message("Human", avatar=human_avatar):
                    st.write(message.content)


        # Text input box
        user_query = self.input_box_container.chat_input("Type your message here...")
        if user_query is not None and user_query != "":
            self.send_text_to_bot(user_query)

        # Mic
        draw_mic(self)


    def send_text_to_bot(self, text_message):
        st.session_state.chat_history.append(HumanMessage(content=text_message))

        with self.chat_feed_container.chat_message("Human", avatar=human_avatar):
            st.markdown(text_message)

        with self.chat_feed_container.chat_message("AI", avatar=bot_avatar):
            # with st.spinner("Generating response..."):
            response = st.write_stream(
                call_langchain(
                    text_message, 
                    st.session_state.chat_history))

            st.session_state.chat_history.append(
                AIMessage(content=response))