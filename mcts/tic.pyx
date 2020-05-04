# distutils: language = c++

from _tictactoe cimport TicTacToeEnv

import numpy as np


cdef class CTicTacToeEnv:
    cdef TicTacToeEnv c_env
    cdef public int players

    def __cinit__(self):
        self.c_env = TicTacToeEnv()
        self.players = 2

    def reset(self):
        self.c_env.reset()
        return np.array(self.c_env.board).reshape(3, 3)

    def step(self, action):
        row, col = action
        reward = self.c_env.step(row, col)
        state = np.array(self.c_env.board).reshape(3, 3)
        return state, np.array(reward), self.c_env.done, {}

    def copy(self):
        copy = CTicTacToeEnv()
        copy.c_env = TicTacToeEnv(self.c_env)
        return copy
    
    @property
    def board(self):
        return np.array(self.c_env.board).reshape(3, 3)

    @property
    def done(self):
        return self.c_env.done

    @property
    def turn(self):
        return self.c_env.turn

    @property
    def actions(self):
        return [(i, j) for i in range(3) for j in range(3)
                if self.c_env.board[3*i + j] == 0]

