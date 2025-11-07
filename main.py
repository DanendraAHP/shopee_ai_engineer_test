import streamlit as st
import httpx
import asyncio
import pandas as pd

from src.ui.upload_file import upload_receipt
from src.ui.get_data import get_data
from src.ui.ask_agent import ask_agent

st.title('Chatbot')
st.header('Current Vector DB')
st.dataframe(asyncio.run(get_data()))

st.header('Input Your Online Food Receipt Here')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    asyncio.run(upload_receipt(uploaded_file)) 

st.header('Ask LLM About Your Previous Transactions')
prompt = st.chat_input("Ask something")
if prompt:
    llm_response = asyncio.run(ask_agent(prompt)) 
    st.write(llm_response)
