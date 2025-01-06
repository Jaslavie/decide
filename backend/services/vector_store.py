from pinecone import init, Index
from dotenv import load_dotenv
import os
from typing import List, Dict, Any
import time
import openai
import pinecone

class VectorStore:
    """
        Vector Store class for storing and querying embeddings used for reasoning. Embeddings contain:
        - context of the user's background and goals
        - decisions the user asks about
        - contingencies, tradeoffs, and external factors unique to the user's situation
    """

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
            
        # Initialize pinecone
        init(
            api_key=api_key,
            environment="gcp-starter"  # starter plan
        )
        
        self.index_name = "context"
        # Create index if it doesn't exist
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=self.index_name,
                dimension=1536, # gpt-4o-mini embedding dimension
                metric="cosine", # cosine similarity search
                # spec=ServerlessSpec(
                #     cloud="aws",
                #     region="us-east-1",
                #     memory="2gb",
                #     timeout="60s"
                # )
            )
        
        self.index = Index(self.index_name)
    
    async def convert_embedding(self, text: str) -> List[float]:
        """Convert text to embedding using OpenAI's API"""
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = await openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']

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
