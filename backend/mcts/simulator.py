# simulator defines the rules of the game (mechanics)

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
import copy
import random

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
        self.possible_actions = list(initial_state.action_metadata.keys()) if hasattr(initial_state, "action_metadata") else []

        # initialize impact factors
        state_attributes = initial_state.attributes
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
        # Deep copy the current state
        new_state = copy.deepcopy(self.state)
        
        # Calculate reward for this action
        reward = self._calculate_reward(action)

        # Update action history in state
        if not hasattr(new_state, 'history'):
            new_state.history = []
        new_state.history.append(action)

        # check if game is over
        is_terminal = self._is_terminal()

        return new_state, reward, is_terminal
    
    def _calculate_reward(self, action: str) -> float:
        """
            Calculate the reward based on impact factors
            - output: reward value
        """
        reward = 0.0
        
        # Get action metadata from state
        action_metadata = self.state.action_metadata.get(action, {})
        
        # Risk factor: penalize high-risk actions if risk tolerance is low
        if action_metadata.get('is_high_risk', False):
            risk_penalty = 1 - self.impact_factors['risk']  # Higher risk tolerance = lower penalty
            reward -= risk_penalty
        
        # Time constraint factor: penalize long-term actions if time constraint is high
        if action_metadata.get('is_long_term', False):
            time_penalty = self.impact_factors['time-constraint']  # Higher time constraint = higher penalty
            reward -= time_penalty
        
        # Importance factor: boost reward based on importance
        importance_boost = self.impact_factors['importance']
        reward += importance_boost
        
        return reward
    
    def _is_terminal(self) -> bool:
        """
            Check if game reached terminal state (leaf node)
        """
        return len(self.state.history) >= len(self.possible_actions)
    
    def get_action(self) -> str:
        """
            Return a random action from the possible actions
        """
        return random.choice(self.possible_actions)
    
    def copy(self) -> 'Environment':
        """
            Return a deep copy of the environment
        """
        return copy.deepcopy(self)
