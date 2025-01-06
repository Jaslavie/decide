# simulator defines the rules of the game (mechanics)

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

@dataclass
class Environment:
    """
        Game environment design for the simulation. The goal of the game is to reach the terminal state
        Functions:
        - step function: taking an action
        - reward function: calculate reward
        - terminal state: check if the game is over

        Attributes:
        - state: the history of all actions taken in the game

    """
    state: Dict[str, Any] # contains the current state of the game
    possible_actions: List[str]    # contains the possible actions the user can take
    constraints: Dict[str, Any] # contains user-defined constraints of the game
    impact_factors: Dict[str, Any] # contains user-defined impact factors

    def __init__(self, initial_state: Dict[str, Any], constraints: Dict[str, Any]):
        self.state = initial_state
        self.constraints = constraints
        self.possible_actions = []

        # initialize impact factors
        state_attributes = initial_state.get("attributes", {})
        self.impact_factors = {
            "risk": state_attributes.get("risk", 0.5),
            "time-constraint": state_attributes.get("time-constraint", 0.5),
            "importance": state_attributes.get("importance", 0.5)
        }

    def step(self, action: str) -> Tuple[Dict[str, Any], float, bool]:
        """ 
            Execute action and return a new state, reward, and done flag
            - action: action to be executed
            - returns: (new_state, reward, is_terminal)
        """
        new_state = self.state.copy()

        # simulate outcome of actions
        reward = self._calculate_reward(action)

        # update state of game
        new_state["history"] = new_state.get("history", []) + [action]

        # check if game is over
        is_terminal = self._is_terminal()

        return new_state, reward, is_terminal
    
    def _calculate_reward(self, action: str) -> float:
        """
            Calculate the reward based on impact factors
            - output: reward value
        """
        base_reward = 0.0

        # risk
        risk_factor = self.impact_factors["risk"]
        if action in self.state.get("high_risk_actions", []):
            base_reward += (1 - risk_factor) * - 1.0 # penalize risk-aversion
        
        # time 
        time_factor = self.impact_factors["time-constraint"]
        if action in self.state.get("long_term_actions", []):
            base_reward += time_factor * 0.5 # bonus for long-term actions

        # importance
        importance_factor = self.impact_factors["importance"]
        base_reward *= (1 * importance_factor) # scale reward by importance

        return base_reward
    
    def _is_terminal(self) -> bool:
        """
            Check if game reached terminal state (leaf node)
        """
        return len(self.state["history"]) >= len(self.possible_actions)