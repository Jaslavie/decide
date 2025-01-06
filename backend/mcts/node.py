# nodes on the tree representing a state
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import math
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Node:
    """
    Information each node holds and methods to interact with it
    Actions:
    - add child node
    - calculate ucb score of node using embeddings
    """
    def __init__(self, game, done, parent, action_index):
        self.child = []                             # list of child nodes 
        self.parent = parent                        # parent node
        self.state = None                           # state of the node
        self.game = game                            # set up the environment to play the game
        self.visits = 0                             # number of times the node has been visited
        self.wins = 0                               # number of rewards from exploration
        self.value = 0                              # average value of the node
        self.action_index = action_index            # index of the action that led to this node
        self.done = done                            # whether the node is terminal
    
    def create_child(self):
        """
        Create a child node for each possible action and test it in a simulation to get a score
        """
        if self.done:
            return
        
        # play a simulation for each action
        actions = []
        games = []
        for i in self.game.get_actions():
            actions.append(i)
            new_game = self.game.copy()
            games.append(new_game)
        
        # run the simulations on the actions and game environments
        child = {}
        for action, game in zip(actions, games):
            child[action] = Node(game, done = game.done, parent = self, action_index = action)
        
        # add ALL child nodes and results of the game to the current node 
        self.child = child
    
    def get_ucb_score(self, exploration_constant: float = 1.41) -> float:
        """ 
        Calculate the UCB score to inform the selection of the best node
        - state embedding: context of the user's background
        - goal embedding: context of the user's goals
        - user preferences: extracted from user input (ex: risk-aversion)
        """
        # if the node has not been visited (favor exploration)
        if self.visits == 0:
            return float('inf')
        
        # calculate the exploration and exploitation
        # ubc formula
        exploration = self.value / self.visits
        exploitation = exploration_constant * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )

        # extract embeddings 
        embedding_bonus = 0.0 # bonus added to score 
        if hasattr(self.state, "embedding") and hasattr(self.game, 'goal_embedding'):
            similarity = cosine_similarity(
                self.state.embedding,
                self.game.goal_embedding
            )
            embedding_bonus = similarity * 0.5 # importance of user context
        
        # add user preferences to weighting
        preference_bonus = 0.0
        if hasattr(self.state, 'attributes'):
            preferences = self.game.user_preferences # dict of attribute weights
            for attr, weight in preferences.items():
                if attr in self.state.attributes: 
                    preference_bonus += self.state.attributes[attr] * weight

        # calculate the score
        score = exploitation + exploration + embedding_bonus + preference_bonus
        return score