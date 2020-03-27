"""A Checkers game"""

from .agents import MCTSAgent
from .graphics import GraphWin, Text, Point, Rectangle, Circle

import numpy as np


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
                    if i>4:
                        self.state[i,j]=-1
                    if i==2 and j<7:
                        self.actions.append(((i,j),(i+1,j-1)))
                        self.actions.append(((i,j),(i+1,j+1)))
                    if i==5 and j!=0:
                        self.actions.append(((i,j),(i-1,j+1)))
                        self.actions.append(((i,j),(i-1,j-1)))
        self.actions.append(((2,7),(3,6)))
        self.actions.append(((5,0),(4,1)))

    def step(self, action):
        """Perform action and return new state, rewards, done, and turn."""
        if np.abs(action[0][0]-action[1][0])==2:
            self.state[(action[0][0]+action[1][0])//2,(action[0][1]+action[1][1])//2]=0
        self.state[action[1]] = self.state[action[0]] 
        if action[1][0]==0 or action[1][0]==7:
            self.state[action[1]] = 2*np.sign(self.state[action[0]])
        self.state[action[0]] = 0
        x=action[0][0]
        y=action[0][1]
        a=action[1][0]
        b=action[1][1]
        l=len(self.actions)
        r=0
        while r<l:
            if self.actions[r][1]==action[1] or self.actions[r][0]==action[0]:
                self.actions.pop(r)
                l=l-1
                r=r-1
            elif np.abs(self.actions[r][0][0]-self.actions[r][1][0])==2 and np.abs(self.actions[r][0][1]-self.actions[r][1][1])==2 and self.actions[r][0][0]+self.actions[r][1][0]==2*x and self.actions[r][0][1]+self.actions[r][1][1]==2*y:
                self.actions.pop(r)
                l=l-1
                r=r-1
            r=r+1
        if x>0 and y>0 and self.state[x-1,y-1]!=-1 and self.state[x-1,y-1]!=0:
            self.actions.append(((x-1,y-1),(x,y)))
        if x>0 and y<7 and self.state[x-1,y+1]!=-1 and self.state[x-1,y+1]!=0:
            self.actions.append(((x-1,y+1),(x,y)))    
        if x<7 and y>0 and self.state[x+1,y-1]!=1 and self.state[x+1,y-1]!=0:
            self.actions.append(((x+1,y-1),(x,y)))     
        if x<7 and y<7 and self.state[x+1,y+1]!=1 and self.state[x+1,y+1]!=0:
            self.actions.append(((x+1,y+1),(x,y)))   
        if x>1 and y>1 and self.state[x-2,y-2]!=-1 and self.state[x-2,y-2]!=0 and np.sign(self.state[x-1,y-1])==(-1)*np.sign(self.state[x-2,y-2]):
            self.actions.append(((x-2,y-2),(x,y)))
        if x>1 and y<6 and self.state[x-2,y+2]!=-1 and self.state[x-2,y+2]!=0 and np.sign(self.state[x-1,y+1])==(-1)*np.sign(self.state[x-2,y+2]):
            self.actions.append(((x-2,y+2),(x,y)))
        if x<6 and y>1 and self.state[x+2,y-2]!=1 and self.state[x+2,y-2]!=0 and np.sign(self.state[x+1,y-1])==(-1)*np.sign(self.state[x+2,y-2]):
            self.actions.append(((x+2,y-2),(x,y)))
        if x<6 and y<6 and self.state[x+2,y+2]!=1 and self.state[x+2,y+2]!=0 and np.sign(self.state[x+1,y+1])==(-1)*np.sign(self.state[x+2,y+2]):
            self.actions.append(((x+2,y+2),(x,y)))
        if a>0 and a<7 and b>0 and b<7:
            if np.sign(self.state[a-1,b-1])==(-1)*np.sign(self.state[a,b]) and self.state[a+1,b+1]==0 and self.state[a-1,b-1]!=-1:
                self.actions.append(((a-1,b-1),(a+1,b+1)))
            if np.sign(self.state[a-1,b+1])==(-1)*np.sign(self.state[a,b]) and self.state[a+1,b-1]==0 and self.state[a-1,b+1]!=-1:
                self.actions.append(((a-1,b+1),(a+1,b-1)))
            if np.sign(self.state[a+1,b-1])==(-1)*np.sign(self.state[a,b]) and self.state[a-1,b+1]==0 and self.state[a+1,b-1]!=1:
                self.actions.append(((a+1,b-1),(a-1,b+1)))
            if np.sign(self.state[a+1,b+1])==(-1)*np.sign(self.state[a,b]) and self.state[a-1,b-1]==0 and self.state[a+1,b+1]!=1:
                self.actions.append(((a+1,b+1),(a-1,b-1)))
        winner = self.winner(action)
        if winner is not None:
            rewards = np.array([winner,(-1)*winner])
        else:
            rewards = np.array([0,0])
        self.done = winner is not None
        self.turn = (self.turn + 1)%2
        if self.done:
            self.actions=[]
        return self.state.copy(), rewards, self.done, self.turn

    def copy(self):
        copy = CheckersEnv()
        copy.state = self.state.copy()
        copy.turn = self.turn
        copy.done = self.done
        copy.actions = self.actions.copy()
        return copy

    def render(self):
        print(self.state)

    def winner(self,action):
        n = (-1)*np.sign(self.state[action[1]])
        for r in range(len(self.actions)):
            if np.sign(self.state[self.actions[r][0]])==n:
                return None
        return (-1)*n


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
                    action=[]
                    a=self.interface.get_action1(self.env.actions).replace('(', '').replace(')', '').split(',')
                    if a[0].lower() == 'q':
                        return
                    elif a[0].lower() == 'r':
                        self.env.reset()
                        total_rewards = np.zeros(self.env.players)
                        continue
                    else:
                        action.append((int(a[0]),int(a[1])))
                        b=self.interface.get_action2(self.env.actions,action[0]).replace('(', '').replace(')', '').split(',')
                        action.append((int(b[0]),int(b[1])))
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


class Button:
    """A button is a labeled rectangle in a window.
    It is activated or deactivate with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it.
    
    From "Python Programming: An Introduction to Computer Science"
    by John Zelle."""
    
    def __init__(self, win, center, width, height, label):
        w, h = width/2.0, height/2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.label = Text(center, label)
        self.deactivate()

    def draw(self, win):
        self.rect.draw(win)
        self.label.draw(win)

    def undraw(self):
        self.rect.undraw()
        self.label.undraw()

    def clicked(self, p):
        """Returns true if button active and p is inside."""
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)
    
    def getLabel(self):
        """Returns the label string of this button."""
        return self.label.getText()
    
    def activate(self):
        """Sets this button to 'active'."""
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True
        
    def deactivate(self):
        """Sets this button to 'inactive'."""
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False


