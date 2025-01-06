from backend.agents.base_agent import BaseAgent, AgentMessage
from typing import List, Dict, Any
from backend.services.vector_store import VectorStore
import time
from backend.mcts.state import State
class TranslatorAgent(BaseAgent):
    """
        Agent that gathers information from the user and converts natural language to structured data with the following abilities:
        - process_input: gathers information from the user from the frontend
        - process_output: processes the message and returns to frontend
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
        # extract user input
        user_input = message.content["text"]
        attributes = message.content["attributes"]

        # get embeddings for user input
        embeddings = await self.vector_store.convert_embedding(user_input)
        
        try:
            # Store first before querying
            vector_id = await self.vector_store.store_embedding(
                message.content["text"], 
                metadata={"timestamp": time.time()}
            )
            
            # Then query
            query_response = await self.vector_store.query_embedding(user_input)
            similar_contexts = []
            
            if hasattr(query_response, 'matches'):
                similar_contexts = [
                    {
                        "id": match.id,
                        "score": match.score,
                        "metadata": match.metadata
                    } for match in query_response.matches
                ]
        except Exception as e:
            print(f"Error in vector operations: {e}")
            similar_contexts = []

        # create initial state object
        state = State(
            description=user_input,
            attributes=attributes,
            embedding=embeddings
        )

        # send to planner
        return AgentMessage(
            from_agent=self.name,
            to_agent="planner",
            content={"state": state, "contexts": similar_contexts},
            metadata={}
        )
    
    # Output workflow
    async def process_output_message(self, message: AgentMessage) -> AgentMessage:
        """ 
            Process the message returned from the planner and return nlp
            - message: message to process
        """
