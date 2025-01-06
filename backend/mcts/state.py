# represent the current state of the game. created by the translator
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class State:
    """
    stored:
    - embedding: vector representation of the state
    - attributes: user preferences set on the front end
    extracted from:
    - user input
    - vector store
    """
    embedding: List[float]
    attributes: Dict[str, float] # contains the user-selected score for risk, time_constraint, importance weights
    description: str
    action_metadata: Dict[str, Dict[str, bool]] # classifies each action

    def __init__(self, description: str, attributes: Dict[str, float], embedding: List[float], actions: List[str] = None):
        self.description = description
        self.embedding = embedding

        # allocate weights for attributes
        default_attributes = {
            'risk': 0.5,
            'time-constraint': 0.5,
            'importance': 0.5
        }
    
        # update default attributes with user-defined attributes
        default_attributes.update(attributes)
        self.attributes = default_attributes

        # initialize action metadata
        self.action_metadata = {}
        if actions:
            self.classify_actions(actions)
    
    def _classify_actions(self, actions: List[str]):
        """ 
            Classify actions into high-risk, long-term, etc. based on user preferences
        """
        for action in actions:
            self.action_metadata[action] = {
                'is_high_risk': self._evaluate_risk(action),
                'is_long_term': self._evaluate_time_constraint(action)
            }
    
    def _evaluate_risk(self, action: str) -> bool:
        """
            Actions are high risk if the selected risk score is over 0.5
        """
        return self.attributes['risk'] > 0.5

    def _evaluate_time_constraint(self, action: str) -> bool:
        """
            Actions are long-term if the selected time constraint score is over 0.5
        """
        return self.attributes['time-constraint'] > 0.5
