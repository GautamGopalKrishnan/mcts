# MCTS
Monte Carlo tree search applied to several games, implementing techniques and principles of reinforcement learning.

This project has a Python implementation of Monte Carlo tree search applied to [Tic-Tac-Toe](https://en.wikipedia.org/wiki/Tic-tac-toe), [Connect Four](https://en.wikipedia.org/wiki/Connect_Four) and [Checkers](https://en.wikipedia.org/wiki/Draughts). The game environments were later converted to a Cython implementation to improve performance (by a factor of 10).

- Tree policy at selection step has an epsilon-greedy implementation (with epsilon = 0.09) and an upper confidence bound (UCB) implementation (with c = sqrt(2))
- Number of rollouts performed is limited by the timeout value which is set to a default of 1.0 second
- Values at each node of game tree stores average expected reward based on Monte Carlo simulation

Our code for the agent and various environments (written in Python 3) can be found under [mcts](mcts) directory. Some results of our hyperparameter tuning can be found under [data](data) and [notebooks](notebooks).

You can find below the instructions (with images) to install and play the games.

## Installation
Install by cloning the repository with

    git clone https://github.com/GautamGopalKrishnan/mcts.git

and building with

    python setup.py build_ext -i

## Playing a Game
Run the main application with

    python run.py

which will prompt you to select a game and choose a player.

![](images/mcts_games_menu.png)

## Tic-Tac-Toe
Select player from the menu and click on the box where you want to make your move.

![](images/tictactoe_menu.png)

![](images/tictactoe.png)

## Connect Four 
Select player from the menu and click on the column number where you want to make your move.

![](images/connectfour_menu.png)

![](images/connectfour.png)

## Checkers
Select player from the menu.

![](images/checkers_menu.png)

Click on the piece you want to move and then click the square where you want the piece to move to.

![](images/checkers.png)

## Running Tests
Basic checks of the package are performed with

    python -m pytest

## Building Documentation

Documentation is built with Sphinx. To rebuild, run

    sphinx-apidoc -f -o source/ ../mcts/
    make html

in the `docs/` directory. Then view the output with

    open build/html/index.html
