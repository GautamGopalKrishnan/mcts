import timeit

setup = """

from mcts.checkers import PyCheckersEnv, CCheckersEnv
from mcts.connectfour import PyConnectFourEnv, CConnectFourEnv
from mcts.tictactoe import PyTicTacToeEnv, CTicTacToeEnv


import numpy as np
import random


def simulate(env):
    env.reset()
    total_rewards = np.zeros(2)
    while not env.done:
        action = random.choice(env.actions)
        state, rewards, _, _ = env.step(action)
        total_rewards += rewards
    return total_rewards


env1 = PyCheckersEnv()
env2 = CCheckersEnv()

"""

print('Python:', timeit.timeit('simulate(env1)', setup=setup, number=1000))
print('Cython:', timeit.timeit('simulate(env2)', setup=setup, number=1000))
