"""Run games between agents and save results."""

import argparse

import numpy as np

from mcts.agents import MCTSAgent, epsilon_greedy, ucb
from mcts.connectfour import CConnectFourEnv
from mcts.tictactoe import CTicTacToeEnv


def make_parser():
    """Return the command line argument parser for this script."""
    parser = argparse.ArgumentParser(description="Run games and save results")
    parser.add_argument('--env',
                        choices=['ConnectFour', 'TicTacToe'],
                        default='ConnectFour',
                        help='the game')
    parser.add_argument('--tree_policy1',
                        choices=['epsilon_greedy', 'ucb'],
                        default='epsilon_greedy',
                        help='the type of tree policy for agent 1')
    parser.add_argument('--epsilon1',
                        type=float,
                        default=0.05,
                        help='the value of epsilon for agent 1 if using epsilon greedy')
    parser.add_argument('--c1',
                        type=float,
                        default=np.sqrt(2),
                        help='the value of c for agent 1 if using ucb')
    parser.add_argument('--timeout1',
                        type=float,
                        default=1.0,
                        help='timeout in seconds for agent 1')
    parser.add_argument('--tree_policy2',
                        choices=['epsilon_greedy', 'ucb'],
                        default='epsilon_greedy',
                        help='the type of tree policy for agent 2')
    parser.add_argument('--epsilon2',
                        type=float,
                        default=0.05,
                        help='the value of epsilon for agent 2 if using epsilon greedy')
    parser.add_argument('--c2',
                        type=float,
                        default=np.sqrt(2),
                        help='the value of c for agent 2 if using ucb')
    parser.add_argument('--timeout2',
                        type=float,
                        default=1.0,
                        help='timeout in seconds for agent 2')
    parser.add_argument('--samples',
                        type=int,
                        default=10,
                        help='the number of games to play')
    return parser


def make_agents(args):
    """Return the list of agents for this run."""
    if args.tree_policy1 == 'epsilon_greedy':
        tree_policy1 = epsilon_greedy(epsilon=args.epsilon1)
    elif args.tree_policy1 == 'ucb':
        tree_policy1 = ucb(c=args.c1)
    else:
        raise ValueError('invalid policy type for agent 1')
    agent1 = MCTSAgent(tree_policy=tree_policy1, timeout=args.timeout1)
    if args.tree_policy2 == 'epsilon_greedy':
        tree_policy2 = epsilon_greedy(epsilon=args.epsilon2)
    elif args.tree_policy2 == 'ucb':
        tree_policy2 = ucb(c=args.c2)
    else:
        raise ValueError('invalid policy type for agent 2')
    agent2 = MCTSAgent(tree_policy=tree_policy2, timeout=args.timeout2)
    return [agent1, agent2]


def make_env(args):
    """Return the environment for this run."""
    if args.env == 'ConnectFour':
        env = CConnectFourEnv()
    elif args.env == 'TicTacToe':
        env = CTicTacToeEnv()
    else:
        raise ValueError('invalid environment type')
    return env


def run_episode(agents, env):
    """Return total reward and steps for one game between agents on env."""
    env.reset()
    done = False
    total_reward = np.zeros(env.players)
    steps = 0
    while not done:
        action = agents[env.turn].act(env)
        _, reward, done, _ = env.step(action)
        total_reward += reward
        steps += 1
    return total_reward, steps


def save_results(results):
    """Save a list of results from run_episode to file."""
    with open('results.csv', 'a') as f:
        f.write('Agent1,Agent2,Steps\n')
        for total_reward, steps in results:
            f.write(f"{total_reward[0]},{total_reward[1]},{steps}\n")


if __name__ == "__main__":
    args = make_parser().parse_args()
    agents = make_agents(args)
    env = make_env(args)
    results = [run_episode(agents, env) for _ in range(args.samples)]
    save_results(results)
