import httpx

async def upload_file(uploaded_file):
    async with httpx.AsyncClient() as client:
        payload = {"file": uploaded_file.name}
        await client.post(
            url='http://0.0.0.0:12345/upload_receipt',
            params=payload, 
            files={"file": uploaded_file.getvalue()},
            timeout=600
        )