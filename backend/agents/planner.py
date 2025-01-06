from backend.agents.base_agent import BaseAgent, AgentMessage
from typing import List, Dict, Any

class PlannerAgent(BaseAgent):
    """
        Agent that selects the best option to test in the simulation with the following abilities:
        - 
    """

    def __init__(self):
        super().__init__(name="planner", role="planner") 
        self._current_plan = None # sets the plan to test
    
