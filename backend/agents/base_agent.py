# Base Agent interface for all agents

from abc import ABC, abstractmethod 
from dataclasses import dataclass
from typing import List, Dict, Any
@dataclass
class AgentMessage:
    from_agent: str
    to_agent: str
    content: Any
    metadata: Dict[str, Any] 

class BaseAgent(ABC):
    """
    Base Agent class
    - ABC: Abstract Base Class
    """

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self._state = {} # initialize agent state
    

    async def _update_state(self, new_state: Dict[str, Any]) -> None:
        """ 
            Update the current agent's state 
            - Dict[str, _]: key of the state
            - Dict[_ , Any]: value of the state
        """
        self._state.update(new_state)
    
    
    