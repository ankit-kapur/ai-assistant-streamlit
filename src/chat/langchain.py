from langchain_openai import ChatOpenAI

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

from constants.config import chat_prompt_template, initial_ai_msg
from chat.tts import speakingHandler

def call_langchain(user_query, chat_history):

    prompt = ChatPromptTemplate.from_template(chat_prompt_template)

    llm = ChatOpenAI(
        streaming=True,
        temperature=st.session_state.llm_temperature, 
        max_tokens=st.session_state.llm_max_tokens,
        callbacks=[speakingHandler]
    )
    
    # Create Langchain
    chain = prompt | llm | StrOutputParser()
    
    # Invoke the chain
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })
