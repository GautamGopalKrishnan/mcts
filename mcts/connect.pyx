# distutils: language = c++

from _connectfour cimport ConnectFourEnv

import numpy as np


cdef class CConnectFourEnv:
    cdef ConnectFourEnv c_env
    cdef public int players

    def __cinit__(self):
        self.c_env = ConnectFourEnv()
        self.players = 2

    def reset(self):
        self.c_env.reset()
        return np.array(self.c_env.board).reshape(6, 7)

    def step(self, action):
        col = action
        reward = self.c_env.step(col)
        state = np.array(self.c_env.board).reshape(6, 7)
        return state, np.array(reward), self.c_env.done, {}

    def copy(self):
        copy = CConnectFourEnv()
        copy.c_env = ConnectFourEnv(self.c_env)
        return copy
    
    @property
    def board(self):
        return np.array(self.c_env.board).reshape(6, 7)

    @property
    def done(self):
        return self.c_env.done

    @property
    def turn(self):
        return self.c_env.turn

    @property
    def actions(self):
        return [i for i in range(7) if self.c_env.board[i] == 0]