class BoardView:
    """Widget for a Checkers board."""
    
    def __init__(self, win, center):#Needs fixing
        self.win = win
        self.background_color = "white"
        self.frame_colors = ['white','brown']
        self.piece_colors = ['black', 'red']
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
                elif board[row, col] == 0:
                    self.circles[row][col].undraw()
                    self.pieces[row][col].setFill(self.frame_colors[(row+col)%2])
                elif board[row, col] == 1:
                    self.circles[row][col].undraw()
                    self.circles[row][col].draw(self.win)
                    self.circles[row][col].setFill(self.piece_colors[1])


class GraphicInterface:
    
    def __init__(self):
        self.win = GraphWin("Checkers", 400, 575)
        self.win.setBackground("white")
        self.banner = Text(Point(200, 50), "")
        self.banner.setSize(25)
        self.banner.setFill("black")
        self.banner.setStyle("bold")
        self.banner.draw(self.win)
        self.start_buttons = [
            Button(self.win, Point(200, 275), 150, 50, "Player 1"),
            Button(self.win, Point(200, 350), 150, 50, "Player 2"),
            Button(self.win, Point(200, 425), 150, 50, "Quit"),
        ]
        self.action_buttons = [Button(self.win, Point(50+j*45,100+i*45), 45, 45, "({},{})".format(i,j)) for i in range(8) for j in range(8)]
        self.action_buttons.append(Button(self.win, Point(100, 525), 150, 50, "Restart"))
        self.action_buttons.append(Button(self.win, Point(300, 525), 150, 50, "Quit"))
        self.board = BoardView(self.win, Point(200, 250))

    def show_start(self):
        for b in self.action_buttons:
            b.undraw()
        self.board.undraw()
        self.banner.setText("Checkers")
        for b in self.start_buttons:
            b.draw(self.win)
    
    def want_to_play(self):
        for b in self.start_buttons:
            b.activate()
        while True:
            p = self.win.getMouse()
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
            b.draw(self.win)
        self.board.draw(self.win)

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
            p = self.win.getMouse()
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
            p = self.win.getMouse()
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
            p = self.win.getMouse()
            for b in self.action_buttons:
                if b.clicked(p):
                    return b.getLabel()

    def close(self):
        self.win.close()
