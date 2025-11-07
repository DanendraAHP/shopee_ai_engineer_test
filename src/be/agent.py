from langchain.tools import tool
from src.be.setup import llm, vector_db
from datetime import datetime
import pandas as pd
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

@tool
def retrieve_trx(start_date:str, end_date:str):
    """Retrieve user previous food transactions. 
    From user query determine the start_date and end_date of the transaction they want to retrieve in regards with the current date.
    So the start and end date of the parameter must inclusively cover the transaction date the user want to see. For example:
    - what food did i buy yesterday : if current date is 2024-11-30 then start_date and end_date will be the same which is 2024-11-29
    - what food did i buy on 20 june : if current date is 2024-11-30 then start_date and end_date will be the same which is 2024-06-20
    - where do i buy ice cream this month : if current date is 2024-11-30 then start_date is 2024-11-01 and end date is 2024-11-30
    - what did i buy 3 days ago : if current date is 2024-11-30 then start_date is 2024-11-27 and end date is 2024-11-30
    Inp:
        - start_date (str) : the start date of transaction the user wants. The input format must be in YYYY-MM-DD
        - end_date (str) : the end date of transaction the user wants. The input format must be in YYYY-MM-DD
    Out:
        - List of dictionary containing user previous transactions from start_date to end_date inclusive
    """
    print(f'retrieve_trx : {start_date} {end_date}')
    df = pd.DataFrame(vector_db.get_item())
    df['date'] = pd.to_datetime(df['date'])
    df = df[
        (df['date']>=pd.to_datetime(start_date))&
        (df['date']<=pd.to_datetime(end_date))
    ]
    return df.to_dict(orient='records')

async def call_agent(query):
    tools = [retrieve_trx]
    # If desired, specify custom instructions
    prompt = (
        "You have access to a tool that retrieves user previous transactions "
        "Use the tool to help answer user queries with regards of the current date."
    )
    agent = create_agent(llm, tools, system_prompt=prompt)
    query = f"{query}\ncurrent date:{datetime.today().strftime('%Y-%m-%d')}"
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    return response['messages'][-1].content