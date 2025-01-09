# short term memory storage

from typing import List, Dict, Any
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import time
from backend.services.llm import LLMService
import numpy as np

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
    """ 
    functions:
    - store interactions in short term
    - create insights about interactions
    - consolidate insights into long term memory
    """
    def __init__(self):
        self.interactions = [] # lightweight storage of user interactions and inputs (ex: questions asked, actions taken)
        self.long_term_memories = [] # long term memory storage of user insights and patterns
        self.consolidation_threshold = 0.8 # minimum confidence score to move to long term memory  

    async def store_interaction(self, text: str, metadata: Dict[str, Any] = None):
        """
            Store user interaction as a summary in short term memory
        """
        memory = Memory(
            text=text,
            timestamp=time.time(),
            type='interaction',
            metadata=metadata or {}
        )
        # create new memory item
        self.interactions.append(memory)
        # create a summary of the user's behavior and preferences
        await self._create_insight(memory)
        # store in short term memory
        await self._store_in_short_term_memory(memory)
    
    async def _create_insight(self, memory: Memory):
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
        
    async def consolidate_memories(self):
        """
        Move from short term memory patterns to long term memory storage in vector store
        """
        for memory in self.interactions:
            if memory.confidence > self.consolidation_threshold:
                # store in vector store
                await self.vector_store
        # keep only recent items 
        self.interactions = self.interactions[-10:]
    
    async def retrieve_memories(self, query: str) -> List[Memory]:
        """
        Retrieval mechanism to extract relevant long term memories to short term memory
        """
        


class MemoryCluster:
    """
    Group memory insights
    """
    def __init__(self, category: str):
        self.memories = [] # list of memories in a cluster
        self.category = category
        self.centroid = None # average of all memories in the cluster
        self.threshold = 0.7 # similarity to add memory to cluster

    def add_memory(self, memory, embedding):
        """ add a memory to the cluster if it's close to the centroid """
        if self.centroid is None:
            self.centroid = embedding
        
        # calculate distance between memory and centroid
        distance = self._calculate_distance(embedding, self.centroid)

        # if distance is less than a threshold, add to cluster
        if distance < self.threshold:
            self.memories.append(memory)

    def _calculate_distance(self, embedding1, embedding2):
        """ calculate the cosine distance between two embeddings """
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

        
