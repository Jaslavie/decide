from backend.agents.base_agent import BaseAgent, AgentMessage
from typing import List, Dict, Any
from backend.services.vector_store import VectorStore
import time
from backend.mcts.state import State
import asyncio
from backend.services.memory_store import MemoryStore

class TranslatorAgent(BaseAgent):
    """
        Agent that gathers information from the user and converts natural language to structured data with the following abilities:
        - process_input: gathers information from the user from the frontend
        - process_output: processes the message and returns to frontend
    """

    def __init__(self):
        super().__init__(name="translator", role="translator")
        self.vector_store = VectorStore()
        self.memory_store = MemoryStore()
    
    # Input workflow
    async def process_input_message(self, message: AgentMessage) -> AgentMessage:
        """ 
            Process the message and return a structured data
            - message: message to process
        """
        # extract user input
        user_input = message.content["text"]
        attributes = message.content["attributes"]
        embeddings = None
        similar_contexts = []
        
        # Store interaction and get insights
        await self.memory_store.store_interaction(user_input, metadata=attributes)
        user_insights = self.memory_store.get_relevant_insights(user_input)
        
        try:
            # get embeddings for user input
            embeddings = await self.vector_store.convert_embedding(user_input)
            
            # Query for similar contexts but don't store current input
            query_response = await self.vector_store.query_embedding(embeddings)
            
            # Process query response and create a context list
            if isinstance(query_response, dict) and 'matches' in query_response:
                similar_contexts = [
                    {
                        "id": match.get("id"),
                        "text": match.get("metadata", {}).get("text", ""),
                        "score": match.get("score", 0.0),
                        "metadata": match.get("metadata", {})
                    } 
                    for match in query_response['matches']
                ]
                print(f"Found {len(similar_contexts)} relevant contexts")
                print(f"Context details: {similar_contexts}")
                
        except Exception as e:
            print(f"Error in vector operations: {str(e)}")
            embeddings = [0.0] * 1536  # Default embedding size

        # Create state with contexts
        state = State(
            description=user_input,
            attributes=attributes,
            embedding=embeddings
        )

        return AgentMessage(
            content={
                "state": state, 
                "contexts": similar_contexts,
                "insights": user_insights
            },
            from_agent=self.name,
            to_agent="planner",
            metadata={}
        )
    
    # Output workflow
    async def process_output_message(self, message: AgentMessage) -> AgentMessage:
        """ 
            Process the message returned from the planner and return nlp
            - message: message to process
        """
