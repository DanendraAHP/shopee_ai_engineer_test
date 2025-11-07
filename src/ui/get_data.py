# import httpx
# import pandas as pd

# async def get_data():
#     async with httpx.AsyncClient() as client:
#         data = await client.get(
#             url='http://be:12345/get_data'
#         )
#     if data.status_code==200:
#         return pd.DataFrame(data.json())
#     else:
#         return pd.DataFrame()

import pandas as pd
from src.be.setup import vector_db
async def get_data():
    return pd.DataFrame(vector_db.get_item())