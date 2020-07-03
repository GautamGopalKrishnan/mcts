from libcpp.utility cimport pair

cdef extern from "connectfour.cpp":
    pass

cdef extern from "connectfour.h":
    cdef cppclass ConnectFourEnv:
        ConnectFourEnv() except +
        ConnectFourEnv(const ConnectFourEnv&)
        void reset()
        pair[float, float] step(int)
        bint done
        int turn
        int[42] board
