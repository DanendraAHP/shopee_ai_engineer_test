from fastapi import FastAPI, File, UploadFile
import aiofiles
import uuid

from src.be.upload_feature import upload_file
from src.be.vector_db import VectorDB

app = FastAPI()
vector_db = VectorDB()

@app.post("/upload_receipt")
async def upload_receipt(file: UploadFile = File(...)):
    try:
        filepath = file.filename
        print(filepath)
        async with aiofiles.open(filepath, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
        result = await upload_file(filepath, vector_db)
        return result
    except Exception as e:
        print(e)

@app.get("/get_data")
async def get_data():
    try:
        return vector_db.get_item()
    except Exception as e:
        print(e)