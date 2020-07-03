#include "connectfour.h"

ConnectFourEnv::ConnectFourEnv() {
  turn = 0;
  count = 0;
  for (int i = 0; i < 42; i++)
    board[i] = 0;
  done = false;
}

void ConnectFourEnv::reset() {
  turn = 0;
  count = 0;
  for (int i = 0; i < 42; i++)
    board[i] = 0;
  done = false;
}

std::pair<float, float> ConnectFourEnv::step(int col) {
  int token = (turn == 0 ? 1 : -1);
  int row=0;
  for(int r=5;r>=0;r--)
  {
      if(board[7*r + col]==0)
      {
          row=r;
          r=-1;
      }
  }
  board[7 * row + col] = token;

  for(int c=0;c<4;c++)
  {
      if(board[7*row+c]==token && board[7*row+c+1]==token && board[7*row+c+2]==token && board[7*row+c+3]==token)
      {
          done = true;
          if (turn == 0)
              return std::make_pair(1, -1);
          else
              return std::make_pair(-1, 1);
      }
  }
  for(int r=0;r<3;r++)
  {
      if(board[7*r+col]==token && board[7*(r+1)+col]==token && board[7*(r+2)+col]==token && board[7*(r+3)+col]==token)
      {
          done = true;
          if (turn == 0)
              return std::make_pair(1, -1);
          else
              return std::make_pair(-1, 1);
      }
  }
  int m=0;
  if(row<col)
  {
      m=row;
  }
  else
  {
      m=col;
  }
  row=row-m;
  col=col-m;
  for(int i=0;i<3;i++)
  {
      if(row+i+3<6 && col+i+3<7)
      {
          if(board[7*(row+i)+col+i]==token && board[7*(row+i+1)+col+i+1]==token && board[7*(row+i+2)+col+i+2]==token && board[7*(row+i+3)+col+i+3]==token)
          {
              done = true;
              if (turn == 0)
                  return std::make_pair(1, -1);
              else
                  return std::make_pair(-1, 1);
          }
      }
  }
  row=row+m;
  col=col+m;
  for(int r=5;r>=3;r--)
  {
      if(row+col-r>=0 && row+col-r<=3)
      {
          if(board[7*r+row+col-r]==token && board[7*(r-1)+row+col-r+1]==token && board[7*(r-2)+row+col-r+2]==token && board[7*(r-3)+row+col-r+3]==token)
          {
              done = true;
              if (turn == 0)
                  return std::make_pair(1, -1);
              else
                  return std::make_pair(-1, 1);
          }
      }
  }
  
  if (++count == 42)
    done = true;
  turn = (turn + 1) % 2;
  return std::make_pair(0, 0);
}
