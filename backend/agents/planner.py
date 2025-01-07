from backend.agents.base_agent import BaseAgent, AgentMessage
from typing import List, Dict, Any
from backend.mcts.simulator import Environment
from backend.mcts.search import Search
from backend.agents.philosopher import PhilosopherAgent
from backend.mcts.state import State
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
            if not isinstance(state, State):
                print("Invalid state object received")
                return ["Unable to process request - invalid state"]
            
            contexts = message.content.get("contexts", []) # extracted from vector store
            insights = message.content.get("insights", []) # extracted from memory store
            print("contexts used in planning: ", contexts)
            print("insights used in planning: ", insights)
            print("states used in planning: ", state.__dict__)  # Print full state details

            # generate possible decisions
            try:
                possible_actions = await self.philosopher.generate_actions(state, contexts, insights)
                print("possible actions: ", possible_actions)
            except Exception as e:
                print(f"Error in philosopher.generate_actions: {str(e)}")
                return ["Unable to generate optimal plan. Please try again."]

            # update state with actions
            try:
                if not hasattr(state, '_classify_actions'):
                    print("State object missing _classify_actions method")
                    return ["Unable to process request - invalid state object"]
                
                state._classify_actions(possible_actions)
            except Exception as e:
                print(f"Error classifying actions: {e}")
                return ["Unable to process request - action classification failed"]

            # initialize MCTS with fewer simulations for testing
            self.num_simulations = 3  # Reduce from 1000 to 3 for testing
            
            try:
                env = Environment(state, constraints={})
                search = Search(game=env)
                print("initialized MCTS with state: ", state)
                
                print("\nRunning simulations...")
                for i in range(self.num_simulations):
                    try:
                        print(f"\nSimulation {i+1}:")
                        
                        search.explore()
                        print(f"Simulation {i+1} completed")
                        
                        # Print simulation results
                        print(f"Node visits: {search.root.visits}")
                        print(f"Node wins: {search.root.wins}")
                        
                    except Exception as e:
                        import traceback
                        print(f"Error in simulation {i}: {str(e)}")
                        print("Full trace:")
                        print(traceback.format_exc())
                        continue
                        
            except Exception as e:
                print(f"Error in MCTS setup: {str(e)}")
                return ["Unable to generate optimal plan. Please try again."]

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
