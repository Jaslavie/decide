from backend.agents.base_agent import BaseAgent, AgentMessage
from typing import List, Dict, Any
from backend.mcts.simulator import Environment
from backend.mcts.search import Search
from backend.agents.philosopher import PhilosopherAgent

class PlannerAgent(BaseAgent):
    """
        Agent that finds the optimal plans by running Monte Carlo Simulations. It has the following abilities:
        - plan: selects decisions and creates a plan for each (i.e. a branch of the tree) by calling the philosopher agent
        - run_simulation: runs a simulation with the given plan by calling the mcts simulator
        - analyze: analyze each node of the simulation and provide feedback using the Philosopher agent
        - make_selection: select the best plan and return trade offs with the commander agent
    """

    def __init__(self):
        super().__init__(name="planner", role="planner") 
        self._current_plan = None # sets the plan to test
        self.num_simulations = 1000
        self.philosopher = PhilosopherAgent()
    
    async def plan(self, message: AgentMessage):
        """ 
            Input: 
            - message from translator agent (attributes selected, context embeddings)
        """
        state = message.content["state"]
        contexts = message.content["contexts"]

        # generate possible decisions
        possible_actions = await self.philosopher.generate_actions(state, contexts)

        # update state with actions
        state.classify_actions(possible_actions)

        # initialize MCTS
        env = Environment(state, constraints={})
        search = Search(env)

        # run simulations
        for _ in range(self.num_simulations):
            search.explore()
        
        # get best paths
        best_paths = search.get_best_paths()

        # analyze paths with reasoning agent
        analyzed_paths = await self.philosopher.analyze_paths(best_paths)

        return analyzed_paths
