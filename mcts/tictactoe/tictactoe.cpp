#include "tictactoe.h"

TicTacToeEnv::TicTacToeEnv() {
  turn = 0;
  count = 0;
  for (int i = 0; i < 9; i++)
    board[i] = 0;
  done = false;
}

void TicTacToeEnv::reset() {
  turn = 0;
  count = 0;
  for (int i = 0; i < 9; i++)
    board[i] = 0;
  done = false;
}

std::pair<float, float> TicTacToeEnv::step(int row, int col) {
  int token = (turn == 0 ? 1 : -1);
  board[3 * row + col] = token;

  if ((board[3 * row] == token && board[3 * row + 1] == token && board[3 * row + 2] == token) ||
      (board[col] == token && board[col + 3] == token && board[col + 6] == token) ||
      (row == col && board[0] == token && board[4] == token && board[8] == token) ||
      (row + col == 2 && board[2] == token && board[4] == token && board[6] == token)) {
    done = true;
    if (turn == 0)
      return std::make_pair(1, -1);
    else
      return std::make_pair(-1, 1);
  }

  if (++count == 9)
    done = true;
  turn = (turn + 1) % 2;
  return std::make_pair(0, 0);
}
