# reasoning agent to analyze each step of the simulation with context of previous steps to make a decision

from backend.agents.base_agent import BaseAgent, AgentMessage
from backend.services.llm import LLMService
from typing import List, Dict
class PhilosopherAgent(BaseAgent):
    """
        Actions:
        - analyze_node: analyze each node based on previous nodes, current state, and embeddings
    """
    def __init__(self):
        super().__init__(name="philosopher", role="philosopher")
        self.llm = LLMService()
    
    async def generate_actions(self, state, contexts: List[Dict]):
        """
            Generate possible actions for the user to take in a string array
        """
        prompt = f"""
            You are a philosopher that generates possible actions for the user.
            The user is trying to make a decision about {state.description}.
            The user has the following background: {contexts}.
            Generate 5-10 possible actions for the user to take.
        """
        actions = await self.llm.generate(prompt)

        return actions
    

