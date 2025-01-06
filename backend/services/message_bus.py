# Message routing service to enable communication between agents
from typing import Dict, List, Any
from dataclasses import dataclass
from backend.agents.base_agent import AgentMessage

class MesassageBus:
    def __init__(self):
        """ 
            Initialize a list of subscribers to each agents
            - callable: functions in the agent that can be called
        """
        self._subscribers: Dict[str, List[callable]] = {} 
    
    async def publish(self, message: AgentMessage) -> None:
        """ 
            Publish a message to the message bus if the agent is subscribed
            - callback: function called when a message is received
        """
        if message.to_agent in self._subscribers:
            for callback in self._subscribers[message.to_agent]:
                await callback(message)
    
    def subscribe(self, agent_name: str, callback: callable) -> None:
        """
            Subscribe to a message bus
            - agent_name: agent that will subscribe to the message bus
        """
        if agent_name not in self._subscribers:
            self._subscribers[agent_name] = []
        self._subscribers[agent_name].append(callback)
            