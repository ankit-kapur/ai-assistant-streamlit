from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

from constants.config import chat_prompt_template, initial_ai_msg
from chat.tts import speakingHandler

def call_langchain(user_query, chat_history):

    prompt = ChatPromptTemplate.from_template(chat_prompt_template)

    openai_llm = ChatOpenAI(
        streaming=True,
        temperature=st.session_state.llm_temperature, 
        max_tokens=st.session_state.llm_max_tokens,
        callbacks=[speakingHandler]
    )

    # TODO: Fix
    '''
    ConnectionError: HTTPConnectionPool(host='localhost', port=11434): 
        Max retries exceeded with url: /api/chat/ 
            (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0xffff247c5210>: 
            Failed to establish a new connection: [Errno 111] 
            Connection refused'))
    '''
    # ------------------------------------------ Ollama
    # Source: https://python.langchain.com/docs/integrations/chat/ollama/
    ollama_llm = ChatOllama(
        model="llama3",
        base_url= "http://localhost:11434",
        temperature=st.session_state.llm_temperature, 
        # max_tokens=st.session_state.llm_max_tokens,
        callbacks=[speakingHandler]
    )
    
    # Create Langchain
    chain = prompt | openai_llm | StrOutputParser()
    
    # Invoke the chain
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })
