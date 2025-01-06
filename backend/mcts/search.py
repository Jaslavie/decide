# main search algorithm implementation defining the strategy for winning the game
from dataclasses import dataclass
from typing import Any
from .node import Node
import random

@dataclass
class Search:
    def __init__(self, game, exploration_constant: float = 1.41, done: bool = False):
        self.game = game
        self.exploration_constant = exploration_constant
        self.root = Node(game, done, parent=None, action_index=None)
    
    def explore(self):
        """
            Explore the game tree by selecting nodes
            - recursively select the best node based on the UCB score
            - expand the node by creating child nodes
            - simulate the game from the child node
            - backpropagate the results of the simulation to the parent node
            - rollout simulates the game until the end
            - a leaf node has no children

        """
        # Start from root node instead of self
        current = self.root

        #* selection: recursively select the best child nodes until a leaf node is found
        while current.child:
            child = current.child
            max_score = max(c.get_ubc_score() for c in child.values()) # retrieve the child with scores that meet the ubc threshold
            actions = [                                                # retrieve the action that led to the best children
                a for a, c in child.items() if c.get_ubc_score() == max_score
            ]

            if len(actions) == 0:
                print("No best node found")
                break

            action = random.choice(actions) # select a random action from the best nodes if there are multiple
            current = child[action]         # select the child node

        #* action: play a game or expand the node
        if current.visits < 1:
            current.wins = current.wins + self.rollout(current)     # Pass current node to rollout
        else:
            current.create_child()
            if current.child:
                current = random.choice(list(current.child.values()))
            current.wins = current.wins + self.rollout(current)     # Pass node to rollout
        
        current.visits += 1
        
        #* backpropagation: backpropagate the results of the sim when a leaf node is reached
        parent = current

        while parent.parent:
            parent = parent.parent
            parent.visits += 1
            parent.wins += current.wins  # update the parent node with results from sim at the leaf node

    def rollout(self, node) -> float:
        """
            Simulate the game until the end for each node
            - node: node to run a simulator on
        """
        if node.done:
            return 0  

        # simulate the game
        wins = 0
        done = False
        new_game = node.game.copy()

        while not done:
            action = new_game.get_action()
            _, reward, done = new_game.step(action) 
            wins += reward
            if done:
                new_game.reset()
                new_game.close()
                break
        
        return wins
        

        
