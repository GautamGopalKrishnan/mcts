"""Basic Tic-Tac-Toe game."""

from .agents import MCTSAgent
from .graphics import GraphWin, Text, Point, Rectangle, Circle


import numpy as np


class TicTacToeEnv:
    """An environment for two-player tic-tac-toe."""

    def __init__(self):
        self.players = 2
        self.reset()

    def reset(self):
        """Initialize a new game."""
        self.board = np.zeros((3, 3), dtype=np.int)
        self.turn = 0
        self.done = False
        self.actions = [(a, b) for a in range(3) for b in range(3)]

    def step(self, action):
        """Perform action and return new state, rewards, done, and turn."""
        assert self.board[action] == 0
        self.board[action] = (-1) ** self.turn
        self.turn = (self.turn + 1) % 2
        winner = self.winner(action)
        if winner is not None:
            rewards = np.array([winner,(-1)*winner])
        else:
            rewards = np.array([0, 0])
        self.done = winner is not None or np.all(self.board != 0)
        if self.done:
            self.actions = []
        else:
            self.actions = [(a, b) for a in range(3) for b in range(3) if self.board[a, b] == 0]
        return self.board.copy(), rewards, self.done, self.turn

    def copy(self):
        copy = TicTacToeEnv()
        copy.board = self.board.copy()
        copy.turn = self.turn
        copy.done = self.done
        copy.actions = self.actions.copy()
        return copy

    def render(self):
        print(self.board)

    def winner(self,action):
        (r,c)=(self.rsum(action[0]),self.csum(action[1]))
        if r==3 or r==-3:
            return np.sign(r)
        if c==3 or c==-3:
            return np.sign(c)
        if (action[0]==action[1]):
            d=self.dsum()
            if d==3 or d==-3:
                return np.sign(d)
        if (sum(action)==2):
            a=self.adsum()
            if a==3 or a==-3:
                return np.sign(a)
        return None
    
    def rsum(self,r=0):
        return np.sum(self.board[r, :])
    
    def csum(self,c=0):
        return np.sum(self.board[:, c])
    
    def dsum(self):
        return np.sum(self.board[np.arange(3), np.arange(3)])
        
    def adsum(self):
        return np.sum(self.board[np.arange(3), np.arange(2, -1, -1)])

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)
    
    
    
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
                self.interface.update_board(self.env.board)
                if self.env.turn == player:
                    action = self.interface.get_action()
                    if action[0].lower() == 'q':
                        return
                    elif action[0].lower() == 'r':
                        self.env.reset()
                        total_rewards = np.zeros(self.env.players)
                        continue
                    else:
                        action = (int(action)//3,int(action)%3)
                else:
                    action = agent.act(self.env)
                _, rewards, _, _ = self.env.step(action)
                total_rewards += rewards
            self.interface.update_board(self.env.board)
            if total_rewards[0]==0:
                self.interface.show_winner(0)
            else:
                self.interface.show_winner(np.argmax(total_rewards)+1)
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

    def update(self, board):
        """Draw board state on this widget."""
        for row in range(3):
            for col in range(3):
                if board[row, col] == -1:
                    self.pieces[row][col].setFill(self.piece_colors[0])
                elif board[row, col] == 0:
                    self.pieces[row][col].setFill(self.background_color)
                elif board[row, col] == 1:
                    self.pieces[row][col].setFill(self.piece_colors[1])


class GraphicInterface2:
    
    def __init__(self):
        self.win = GraphWin("Tic Tac Toe", 400, 575)
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
        self.action_buttons = [
            Button(self.win, Point(100, 150), 100, 100, "0"),
            Button(self.win, Point(200, 150), 100, 100, "1"),
            Button(self.win, Point(300, 150), 100, 100, "2"),
            Button(self.win, Point(100, 250), 100, 100, "3"),
            Button(self.win, Point(200, 250), 100, 100, "4"),
            Button(self.win, Point(300, 250), 100, 100, "5"),
            Button(self.win, Point(100, 350), 100, 100, "6"),
            Button(self.win, Point(200, 350), 100, 100, "7"),
            Button(self.win, Point(300, 350), 100, 100, "8"),
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

    def get_action(self):
        self.banner.setText("Your turn")
        for b in self.action_buttons:
            b.activate()
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

