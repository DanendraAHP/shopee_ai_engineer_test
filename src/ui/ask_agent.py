# import httpx

# async def ask_agent(query):
#     async with httpx.AsyncClient() as client:
#         payload = {"query": query}
#         response = await client.post(
#             url='http://be:12345/ask_llm',
#             json=payload, 
#             timeout=600
#         )
#     return response.json()['reponse']
from src.be.agent import call_agent
async def ask_agent(query):
    return await call_agent(query)