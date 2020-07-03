#ifndef CHECKERS_H
#define CHECKERS_H

#include <utility>

class CheckersEnv {
public:
  CheckersEnv();
  void reset();
  std::pair<float, float> step(int i1, int j1, int i2, int j2);
  std::vector<std::pair<std::pair<int, int>, std::pair<int, int> > > actions;
  int turn;
  bool done;
  int board[64];
};

#endif
