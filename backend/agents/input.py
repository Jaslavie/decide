from backend.agents.base_agent import BaseAgent, AgentMessage
from typing import List, Dict, Any
from backend.services.vector_store import VectorStore
import time
class TranslatorAgent(BaseAgent):
    """
        Agent that gathers information from the user and converts natural language to structured data with the following abilities:
        - get_user_input: gathers information from the user from the frontend
        - process_message: processes the message and returns a structured data
        - store_input: stores the input in the vector db by calling embedding services
    """

    def __init__(self):
        super().__init__(name="translator", role="translator")
        self.vector_store = VectorStore()
    
    # Input workflow
    async def process_input_message(self, message: AgentMessage) -> AgentMessage:
        """ 
            Process the message and return a structured data
            - message: message to process
        """
        if message.content.get("type") == "user_input":
            # store input in vector DB
            vector_id = await self.vector_store.store_embedding(
                message.content["text"], 
                metadata={"timestamp": time.time()}
            )

            # find similar past contexts
            similar_contexts = await self.vector_store.query_embedding(
                message.content["text"]
            )

            # created structured data for planner
            structured_data = {
                "vector_id": vector_id,
                "raw_text": message.content["text"],
                "similar_contexts": similar_contexts,
                "timestamp": time.time()
            }

            # send to planner
            return AgentMessage(
                from_agent=self.name,
                to_agent="planner",
                content=structured_data,
                metadata={"type": "processed_input"}
            )  
    
    # Output workflow
    async def process_output_message(self, message: AgentMessage) -> AgentMessage:
        """ 
            Process the message returned from the planner and return nlp
            - message: message to process
        """
