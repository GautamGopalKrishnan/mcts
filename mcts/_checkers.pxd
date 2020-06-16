from libcpp.utility cimport pair
from libcpp.vector cimport vector


cdef extern from "_checkers.cpp":
    pass

cdef extern from "_checkers.h":
    cdef cppclass CheckersEnv:
        CheckersEnv() except +
        CheckersEnv(const CheckersEnv&)
        void reset()
        pair[float, float] step(int, int, int, int)
        vector[pair[pair[int, int], pair[int, int]]] actions
        bint done
        int turn
        int[64] board
