from langchain_openai import OpenAIEmbeddings
from typing_extensions import List, Dict
import json

from src.be.constant import VECTOR_DB_JSON, VECTOR_DB_EMBEDDING_DIM, VECTOR_DB_ADD_BATCH_SIZE


class VectorDB:
    def __init__(self, embedding_dimension:int=VECTOR_DB_EMBEDDING_DIM, add_batch_size:int=VECTOR_DB_ADD_BATCH_SIZE):
        try:
            with open(VECTOR_DB_JSON, 'r') as f:
                self.table = json.load(f)
        except:
            print('Initializing Empty Table')
            self.table = []
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            dimensions=embedding_dimension
        )
        self.add_batch_size = add_batch_size

    def add_item(self, receipts:List[Dict]):
        for i in range(0, len(receipts), self.add_batch_size):
            batch_receipt = receipts[i:i+self.add_batch_size]
            batch_description = [receipt['description'] for receipt in batch_receipt]
            batch_embeddings = self.make_embedding(batch_description)
            self.table.extend([{**batch_receipt[batch_idx], 'embeddings':batch_embeddings[batch_idx]} for batch_idx in range(len(batch_receipt))])
        with open(VECTOR_DB_JSON, 'w') as fp:
            json.dump(self.table, fp)

    def get_item(self):
        return [{k:v for k,v in data.items() if k!='embeddings'} for data in self.table]

    def make_embedding(self, texts:List[str]):
        return self.embeddings.embed_documents(texts) 
    
    def dot_product(self, l1, l2):
        assert len(l1)==len(l2), f"Array size not same, len l1 {len(l1)} len l2 {len(l2)}"
        dot_result = 0
        for i in range(len(l1)):
            dot_result+=(l1[i]*l2[i])
        return dot_result
    
    def magnitude(self, l):
        sum_l = 0
        for i in range(len(l)):
            sum_l+=l[i]**2
        return sum_l**0.5
    
    def calculate_distance(self, embedding_1:List, embedding_2:List):
        return self.dot_product(embedding_1, embedding_2)/(self.magnitude(embedding_1)*self.magnitude(embedding_2))
    
    def search(self, query:str, top_n:int):
        query_embedding = self.make_embedding([query])[0]
        top_n_results = []
        for i,receipt in enumerate(self.table):
            distance = self.calculate_distance(query_embedding, receipt['embeddings'])
            if len(top_n_results)>top_n:
                if distance>top_n_results[-1]['distance']:
                    top_n_results[-1] = {'index':i, 'distance':distance}
                    top_n_results = sorted(top_n_results, key=lambda x:x['distance'], reverse=True)
            else:
                top_n_results.append({'index':i, 'distance':distance})
                top_n_results = sorted(top_n_results, key=lambda x:x['distance'], reverse=True)
        print(top_n_results)
        top_n_results = [{k:v for k,v in self.table[top_n['index']].items() if k!='embeddings'} for top_n in top_n_results]
        return top_n_results