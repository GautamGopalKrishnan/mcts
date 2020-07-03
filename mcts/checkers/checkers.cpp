#include "checkers.h"

CheckersEnv::CheckersEnv() {
  turn = 0;
  actions.clear();
  actions.push_back(std::make_pair(std::make_pair(2, 1), std::make_pair(3, 0)));
  actions.push_back(std::make_pair(std::make_pair(2, 1), std::make_pair(3, 2)));
  actions.push_back(std::make_pair(std::make_pair(2, 3), std::make_pair(3, 2)));
  actions.push_back(std::make_pair(std::make_pair(2, 3), std::make_pair(3, 4)));
  actions.push_back(std::make_pair(std::make_pair(2, 5), std::make_pair(3, 4)));
  actions.push_back(std::make_pair(std::make_pair(2, 5), std::make_pair(3, 6)));
  actions.push_back(std::make_pair(std::make_pair(2, 7), std::make_pair(3, 6)));
  for (int i=0; i < 8; i++)
  {
      for (int j=0; j < 8; j++)
      {
          board[8*i+j]=0;
          if ((i+j)%2!=0)
          {
              if (i<3)
              {
                  board[8*i+j]=1;
              }
              if (i>4)
              {
                  board[8*i+j]=-1;
              }
          }
      }
  }
  done = false;
}

void CheckersEnv::reset() {
  turn = 0;
  actions.clear();
  actions.push_back(std::make_pair(std::make_pair(2, 1), std::make_pair(3, 0)));
  actions.push_back(std::make_pair(std::make_pair(2, 1), std::make_pair(3, 2)));
  actions.push_back(std::make_pair(std::make_pair(2, 3), std::make_pair(3, 2)));
  actions.push_back(std::make_pair(std::make_pair(2, 3), std::make_pair(3, 4)));
  actions.push_back(std::make_pair(std::make_pair(2, 5), std::make_pair(3, 4)));
  actions.push_back(std::make_pair(std::make_pair(2, 5), std::make_pair(3, 6)));
  actions.push_back(std::make_pair(std::make_pair(2, 7), std::make_pair(3, 6)));
  for (int i=0; i < 8; i++)
  {
      for (int j=0; j < 8; j++)
      {
          board[8*i+j]=0;
          if ((i+j)%2!=0)
          {
              if (i<3)
              {
                  board[8*i+j]=1;
              }
              if (i>4)
              {
                  board[8*i+j]=-1;
              }
          }
      }
  }
  done = false;
}

std::pair<float, float> CheckersEnv::step(int i1, int j1, int i2, int j2) {
    if ((i1 - i2 == 2)||(i2 - i1 == 2))
    {
        board[8*((i1+i2)/2)+((j1+j2)/2)]=0;
    }
    board[8*i2+j2]=board[8*i1+j1];
    if ((i2 == 0)||(i2 == 7))
    {
        if ((board[8*i1+j1] == 1)||(board[8*i1+j1] == -1))
        {
            board[8*i2+j2]=2*board[8*i1+j1];
        }
    }
    board[8*i1+j1] = 0;
    turn = (turn + 1) % 2;
    actions.clear();
    int token = (turn == 0 ? 1 : -1);
    for(int i=0; i < 8; i++)
    {
        for(int j=0; j < 8; j++)
        {
            if ((board[8*i+j] == token)||(board[8*i+j]==2*token))
            {
                if ((i>0)&&(j>0)&&(board[8*i+j]!=1))
                {
                    if(board[8*(i-1)+(j-1)]==0)
                    {
                        actions.push_back(std::make_pair(std::make_pair(i, j), std::make_pair(i-1, j-1)));
                    }
                }
                if ((i>0)&&(j<7)&&(board[8*i+j]!=1))
                {
                    if(board[8*(i-1)+(j+1)]==0)
                    {
                        actions.push_back(std::make_pair(std::make_pair(i, j), std::make_pair(i-1, j+1)));
                    }
                }
                if ((i<7)&&(j>0)&&(board[8*i+j]!=-1))
                {
                    if(board[8*(i+1)+(j-1)]==0)
                    {
                        actions.push_back(std::make_pair(std::make_pair(i, j), std::make_pair(i+1, j-1)));
                    }
                }
                if ((i<7)&&(j<7)&&(board[8*i+j]!=-1))
                {
                    if(board[8*(i+1)+(j+1)]==0)
                    {
                        actions.push_back(std::make_pair(std::make_pair(i, j), std::make_pair(i+1, j+1)));
                    }
                }
                if ((i>1)&&(j>1)&&(board[8*i+j]!=1))
                {
                    if ((board[8*(i-2)+(j-2)]==0)&&(board[8*(i-1)+(j-1)]*board[8*i+j]<0))
                    {
                        actions.push_back(std::make_pair(std::make_pair(i, j), std::make_pair(i-2, j-2)));
                    }
                }
                if ((i>1)&&(j<6)&&(board[8*i+j]!=1))
                {
                    if ((board[8*(i-2)+(j+2)]==0)&&(board[8*(i-1)+(j+1)]*board[8*i+j]<0))
                    {
                        actions.push_back(std::make_pair(std::make_pair(i, j), std::make_pair(i-2, j+2)));
                    }
                }
                if ((i<6)&&(j>1)&&(board[8*i+j]!=-1))
                {
                    if ((board[8*(i+2)+(j-2)]==0)&&(board[8*(i+1)+(j-1)]*board[8*i+j]<0))
                    {
                        actions.push_back(std::make_pair(std::make_pair(i, j), std::make_pair(i+2, j-2)));
                    }
                }
                if ((i<6)&&(j<6)&&(board[8*i+j]!=-1))
                {
                    if ((board[8*(i+2)+(j+2)]==0)&&(board[8*(i+1)+(j+1)]*board[8*i+j]<0))
                    {
                        actions.push_back(std::make_pair(std::make_pair(i, j), std::make_pair(i+2, j+2)));
                    }
                }
            }
        }
    }
    if (actions.size()==0)
    {
        done=true;
        if (turn == 0)
        {
            return std::make_pair(-1, 1);
        }
        else
        {
            return std::make_pair(1, -1);
        }
    }
    return std::make_pair(0, 0);
}
