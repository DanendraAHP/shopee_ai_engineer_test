import httpx
import pandas as pd

async def get_data():
    async with httpx.AsyncClient() as client:
        data = await client.get(
            url='http://0.0.0.0:12345/get_data'
        )
    if data.status_code==200:
        return pd.DataFrame(data.json())
    else:
        return pd.DataFrame()