# import httpx

# async def upload_file(uploaded_file):
#     async with httpx.AsyncClient() as client:
#         payload = {"file": uploaded_file.name}
#         await client.post(
#             url='http://be:12345/upload_receipt',
#             params=payload, 
#             files={"file": uploaded_file.getvalue()},
#             timeout=600
#         )


import aiofiles
from src.be.setup import vector_db
from src.be.upload_feature import upload_file
async def upload_receipt(uploaded_file):
    try:
        filepath = uploaded_file.name
        async with aiofiles.open(filepath, 'wb') as out_file:
            content = uploaded_file.getvalue()  # async read
            await out_file.write(content)  # async write
        result = await upload_file(filepath, vector_db)
        return result
    except Exception as e:
        print(e)
        return {'error':str(e)}