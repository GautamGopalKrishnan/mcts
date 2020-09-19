"""Tests for the TicTacToe game."""

from mcts.connectfour import *

import numpy as np
import pytest


def test_ConnectFourEnv_0():
    env = PyConnectFourEnv()
    env.reset()
    assert np.array_equal(env.board, np.zeros((6, 7), dtype=np.int))
    env.step(0)
    assert np.array_equal(env.board, np.array([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0]], dtype=np.int))
    assert env.done == False
    assert env.actions == [0,1,2,3,4,5,6] 
    
def test_ConnectFourEnv_1():
    env = CConnectFourEnv()
    env.reset()
    assert np.array_equal(env.board, np.zeros((6, 7), dtype=np.int))
    env.step(6)
    assert np.array_equal(env.board, np.array([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1]], dtype=np.int))
    assert env.done == False
    assert env.actions == [0,1,2,3,4,5,6]
