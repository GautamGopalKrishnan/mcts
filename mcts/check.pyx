# distutils: language = c++

from _checkers cimport CheckersEnv

import numpy as np


cdef class CCheckersEnv:
    cdef CheckersEnv c_env
    cdef public int players

    def __cinit__(self):
        self.c_env = CheckersEnv()
        self.players = 2

    def reset(self):
        self.c_env.reset()
        return np.array(self.c_env.board).reshape(8, 8)

    def step(self, action):
        ((i1, j1),(i2,j2)) = action
        reward = self.c_env.step(i1,j1,i2,j2)
        state = np.array(self.c_env.board).reshape(8, 8)
        return state, np.array(reward), self.c_env.done, {}

    def copy(self):
        copy = CCheckersEnv()
        copy.c_env = CheckersEnv(self.c_env)
        return copy
    
    @property
    def board(self):
        return np.array(self.c_env.board).reshape(8, 8)

    @property
    def done(self):
        return self.c_env.done

    @property
    def turn(self):
        return self.c_env.turn

    @property
    def actions(self):
        return self.c_env.actions
        
    
    
        

