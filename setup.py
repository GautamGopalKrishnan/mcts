from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("mcts/tic.pyx"))
setup(ext_modules=cythonize("mcts/connect.pyx"))