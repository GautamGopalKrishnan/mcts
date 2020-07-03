#ifndef CONNECTFOUR_H
#define CONNECTFOUR_H

#include <utility>

class ConnectFourEnv {
public:
  ConnectFourEnv();
  void reset();
  std::pair<float, float> step(int col);
  int turn;
  bool done;
  int board[42];
private:
  int count;
};

#endif
