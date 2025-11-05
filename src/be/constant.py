from pydantic import BaseModel
from typing_extensions import List
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
    
VECTOR_DB_JSON = 'data/vector_db.json'
VECTOR_DB_EMBEDDING_DIM = 128
VECTOR_DB_ADD_BATCH_SIZE = 3
llm = init_chat_model("gpt-5")