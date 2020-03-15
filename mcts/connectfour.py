"""A Connect Four game"""

from .agents import MCTSAgent

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


class ConnectFourApp:
    """Application for running a game of Connect Four."""

    def __init__(self, interface):
        self.env = ConnectFourEnv()
        self.interface = interface

    def run(self):
        """Start the application."""
        while True:
            entry = self.interface.start()
            if entry == 'quit':
                self.interface.close()
                break
            else:
                player = int(entry) - 1
                agent = MCTSAgent()
                self.play_games(player, agent)

    def play_games(self, player, agent):
        """Play games between player and agent."""
        while True:
            self.env.reset()
            total_rewards = np.zeros(self.env.players)
            while not self.env.done:
                self.interface.show_board(self.env.state)
                if self.env.turn == player:
                    action = self.interface.get_action()
                    if action == 'quit':
                        return
                    elif action == 'restart':
                        self.env.reset()
                        total_rewards = np.zeros(self.env.players)
                        continue
                    else:
                        action = int(action) - 1
                else:
                    action = agent.act(self.env)
                _, rewards, _, _ = self.env.step(action)
                total_rewards += rewards
            winner = np.argmax(total_rewards)
            self.interface.show_board(self.env.state)
            self.interface.show_winner(winner)


class TextInterface:
    """Text interface for playing Connect Four."""

    def start(self):
        print("Welcome to Connect Four.")
        return input("Choose player (1 or 2) or quit: ")

    def get_action(self):
        return input("Choose a column or restart or quit: ")

    def show_board(self, board):
        board = np.where(board == 0, "_", np.where(board == 1, "X", "O"))
        print()
        for row in board:
            print("|" + "|".join(row) + "|")
        print()
        print(" " + " ".join(str(x) for x in range(1, 8)) + " ")

    def show_winner(self, winner):
        print("Player {0} wins".format(winner + 1))

    def close(self):
        print("\nThanks for playing!")
