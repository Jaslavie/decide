# long term memory storage

from typing import List, Dict, Any
import numpy as np
from openai import OpenAI
import os

class VectorStore:
    """
    Long term memory storage:
    - convert and store user insights as vectors
    - retrieve relevant memories to answer a query
    - reinforce frequently accessed memories
    """
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.vectors = []  # Store vectors in memory for now
        self.metadata = []  # Store corresponding metadata
        self.access_counts = {} # track access count for each memory

    async def convert_embedding(self, text: str) -> List[float]:
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            print("embedding response: ", response)
            return response.data[0].embedding
        except Exception as e:
            print(f"Error converting to embedding: {e}")
            return []

    async def store_embedding(self, text: str, metadata: Dict[str, Any] = None) -> str:
        embedding = await self.convert_embedding(text)
        if embedding:
            self.vectors.append(embedding)
            self.metadata.append(metadata or {})
            return str(len(self.vectors) - 1)  # Return index as ID
            print("embedding stored")
        return ""

    async def query_embedding(self, query_vector: List[float], top_k: int = 5) -> Dict:
        if not self.vectors or not query_vector:
            print("No vectors stored or invalid query vector")
            return {"matches": []}
        
        try:
            # Convert lists to numpy arrays
            query_array = np.array(query_vector)
            vectors_array = np.array(self.vectors)
            
            # Calculate similarities
            similarities = np.dot(vectors_array, query_array) / (
                np.linalg.norm(vectors_array, axis=1) * np.linalg.norm(query_array)
            )
            
            # Get top k indices
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            # create matches
            matches = []
            for idx in top_indices:
                matches.append({
                    "id": str(idx),
                    "text": self.metadata[idx].get("text", ""),
                    "score": float(similarities[idx]),
                    "metadata": self.metadata[idx]
                })
            
            print(f"Found {len(matches)} similar contexts")
            return {"matches": matches}
            
        except Exception as e:
            print(f"Error in similarity calculation: {e}")
            return {"matches": []}
    
    async def reinforce_memory(self, memory_id: str):
        """
        Reinforce a memory based on frequency of access
        """
        # increment access count
        self.access_counts[memory_id] = self.access_counts.get(memory_id, 0) + 1
        # update vector store by moving it to the front of the list
        self.vectors.insert(0, self.vectors.pop(memory_id))
