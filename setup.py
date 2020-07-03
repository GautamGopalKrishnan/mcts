from setuptools import setup
from Cython.Build import cythonize


setup(ext_modules=cythonize(["mcts/tictactoe/wrapped.pyx",
                             "mcts/checkers/wrapped.pyx",
                             "mcts/connectfour/wrapped.pyx"]))
