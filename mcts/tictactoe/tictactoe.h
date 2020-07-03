#ifndef TICTACTOE_H
#define TICTACTOE_H

#include <utility>

class TicTacToeEnv {
public:
  TicTacToeEnv();
  void reset();
  std::pair<float, float> step(int row, int col);
  int turn;
  bool done;
  int board[9];
private:
  int count;
};

#endif
