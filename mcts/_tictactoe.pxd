from libcpp.utility cimport pair

cdef extern from "_tictactoe.cpp":
    pass

cdef extern from "_tictactoe.h":
    cdef cppclass TicTacToeEnv:
        TicTacToeEnv() except +
        TicTacToeEnv(const TicTacToeEnv&)
        void reset()
        pair[float, float] step(int, int)
        bint done
        int turn
        int[9] board
