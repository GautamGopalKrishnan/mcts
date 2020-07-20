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
