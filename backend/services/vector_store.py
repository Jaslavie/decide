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

        Vector store:
        - index: id of the vector store
    """

    def __init__(self):
        try:
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
                try:
                    # Wait for index to be created
                    pinecone.create_index(
                        name=self.index_name,
                        dimension=1536,
                        metric="cosine"
                    )
                    time.sleep(10)  # Wait for index to be ready
                except Exception as e:
                    print(f"Error creating Pinecone index: {e}")
                    raise
            
            try:
                self.index = Index(self.index_name)
            except Exception as e:
                print(f"Error connecting to Pinecone index: {e}")
                raise
        except Exception as e:
            print(f"Critical error initializing VectorStore: {e}")
            raise
    
    async def convert_embedding(self, text: str) -> List[float]:
        """Convert text to embedding using OpenAI's API"""
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            print("Generated embedding for:", text[:50], "...", "sample:", response.data[0].embedding)  # Debug print
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise

    async def store_embedding(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """
            Store the embedding in the vector db
            - text: input of text to store
            - metadata: metadata to store with the vector
            - vector_id: time stamp used for temporal mapping
        """
        try:
            try:
                vector = await self.convert_embedding(text)
            except Exception as e:
                print(f"Error converting text to embedding: {e}")
                raise

            vector_id = str(time.time())
            
            # Debug print
            print(f"Attempting to upsert vector with id: {vector_id}")
            print(f"Vector length: {len(vector)}")
            print(f"Metadata: {metadata}")
            
            try:
                # Ensure vector is a list of floats
                vector = [float(v) for v in vector]
            except Exception as e:
                print(f"Error converting vector values to float: {e}")
                raise
            
            try:
                self.index.upsert(
                    vectors=[(vector_id, vector, metadata or {})],
                    namespace=""  # Explicitly set namespace
                )
            except Exception as e:
                print(f"Error upserting to Pinecone: {e}")
                raise
            
            print(f"Successfully upserted vector with id: {vector_id}")
            return vector_id
            
        except Exception as e:
            print(f"Critical error in store_embedding: {str(e)}")
            print(f"Vector type: {type(vector)}")
            print(f"First few values: {vector[:5]}")
            raise

    async def query_embedding(self, query_vector: List[float], top_k: int = 5) -> Dict:
        try:
            # Validate input vector
            if not query_vector or not isinstance(query_vector, list):
                print("Invalid query vector")
                return {"matches": []}

            # Print debug info
            print(f"Vector type: {type(query_vector)}")
            print(f"First few values: {query_vector[:5]}")

            try:
                results = self.index.query(
                    vector=query_vector,
                    top_k=top_k,
                    include_values=True,
                    include_metadata=True,
                    namespace=""
                )
                return results
            except Exception as e:
                print(f"Error in vector operations: {str(e)}")
                # Return empty results instead of failing
                return {"matches": []}

        except Exception as e:
            print(f"Critical error in query_embedding: {str(e)}")
            return {"matches": []}
