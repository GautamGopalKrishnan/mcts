"""Tests for the TicTacToe game."""

from mcts.tictactoe import *

import numpy as np
import pytest


def test_TicTacToeEnv_0():
    env = PyTicTacToeEnv()
    env.reset()
    assert np.array_equal(env.board, np.zeros((3, 3), dtype=np.int))
    env.step((1, 1))
    assert np.array_equal(env.board, np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.int))
    
def test_TicTacToeEnv_1():
    env = PyTicTacToeEnv()
    env.reset()
    assert np.array_equal(env.board, np.zeros((3, 3), dtype=np.int))
    env.step((0, 0))
    assert np.array_equal(env.board, np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=np.int))
    env.step((1, 1))
    assert np.array_equal(env.board, np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=np.int))
    env.step((1, 0))
    assert np.array_equal(env.board, np.array([[1, 0, 0], [1, -1, 0], [0, 0, 0]], dtype=np.int))
    env.step((2, 2))
    assert np.array_equal(env.board, np.array([[1, 0, 0], [1, -1, 0], [0, 0, -1]], dtype=np.int))
    env.step((2, 0))
    assert np.array_equal(env.board, np.array([[1, 0, 0], [1, -1, 0], [1, 0, -1]], dtype=np.int))
    assert env.done==True
    
def test_TicTacToeEnv_2():
    env = CTicTacToeEnv()
    env.reset()
    assert np.array_equal(env.board, np.zeros((3, 3), dtype=np.int))
    env.step((1, 1))
    assert np.array_equal(env.board, np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.int))
    
    