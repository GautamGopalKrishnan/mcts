"""A Checkers game"""

import numpy as np

from .agents import MCTSAgent
from .graphics import GraphWin, Text, Point, Rectangle, Circle
from .gui import Button


class CheckersEnv:
    """An environment for two-player checkers."""

    def __init__(self):
        self.players = 2
        self.reset()

    def reset(self):
        """Initialize a new game and return state and turn."""
        self.state = np.zeros((8, 8), dtype=np.int)
        self.done = False
        self.actions = []
        self.turn = 0
        for i in range(8):
            for j in range(8):
                if (i+j)%2!=0:
                    if i<3:
                        self.state[i,j]=1
                    if i==2:
                        moves=(self.bdiag(i,j),self.badiag(i,j),self.fdiag(i,j),self.fadiag(i,j))
                        for r in range(4):
                            if moves[r] is not None:
                                self.actions.append(moves[r])
                    if i>4:
                        self.state[i,j]=-1

    def step(self, action):
        """Perform action and return new state, rewards, done, and turn."""
        if np.abs(action[0][0]-action[1][0])==2:
            self.state[(action[0][0]+action[1][0])//2,(action[0][1]+action[1][1])//2]=0
        self.state[action[1]] = self.state[action[0]] 
        if action[1][0]==0 or action[1][0]==7:
            self.state[action[1]] = 2*np.sign(self.state[action[0]])
        self.state[action[0]] = 0
        self.turn = (self.turn + 1)%2
        self.actions=[]
        for i in range(8):
            for j in range(8):
                if np.sign(self.state[i,j])==(-1)**self.turn:
                    moves=(self.bdiag(i,j),self.badiag(i,j),self.fdiag(i,j),self.fadiag(i,j))
                    for r in range(4):
                        if moves[r] is not None:
                            self.actions.append(moves[r])
        winner = self.winner(action)
        if winner is not None:
            rewards = np.array([winner,(-1)*winner])
        else:
            rewards = np.array([0,0])
        self.done = winner is not None
        return self.state.copy(), rewards, self.done, self.turn
    
    def winner(self,action):
        if len(self.actions)==0:
            return (-1)**(self.turn+1)
        return None 
    
    def bdiag(self, row, col):
        if self.state[row,col]==1:
            return None
        else:
            if row>0 and col>0 and self.state[row-1,col-1]==0:
                return ((row,col),(row-1,col-1))
            if row>1 and col>1 and self.state[row-2,col-2]==0 and np.sign(self.state[row-1,col-1])==(-1)*np.sign(self.state[row,col]):
                return ((row,col),(row-2,col-2))
        return None
    
    def badiag(self, row, col):
        if self.state[row,col]==1:
            return None
        else:
            if row>0 and col<7 and self.state[row-1,col+1]==0:
                return ((row,col),(row-1,col+1))
            if row>1 and col<6 and self.state[row-2,col+2]==0 and np.sign(self.state[row-1,col+1])==(-1)*np.sign(self.state[row,col]):
                return ((row,col),(row-2,col+2))
        return None
    
    def fdiag(self, row, col):
        if self.state[row,col]==-1:
            return None
        else:
            if row<7 and col<7 and self.state[row+1,col+1]==0:
                return ((row,col),(row+1,col+1))
            if row<6 and col<6 and self.state[row+2,col+2]==0 and np.sign(self.state[row+1,col+1])==(-1)*np.sign(self.state[row,col]):
                return ((row,col),(row+2,col+2))
        return None
    
    def fadiag(self, row, col):
        if self.state[row,col]==-1:
            return None
        else:
            if row<7 and col>0 and self.state[row+1,col-1]==0:
                return ((row,col),(row+1,col-1))
            if row<6 and col>1 and self.state[row+2,col-2]==0 and np.sign(self.state[row+1,col-1])==(-1)*np.sign(self.state[row,col]):
                return ((row,col),(row+2,col-2))
        return None

    def copy(self):
        copy = CheckersEnv()
        copy.state = self.state.copy()
        copy.turn = self.turn
        copy.done = self.done
        copy.actions = self.actions.copy()
        return copy

    def render(self):
        print(self.state)

class CheckersApp:
    """Application for running a game of Checkers."""

    def __init__(self, interface):
        self.env = CheckersEnv()
        self.interface = interface

    def run(self):
        """Start the application."""
        while True:
            self.interface.show_start()
            choice = self.interface.want_to_play()
            if choice[0].lower() == 'q':
                self.interface.close()
                break
            else:
                player = int(choice) - 1
                agent = MCTSAgent()
                self.play_games(player, agent)

    def play_games(self, player, agent):
        """Play games between player and agent."""
        self.interface.show_board()
        while True:
            self.env.reset()
            total_rewards = np.zeros(self.env.players)
            while not self.env.done:
                self.interface.update_board(self.env.state)
                if self.env.turn == player:
                    a=self.interface.get_action1(self.env.actions)
                    if a[0].lower() == 'q':
                        return
                    elif a[0].lower() == 'r':
                        self.env.reset()
                        total_rewards = np.zeros(self.env.players)
                        continue
                    else:
                        a=a.replace('(', '').replace(')', '').split(',')
                        a=(int(a[0]),int(a[1]))
                        b=self.interface.get_action2(self.env.actions,a).replace('(', '').replace(')', '').split(',')
                        b=(int(b[0]),int(b[1]))
                        action=(a,b)
                else:
                    action = agent.act(self.env)
                _, rewards, _, _ = self.env.step(action)
                total_rewards += rewards
            self.interface.update_board(self.env.state)
            if total_rewards[0]==0:
                self.interface.show_winner(0)
            else:
                self.interface.show_winner(np.argmax(total_rewards)+1)
            choice = self.interface.want_to_replay()
            if choice[0].lower() == 'q':
                return

class CheckersBoard:
    """Widget for a Checkers board."""
    
    def __init__(self, win, center):
        self.win = win
        self.background_color = "white"
        self.frame_colors = ['white','brown']
        self.piece_colors = ['black', 'red', 'gray', 'orange']
        self.pieces = [[self._make_piece(Point(50+col*45,100+row*45), 45, (row+col)%2)
                        for col in range(8)]
                       for row in range(8)]
        self.circles=[[Circle(Point(50+col*45,100+row*45), 17)
                        for col in range(8)]
                       for row in range(8)]
   
        
    def _make_piece(self, center, size, var):
        """Set up the grid of pieces."""
        piece = Rectangle(Point(center.getX()-size/2,center.getY()-size/2),Point(center.getX()+size/2,center.getY()+size/2))
        piece.setFill(self.frame_colors[var])
        return piece
    
    def draw(self, win):
        for row in range(8):
            for col in range(8):
                self.pieces[row][col].draw(win)

    def undraw(self):
        for row in range(8):
            for col in range(8):
                self.pieces[row][col].undraw()
                self.circles[row][col].undraw()

    def update(self, board):
        """Draw board state on this widget."""
        for row in range(8):
            for col in range(8):
                if board[row, col] == -1:
                    self.circles[row][col].undraw()
                    self.circles[row][col].draw(self.win)
                    self.circles[row][col].setFill(self.piece_colors[0])
                elif board[row, col] == -2:
                    self.circles[row][col].undraw()
                    self.circles[row][col].draw(self.win)
                    self.circles[row][col].setFill(self.piece_colors[2])
                elif board[row, col] == 0:
                    self.circles[row][col].undraw()
                    self.pieces[row][col].setFill(self.frame_colors[(row+col)%2])
                elif board[row, col] == 1:
                    self.circles[row][col].undraw()
                    self.circles[row][col].draw(self.win)
                    self.circles[row][col].setFill(self.piece_colors[1])
                elif board[row, col] == 2:
                    self.circles[row][col].undraw()
                    self.circles[row][col].draw(self.win)
                    self.circles[row][col].setFill(self.piece_colors[3])


class CheckersGUI:
    
    def __init__(self, window):
        #self.window = GraphWin("Checkers", 400, 575)
        self.window=window
        self.window.setBackground("white")
        self.banner = Text(Point(200, 50), "")
        self.banner.setSize(25)
        self.banner.setFill("black")
        self.banner.setStyle("bold")
        self.banner.draw(self.window)
        self.start_buttons = [
            Button(self.window, Point(200, 275), 150, 50, "Player 1"),
            Button(self.window, Point(200, 350), 150, 50, "Player 2"),
            Button(self.window, Point(200, 425), 150, 50, "Quit"),
        ]
        self.action_buttons = [Button(self.window, Point(50+j*45,100+i*45), 45, 45, "({},{})".format(i,j)) for i in range(8) for j in range(8)]
        self.action_buttons.append(Button(self.window, Point(100, 525), 150, 50, "Restart"))
        self.action_buttons.append(Button(self.window, Point(300, 525), 150, 50, "Quit"))
        self.board = CheckersBoard(self.window, Point(200, 250))

    def show_start(self):
        for b in self.action_buttons:
            b.undraw()
        self.board.undraw()
        self.banner.setText("Checkers")
        for b in self.start_buttons:
            b.draw(self.window)
    
    def want_to_play(self):
        for b in self.start_buttons:
            b.activate()
        while True:
            p = self.window.getMouse()
            for b in self.start_buttons:
                if b.clicked(p):
                    label = b.getLabel()
                    if label != 'Quit':
                        label = label[-1]
                    return label

    def show_board(self):
        for b in self.start_buttons:
            b.undraw()
        self.banner.setText("")
        for b in self.action_buttons:
            b.draw(self.window)
        self.board.draw(self.window)

    def get_action1(self, actions):
        self.banner.setText("Your turn")
        for i in range(8):
            for j in range(8):
                self.action_buttons[8*i+j].deactivate()
        for r in actions:
            self.action_buttons[8*r[0][0]+r[0][1]].activate()                
        self.action_buttons[-1].activate()
        self.action_buttons[-2].activate()
        while True:
            p = self.window.getMouse()
            for b in self.action_buttons:
                if b.clicked(p):
                    self.banner.setText("")
                    return b.getLabel()
                
    def get_action2(self, actions, firstaction):
        self.banner.setText("Your turn")
        for i in range(8):
            for j in range(8):
                self.action_buttons[8*i+j].deactivate()
        for r in range(len(actions)):
            if actions[r][0][0]==firstaction[0] and actions[r][0][1]==firstaction[1]:
                self.action_buttons[8*actions[r][1][0]+actions[r][1][1]].activate()                
        #self.action_buttons[-1].activate()
        #self.action_buttons[-2].activate()
        while True:
            p = self.window.getMouse()
            for b in self.action_buttons:
                if b.clicked(p):
                    self.banner.setText("")
                    return b.getLabel()            
     
        
    def update_board(self, board):
        self.board.update(board)
        self.banner.setText("")

    def show_winner(self, winner):
        if winner==0:
                self.banner.setText("Its a tie!")
        else:
            self.banner.setText("Player {} wins!".format(winner))
        
    def want_to_replay(self):
        for b in self.action_buttons:
            b.activate()
        while True:
            p = self.window.getMouse()
            for b in self.action_buttons:
                if b.clicked(p):
                    return b.getLabel()

    def close(self):
        self.banner.undraw()
        for b in self.start_buttons:
            b.undraw()
        #self.window.close()
