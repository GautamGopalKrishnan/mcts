"""Basic Tic-Tac-Toe game."""

from .agents import MCTSAgent
from .graphics import GraphWin, Text, Point, Rectangle, Circle, Line


import numpy as np


class TicTacToeEnv:
    """An environment for one-player tic-tac-toe."""
    
    def __init__(self, state=np.zeros((3, 3), dtype=np.int)):
        self.state = state
        self.players=1

    def reset(self):
        self.state = np.zeros((3, 3), dtype=np.int)
        self.done=False
        self.turn=0

    def step(self, action):
        assert self.state[action] != 1
        self.state[action] = 1
        self.done=self.donef(action)
        return self.state.copy(), -1, self.done, {}

    def copy(self):
        copy = TicTacToeEnv()
        copy.state = self.state.copy()
        copy.done=self.done
        copy.turn=self.turn
        return copy
    
    def render(self):
        print(self.state)

    def donef(self,action=()):
        """True if three in a row somewhere."""
        if (action[0]==action[1] and self.dsum()==3) or (sum(action)==2 and self.adsum()==3):
            return True
        if self.rsum(action[0])==3 or self.csum(action[1])==3:
            return True
        return False
    
    def rsum(self,r=0):
        return np.sum(self.state[r, :])
    
    def csum(self,c=0):
        return np.sum(self.state[:, c])
    
    def dsum(self):
        return np.sum(self.state[np.arange(3), np.arange(3)])
        
    def adsum(self):
        return np.sum(self.state[np.arange(3), np.arange(2, -1, -1)])
    
    @property
    def actions(self):
        """The available actions for the current state."""
        return [(a, b) for a in range(3) for b in range(3) if self.state[a, b] != 1]    
    
    
class TicTacToeApp:
    """Application for running a game of Tic-Tac-Toe."""

    def __init__(self, interface):
        self.env = TicTacToeEnv()
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
                agent = MCTSAgent()
                self.play_games(agent)

    def play_games(self, agent):
        """Play games between player and agent."""
        self.interface.show_board()
        while True:
            self.env.reset()
            while not self.env.done:
                self.interface.update_board(self.env.state)
                action = agent.act(self.env)
                _, rewards, _, _ = self.env.step(action)
            self.interface.update_board(self.env.state)
            choice = self.interface.want_to_replay()
            if choice[0].lower() == 'q':
                return


class TextInterface2:
    """Text interface for playing Tic-Tac-Toe."""

    def show_start(self):
        print("Welcome to Tic-Tac-Toe.")

    def want_to_play(self):
        return input("Choose player (1) or (2) or (Q)uit: ")

    def get_action(self):
        return input("Choose a column or (R)estart or (Q)uit: ")
    
    def show_board(self):
        pass

    def update_board(self, board):
        board = np.where(board == 0, "_", np.where(board == 1, "X", "O"))
        print()
        for row in board:
            print("|" + "|".join(row) + "|")
        print()
        print(" " + " ".join(str(x) for x in range(1, 8)) + " ")

    def show_winner(self, winner):
        print("\nPlayer {0} wins".format(winner + 1))
        
    def want_to_replay(self):
        return input("Choose (R)estart or (Q)uit: ")

    def close(self):
        print("\nThanks for playing!")


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
    """Widget for a Tic-Tac-Toe board."""
    
    def __init__(self, win, center):
        self.win = win
        self.background_color = "white"
        self.frame_color = 'white'
        self.piece_colors = ['yellow', 'red']
        self.pieces = [[self._make_piece(Point(100 * (col+1), (100*(row+1))+50), 50)
                        for col in range(3)]
                       for row in range(3)]
        self.crosses=[[(Line(Point((100*(col+1))-25, 100*(row+1)+25), Point((100*(col+1))+25, 100*(row+1)+75)),Line(Point((100*(col+1))-25, 100*(row+1)+75), Point((100*(col+1))+25, 100*(row+1)+25)))
                        for col in range(3)]
                       for row in range(3)]
        
    def _make_piece(self, center, size):
        """Set up the grid of pieces."""
        piece = Rectangle(Point(center.getX()-50,center.getY()-50),Point(center.getX()+50,center.getY()+50))
        piece.setFill(self.frame_color)
        return piece
    
    def draw(self, win):
        for row in range(3):
            for col in range(3):
                self.pieces[row][col].draw(win)

    def undraw(self):
        for row in range(3):
            for col in range(3):
                self.pieces[row][col].undraw()
                self.crosses[row][col][0].undraw()
                self.crosses[row][col][1].undraw()

    def update(self, board):
        """Draw board state on this widget."""
        for row in range(3):
            for col in range(3):
                if board[row, col] == 0:
                    self.pieces[row][col].setFill(self.background_color)
                    self.crosses[row][col][0].undraw()
                    self.crosses[row][col][1].undraw()
                elif board[row, col] == 1:
                    self.crosses[row][col][0].undraw()
                    self.crosses[row][col][1].undraw()
                    self.crosses[row][col][0].draw(self.win)
                    self.crosses[row][col][1].draw(self.win)


class GraphicInterface1:
    
    def __init__(self):
        self.win = GraphWin("Tic Tac Toe", 400, 575)
        self.win.setBackground("white")
        self.banner = Text(Point(200, 50), "")
        self.banner.setSize(25)
        self.banner.setFill("black")
        self.banner.setStyle("bold")
        self.banner.draw(self.win)
        self.start_buttons = [
            Button(self.win, Point(200, 275), 150, 50, "New Game"),
            Button(self.win, Point(200, 425), 150, 50, "Quit"),
        ]
        self.action_buttons = [
            Button(self.win, Point(100, 525), 150, 50, "Restart"),
            Button(self.win, Point(300, 525), 150, 50, "Quit"),
        ]
        self.board = BoardView(self.win, Point(200, 250))

    def show_start(self):
        for b in self.action_buttons:
            b.undraw()
        self.board.undraw()
        self.banner.setText("Tic Tac Toe")
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
                    return label

    def show_board(self):
        for b in self.start_buttons:
            b.undraw()
        self.banner.setText("")
        for b in self.action_buttons:
            b.draw(self.win)
        self.board.draw(self.win)
        
    def update_board(self, board):
        self.board.update(board)
        self.banner.setText("")
        
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

