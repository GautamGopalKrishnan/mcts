from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(["mcts/tic.pyx",
                             "mcts/connect.pyx",
                             "mcts/check.pyx"]))

