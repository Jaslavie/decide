from backend.agents.base_agent import BaseAgent, AgentMessage
from typing import List, Dict, Any

class PlannerAgent(BaseAgent):
    """
        Agent that finds the optimal plans by running Monte Carlo Simulations. It has the following abilities:
        - create_plan: creates a plan for each decision
        - run_simulation: runs a simulation with the given plan
        - analyze_simulation: analyze each node of the simulation and provide feedback using the Philosopher agent
        - make_selection: select the best plan and return trade offs with the commander agent
    """

    def __init__(self):
        super().__init__(name="planner", role="planner") 
        self._current_plan = None # sets the plan to test
    
