import streamlit as st
import httpx
import asyncio
import pandas as pd

from src.ui.upload_file import upload_file
from src.ui.get_data import get_data

st.title('Chatbot')
st.header('Current Vector DB')
st.dataframe(asyncio.run(get_data()))

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    asyncio.run(upload_file(uploaded_file)) 