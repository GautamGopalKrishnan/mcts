"""A Connect 4 game."""

import numpy as np


class ConnectFourEnv:
    """An environment for two-player connect-four."""

    def __init__(self, state=None, turn=None):
        self.state = np.zeros((6, 7), dtype=np.int) if state is None else state
        self.players = 2
        self.turn = 0 if turn is None else turn

    def reset(self):
        """Initialize a new game and return state and turn."""
        self.state = np.zeros((6, 7), dtype=np.int)
        self.turn = 0
        return self.state.copy(), self.turn

    def step(self, action):
        """Perform action and return new state, rewards, done, and turn."""
        assert self.state[action] == 0
        self.state[action] = (-1) ** self.turn
        if self.done:
            winner = self.winner(action)
            if winner is not None:
                rewards = np.array([winner,(-1)*winner])
            else:
                rewards = np.array([0,0])
        self.turn = (self.turn + 1) % 2
        return self.state.copy(), rewards, self.done, self.turn

    def copy(self):
        copy = ConnectFourEnv()
        copy.state = self.state.copy()
        copy.turn = self.turn
        return copy

    def render(self):
        print(self.state)

    def winner(self,action):
        if (self.rcheck(action),self.ccheck(action),self.dcheck(action),self.acheck(action))!=(0,0,0,0):
            return np.sign(self.state[action])
        return None
        
    def rcheck(self,action):
        for i in range(4):
            count=0
            for j in range(3):
                if self.state[action,i+j]==self.state[action,i]:
                    count=count+1
            if count==4:
                return np.sign(self.state[r,i])
        return 0    
            
    def ccheck(self,action):
        count=0
        for i in range(4):
            if self.state[action[0]+i,action[1]]==self.state[action]:
                count=count+1
        if count==4:
            return np.sign(self.state[action])
        return 0
    
    def dcheck(self,action):
        return 0
    """Code this"""
    
    def acheck(self,action):
        return 0
    """code this"""

    @property
    def actions(self):
        """The available actions for the current state."""
        if self.done:
            return []
        l=[]
        for b in range(6):
            for a in range(7):
                if self.state[a,b]==0:
                    if a==6:
                        l.append((a,b))
                    elif self.state[a+1,b]!=0:
                        l.append((a,b))
        return l

    @property
    def done(self):
        """True if three in a row somewhere."""
        return self.winner() is not None or np.all(self.state != 0)