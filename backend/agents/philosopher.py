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
    
    async def generate_actions(self, state, contexts: List[Dict], insights: List[Dict]):
        """
            Generate possible actions for the user to take in a string array
        """
        # Truncate contexts and insights to prevent token overflow
        context_summary = [
            f"{ctx.get('text', '')}(score:{ctx.get('score', 0):.2f})" 
            for ctx in contexts[:3]  # Only use top 3 contexts
        ]
        insight_summary = [
            f"{ins.get('description', '')}" 
            for ins in insights[:3]  # Only use top 3 insights
        ]
        
        prompt = f"""
            You are a philosopher that generates possible actions for the user.
            The user is trying to make a decision about {state.description}.
            The user has the following background: {contexts} and {insights}.
            Here is additional information about the user's risk tolerance, time constraints, and importance of the decision: {state.attributes}.
            
            Generate 5-10 possible actions for the user to take in a list of strings.
            - Each action should be no more than 100 characters long.
            - Return the list of actions in a list of strings only and nothing else.
            - align with the user's behavorial patterns and preferences
            - builds on previous experience
        """
        try:
            actions = await self.llm.generate(prompt)

            # clean up the array
            cleaned_actions = []
            for action in actions:
                action = ''.join(e for e in action if e.isalnum() or e.isspace())
                action = action.strip()
                if action and not action.isspace():
                    cleaned_actions.append(action)

            return cleaned_actions
        except Exception as e:
            print(f"Error in philosopher.generate_actions: {e}")
            return []
    

