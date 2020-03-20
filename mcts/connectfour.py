"""A Connect Four game"""

from .agents import MCTSAgent
from .graphics import GraphWin, Text, Point, Rectangle, Circle

import numpy as np


class ConnectFourEnv:
    """An environment for two-player connect-four."""

    def __init__(self):
        self.players = 2
        self.reset()

    def reset(self):
        """Initialize a new game and return state and turn."""
        self.state = np.zeros((6, 7), dtype=np.int)
        self.done = False
        self.actions = list(range(7))
        self.turn = 0

    def step(self, action):
        """Perform action and return new state, rewards, done, and turn."""
        move=(max([i for i in range(6) if self.state[i,action]==0]),action)
        assert self.state[move] == 0
        self.state[move] = (-1) ** self.turn
        winner = self.winner(move)
        if winner is not None:
            rewards = np.array([winner,(-1)*winner])
        else:
            rewards = np.array([0,0])
        self.done = winner is not None or np.all(self.state != 0)
        self.turn = (self.turn + 1) % 2
        if self.done:
            self.actions = []
        else:
            self.actions = [i for i in range(7) if self.state[0,i]==0]
        return self.state.copy(), rewards, self.done, self.turn

    def copy(self):
        copy = ConnectFourEnv()
        copy.state = self.state.copy()
        copy.turn = self.turn
        copy.done = self.done
        copy.actions = self.actions.copy()
        return copy

    def render(self):
        print(self.state)

    def winner(self,move):
        if (self.rcheck(move),self.ccheck(move),self.dcheck(move),self.acheck(move))!=(0,0,0,0):
            return np.sign(self.state[move])
        return None
        
    def rcheck(self,move):
        for i in range(4):
            if np.sum(self.state[move[0]][i:i+4])==4*self.state[move]:
                return 1
        return 0    
            
    def ccheck(self,move):
        if np.sum(self.state[move[0]:min(move[0]+4,6),move[1]])==4*self.state[move]:
            return 1
        return 0
    
    def dcheck(self,move):
        l=self.state.copy().diagonal(move[1]-move[0])
        for i in range(len(l)-3):
            if np.sum(l[i:i+4])==4*self.state[move]:
                return 1
        return 0
    
    def acheck(self,move):
        l=self.state.copy()[::-1,:].diagonal(move[1]+move[0]-5)
        for i in range(len(l)-3):
            if np.sum(l[i:i+4])==4*self.state[move]:
                return 1
        return 0


class ConnectFourApp:
    """Application for running a game of Connect Four."""

    def __init__(self, interface):
        self.env = ConnectFourEnv()
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
                    action = self.interface.get_action()
                    if action[0].lower() == 'q':
                        return
                    elif action[0].lower() == 'r':
                        self.env.reset()
                        total_rewards = np.zeros(self.env.players)
                        continue
                    else:
                        action = int(action) - 1
                else:
                    action = agent.act(self.env)
                _, rewards, _, _ = self.env.step(action)
                total_rewards += rewards
            self.interface.update_board(self.env.state)
            self.interface.show_winner(np.argmax(total_rewards))
            choice = self.interface.want_to_replay()
            if choice[0].lower() == 'q':
                return


class TextInterface:
    """Text interface for playing Connect Four."""

    def show_start(self):
        print("Welcome to Connect Four.")

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
    """Widget for a Connect Four board."""
    
    def __init__(self, win, center):
        self.win = win
        self.background_color = "white"
        self.frame_color = 'blue'
        self.piece_colors = ['yellow', 'red']
        cx, cy = center.getX(), center.getY()
        self.rect = Rectangle(Point(cx - 175, cy - 150),
                              Point(cx + 175, cy + 150))
        self.rect.setFill(self.frame_color)
        self.pieces = [[self._make_piece(Point(50 + 50 * col, 125 + 50 * row), 50)
                        for col in range(7)]
                       for row in range(6)]
        
    def _make_piece(self, center, size):
        """Set up the grid of pieces."""
        piece = Circle(center, size / 2 - 1)
        piece.setFill(self.background_color)
        piece.setOutline(self.frame_color)
        return piece
    
    def draw(self, win):
        self.rect.draw(win)
        for row in range(6):
            for col in range(7):
                self.pieces[row][col].draw(win)

    def undraw(self):
        self.rect.undraw()
        for row in range(6):
            for col in range(7):
                self.pieces[row][col].undraw()

    def update(self, board):
        """Draw board state on this widget."""
        for row in range(6):
            for col in range(7):
                if board[row, col] == -1:
                    self.pieces[row][col].setFill(self.piece_colors[0])
                elif board[row, col] == 0:
                    self.pieces[row][col].setFill(self.background_color)
                elif board[row, col] == 1:
                    self.pieces[row][col].setFill(self.piece_colors[1])


class GraphicInterface:
    
    def __init__(self):
        self.win = GraphWin("Connect Four", 400, 575)
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
            Button(self.win, Point(50, 450), 50, 50, "1"),
            Button(self.win, Point(100, 450), 50, 50, "2"),
            Button(self.win, Point(150, 450), 50, 50, "3"),
            Button(self.win, Point(200, 450), 50, 50, "4"),
            Button(self.win, Point(250, 450), 50, 50, "5"),
            Button(self.win, Point(300, 450), 50, 50, "6"),
            Button(self.win, Point(350, 450), 50, 50, "7"),
            Button(self.win, Point(100, 525), 150, 50, "Restart"),
            Button(self.win, Point(300, 525), 150, 50, "Quit"),
        ]
        self.board = BoardView(self.win, Point(200, 250))

    def show_start(self):
        for b in self.action_buttons:
            b.undraw()
        self.board.undraw()
        self.banner.setText("Connect Four")
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
        self.banner.setText("Player {} wins!".format(winner + 1))
        
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
