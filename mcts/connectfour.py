"""A Connect Four game"""

import numpy as np


class ConnectFourEnv:
    """An environment for two-player connect-four."""

    def __init__(self):
        self.players = 2
        self.reset()

    def reset(self):
        """Initialize a new game and return state and turn."""
        self.state = np.zeros((6, 7), dtype=np.int)
        self.done = False
        self.actions = list(range(7))
        self.turn = 0

    def step(self, action):
        """Perform action and return new state, rewards, done, and turn."""
        move=(max([i for i in range(6) if self.state[i,action]==0]),action)
        assert self.state[move] == 0
        self.state[move] = (-1) ** self.turn
        winner = self.winner(move)
        if winner is not None:
            rewards = np.array([winner,(-1)*winner])
        else:
            rewards = np.array([0,0])
        self.done = winner is not None or np.all(self.state != 0)
        self.turn = (self.turn + 1) % 2
        if self.done:
            self.actions = []
        else:
            self.actions = [i for i in range(7) if self.state[0,i]==0]
        return self.state.copy(), rewards, self.done, self.turn

    def copy(self):
        copy = ConnectFourEnv()
        copy.state = self.state.copy()
        copy.turn = self.turn
        copy.done = self.done
        copy.actions = self.actions.copy()
        return copy

    def render(self):
        print(self.state)

    def winner(self,move):
        if (self.rcheck(move),self.ccheck(move),self.dcheck(move),self.acheck(move))!=(0,0,0,0):
            return np.sign(self.state[move])
        return None
        
    def rcheck(self,move):
        for i in range(4):
            if np.sum(self.state[move[0]][i:i+4])==4*self.state[move]:
                return 1
        return 0    
            
    def ccheck(self,move):
        if np.sum(self.state[move[0]:min(move[0]+4,6),move[1]])==4*self.state[move]:
            return 1
        return 0
    
    def dcheck(self,move):
        l=self.state.copy().diagonal(move[1]-move[0])
        for i in range(len(l)-3):
            if np.sum(l[i:i+4])==4*self.state[move]:
                return 1
        return 0
    
    def acheck(self,move):
        l=self.state.copy()[::-1,:].diagonal(move[1]+move[0]-5)
        for i in range(len(l)-3):
            if np.sum(l[i:i+4])==4*self.state[move]:
                return 1
        return 0