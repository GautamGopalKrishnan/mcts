"""Basic Tic-Tac-Toe game."""

import numpy as np


class TicTacToeEnv:
    """An environment for two-player tic-tac-toe."""

    def __init__(self):
        self.players = 2
        self.reset()

    def reset(self):
        """Initialize a new game."""
        self.board = np.zeros((3, 3), dtype=np.int)
        self.turn = 0
        self.done = False
        self.actions = [(a, b) for a in range(3) for b in range(3)]

    def step(self, action):
        """Perform action and return new state, rewards, done, and turn."""
        assert self.board[action] == 0
        self.board[action] = (-1) ** self.turn
        self.turn = (self.turn + 1) % 2
        winner = self.winner(action)
        if winner is not None:
            rewards = np.array([winner,(-1)*winner])
        else:
            rewards = np.array([0, 0])
        self.done = winner is not None or np.all(self.board != 0)
        if self.done:
            self.actions = []
        else:
            self.actions = [(a, b) for a in range(3) for b in range(3) if self.board[a, b] == 0]
        return self.board.copy(), rewards, self.done, self.turn

    def copy(self):
        copy = TicTacToeEnv()
        copy.board = self.board.copy()
        copy.turn = self.turn
        copy.done = self.done
        copy.actions = self.actions.copy()
        return copy

    def render(self):
        print(self.board)

    def winner(self,action):
        (r,c)=(self.rsum(action[0]),self.csum(action[1]))
        if r==3 or r==-3:
            return np.sign(r)
        if c==3 or c==-3:
            return np.sign(c)
        if (action[0]==action[1]):
            d=self.dsum()
            if d==3 or d==-3:
                return np.sign(d)
        if (sum(action)==2):
            a=self.adsum()
            if a==3 or a==-3:
                return np.sign(a)
        return None
    
    def rsum(self,r=0):
        return np.sum(self.board[r, :])
    
    def csum(self,c=0):
        return np.sum(self.board[:, c])
    
    def dsum(self):
        return np.sum(self.board[np.arange(3), np.arange(3)])
        
    def adsum(self):
        return np.sum(self.board[np.arange(3), np.arange(2, -1, -1)])

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)
