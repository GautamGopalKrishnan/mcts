"""Tests for the TicTacToe game."""

from mcts.checkers import *

import numpy as np
import pytest


def test_CheckersEnv_0():
    env = PyCheckersEnv()
    env.reset()
    assert env.turn == 0
    env.step(((2, 1),(3,2)))
    assert env.done == False
    assert env.turn == 1

def test_CheckersEnv_1():
    env = CCheckersEnv()
    env.reset()
    env.step(((2, 7),(3,6)))
    assert env.done == False
    assert env.turn == 1