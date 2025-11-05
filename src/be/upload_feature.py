from src.be.extract_receipt import extract_receipt
import os

async def upload_file(filepath, vector_db):
    try:
        print('extracting receipt')
        receipts = await extract_receipt(filepath)
        if receipts:
            vector_db.add_item(receipts)
            return {"Items Added" : len(receipts)}
        os.remove(filepath)
    except Exception as e:
        print(e)
        return {"Items Added" : 0, "Error":e}