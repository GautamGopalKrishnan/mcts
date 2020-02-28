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

    def winner(self,action):
        if (self.rcheck(action),self.ccheck(action),self.dcheck(action),self.acheck(action))!=(0,0,0,0):
            return np.sign(self.state[action])
        return None
        
    def rcheck(self,action):
        for i in range(4):
            count=0
            for j in range(4):
                if self.state[action[0],i+j]==self.state[action]:
                    count=count+1
                else:
                    break
            if count==4:
                return 1
        return 0    
            
    def ccheck(self,action):
        count=0
        for i in range(4):
            if action[0]+i<6 and self.state[action[0]+i,action[1]]==self.state[action]:
                count=count+1
            else:
                break
        if count==4:
            return 1
        return 0
    
    def dcheck(self,action):
        count=1
        while count!=4:
            if action[0]-count>=0 and action[1]-count>=0 and self.state[action[0]-count,action[1]-count]==self.state[action]:
                count=count+1
            else:
                break
        i=1
        while count!=4:
            if action[0]+i<6 and action[1]+i<7 and self.state[action[0]+i,action[1]+i]==self.state[action]:
                count=count+1
                i=i+1
            else:
                break
        if count==4:
            return 1
        return 0
    
    def acheck(self,action):
        count=1
        while count!=4:
            if action[0]-count>=0 and action[1]+count<7 and self.state[action[0]-count,action[1]+count]==self.state[action]:
                count=count+1
            else:
                break
        i=1
        while count!=4:
            if action[0]+i<6 and action[1]-i>=0 and self.state[action[0]+i,action[1]-i]==self.state[action]:
                count=count+1
                i=i+1
            else:
                break
        if count==4:
            return 1
        return 0