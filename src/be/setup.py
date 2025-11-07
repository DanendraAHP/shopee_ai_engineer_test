from src.be.vector_db import VectorDB
from langchain.chat_models import init_chat_model

llm = init_chat_model("gpt-5")
vector_db = VectorDB()