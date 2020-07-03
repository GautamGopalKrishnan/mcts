from libcpp.utility cimport pair

cdef extern from "tictactoe.cpp":
    pass

cdef extern from "tictactoe.h":
    cdef cppclass TicTacToeEnv:
        TicTacToeEnv() except +
        TicTacToeEnv(const TicTacToeEnv&)
        void reset()
        pair[float, float] step(int, int)
        bint done
        int turn
        int[9] board
