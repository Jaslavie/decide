from typing import List, Dict, Any
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time
from dotenv import load_dotenv
import os

class VectorStore:
    def __init__(self):
        load_dotenv()
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = "context"

        # create index if it doesn't exist
        if self.index_name not in pc.list_indexes():
            pc.create_index(
                name=self.index_name,
                dimension=1536, # gpt-4o-mini embedding dimension
                metric="cosine", # cosine similarity search
            )
        
        self.index = self.pc.Index(self.index_name)
    
    async def convert_embedding(self, text: str) -> List[float]:
        """
            convert input (text) into numerical vector embedding
            - text: input of text to convert
        """

        embeddings = self.pc.interface.embed(
            model="multilingual-e5-large",
            inputs=[text],
            parameters={"input_type": "passage", "truncate": "END"}
        )

        return embeddings[0]

    async def store_embedding(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """
            Store the embedding in the vector db
            - text: input of text to store
            - metadata: metadata to store with the vector
            - vector_id: time stamp used for temporal mapping
        """

        vector = await self.convert_embedding(text)
        vector_id = str(time.time()) 
        self.index.upsert(
            vectors=[(vector_id, vector, metadata or {})],
        ) 

        return vector_id

    async def query_embedding(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """ 
            Query the vector db for similar vectors through similarity search
            - query: input of text to query
            - top_k: number of similar vectors to return
        """

        query_vector = await self.convert_embedding(query)
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
        )

        return results
