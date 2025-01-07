# stores memory about the user interactions and context

from typing import List, Dict, Any
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import time
from backend.services.llm import LLMService
# base class for memory storage
@dataclass
class Memory:
    text: str
    timestamp: float
    type: str # 'interaction' or 'context'
    metadata: Dict[str, Any]

# class for user insight
@dataclass
class UserInsight:
    category: str # 'behavior', 'preference', 'pattern', 'goal'
    description: str
    confidence: float # confidence score of the insight
    timestamp: float

class MemoryStore:
    def __init__(self):
        self.interactions = [] # lightweight storage of user interactions and inputs (ex: questions asked, actions taken)
        self.insights = [] # key summaries about user preferences and behaviors (ex: user is interested in building a product)
        self.llm = LLMService()

    async def store_interaction(self, text: str, metadata: Dict[str, Any] = None):
        """
            Store user interaction as a summary
        """
        memory = Memory(
            text=text,
            timestamp=time.time(),
            type='interaction',
            metadata=metadata or {}
        )
        self.interactions.append(memory)
        await self._update_summaries(memory)
    
    async def _update_summaries(self, memory: Memory):
        """
            Create a summary of the user's behavior and preferences
        """
        if memory.type != 'interaction':
            return
        
        # get recent interactions
        recent_interactions = [m.text for m in self.interactions[-5:]]

        # extract insights from interaction
        prompt = f"""
            You are an expert at summarizing user behavior and preferences.
            You will be given a summary of a user's interactions and patterns of input over time.
            This should describe a unique insight about the user.

            Current interaction: "{memory.text}"
            Recent interactions taken by the user: {recent_interactions}

            Generate insights in this JSON format:
            [{{
                "category": "behavior|preference|goal|pattern",
                "description": "Clear insight about the user",
                "confidence": 0.0-1.0 based on the confidence level of your insight
                "timestamp": return current timestamp
            }}]
            
            Here are some examples of good descriptions:
            - The user is currently interning at Palantir as a Product Design Intern
            - The user enjoys going to hackathons and building a product from 0 to 1
            - The user has been working on a chrome extension tool for the past 3 months
        """

        # generate insights
        try:
            insights = await self.llm.generate_json(prompt)
            
            for insight in insights:
                self.insights.append(UserInsight(
                    category=insight["category"],
                    description=insight["description"],
                    confidence=float(insight["confidence"]),
                    timestamp=time.time()
                ))

            # Filter insights
            self.insights = [
                i for i in self.insights 
                if i.confidence > 0.7
            ]

        except Exception as e:
            print(f"Error updating insights: {e}")

    def get_relevant_insights(self, query: str) -> List[Dict[str, Any]]:
        return [
            {
                "category": i.category,
                "description": i.description,
                "confidence": i.confidence,
                "timestamp": i.timestamp
            }
            for i in self.insights
        ]
        

