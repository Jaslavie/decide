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
        try:
            state = message.content["state"]
            contexts = message.content.get("contexts", []) 
            print("contexts used in planning: ", contexts)
            print("states used in planning: ", state)

            # generate possible decisions
            try:
                possible_actions = await self.philosopher.generate_actions(state, contexts)
                print("possible actions: ", possible_actions)
            except Exception as e:
                print(f"Error in philosopher.generate_actions: {str(e)}")
                return ["Unable to generate optimal plan. Please try again."]

            # update state with actions
            state._classify_actions(possible_actions)

            # initialize MCTS
            try:
                env = Environment(state, constraints={})
                search = Search(game=env)
                print("initialized MCTS")
            except Exception as e:
                print(f"Error in initializing MCTS: {str(e)}")
                return ["Unable to generate optimal plan. Please try again."]

            # run simulations
            for _ in range(self.num_simulations):
                try:
                    search.explore()
                    print(f"Simulation {_} completed")
                except Exception as e:
                    print(f"Error in simulation {_}: {str(e)}")
                    continue  # Skip failed simulation and continue with next one

            # get best paths - fallback to possible actions if no paths found
            try:
                best_paths = search.get_best_paths()
            except Exception as e:
                print(f"Error getting best paths: {str(e)}")
                best_paths = possible_actions  # Fallback to raw actions

            # analyze paths with reasoning agent
            try:
                analyzed_paths = await self.philosopher.analyze_paths(best_paths)
            except Exception as e:
                print(f"Error in path analysis: {str(e)}")
                return best_paths  # Return unanalyzed paths as fallback

            return analyzed_paths

        except Exception as e:
            print(f"Critical error in planning: {str(e)}")
            # Return a basic response rather than failing completely
            return ["Unable to generate optimal plan. Please try again."]
