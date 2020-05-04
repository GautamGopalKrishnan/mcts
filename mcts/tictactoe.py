"""A Tic-Tac-Toe game."""

import numpy as np

from .tic import CTicTacToeEnv
from .agents import MCTSAgent
from .graphics import Text, Point, Rectangle, Circle, Line
from .gui import Button


class PyTicTacToeEnv:
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
        copy = PyTicTacToeEnv()
        copy.board = self.board.copy()
        copy.turn = self.turn
        copy.done = self.done
        copy.actions = self.actions.copy()
        return copy

    def render(self):
        print(self.board)

    def winner(self, action):
        r, c = (self.rsum(action[0]), self.csum(action[1]))
        if r in [3, -3]:
            return np.sign(r)
        if c in [3, -3]:
            return np.sign(c)
        if action[0] == action[1]:
            d = self.dsum()
            if d in [3, -3]:
                return np.sign(d)
        if sum(action) == 2:
            a = self.adsum()
            if a in [3, -3]:
                return np.sign(a)
        return None

    def rsum(self, r=0):
        return np.sum(self.board[r, :])

    def csum(self, c=0):
        return np.sum(self.board[:, c])

    def dsum(self):
        return np.sum(self.board[np.arange(3), np.arange(3)])

    def adsum(self):
        return np.sum(self.board[np.arange(3), np.arange(2, -1, -1)])

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)


class TicTacToeApp:
    """Application for running a game of Tic-Tac-Toe."""

    def __init__(self, interface, implementation="python"):
        self.env = PyTicTacToeEnv() if implementation == "python" else CTicTacToeEnv()
        self.interface = interface

    def run(self):
        """Start the application."""
        while True:
            self.interface.show_start()
            choice = self.interface.want_to_play()
            if choice[0].lower() == 'q':
                self.interface.close()
                break
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
                    action = self.interface.get_action(self.env.actions)
                    if action[0].lower() == 'q':
                        return
                    elif action[0].lower() == 'r':
                        self.env.reset()
                        total_rewards = np.zeros(self.env.players)
                        continue
                    else:
                        action = (int(action) // 3, int(action) % 3)
                else:
                    action = agent.act(self.env)
                _, rewards, _, _ = self.env.step(action)
                total_rewards += rewards
            self.interface.update_board(self.env.board)
            if total_rewards[0] == 0:
                self.interface.show_winner(0)
            else:
                self.interface.show_winner(np.argmax(total_rewards)+1)
            choice = self.interface.want_to_replay()
            if choice[0].lower() == 'q':
                return


class TicTacToeTUI:
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


class TicTacToeBoard:
    """Graphical widget for a Tic-Tac-Toe board."""

    def __init__(self, win):
        self.window = win
        self.background_color = "white"
        self.frame_color = 'white'
        self.piece_colors = ['yellow', 'red']
        self.pieces = [[self._make_piece(Point(100 * (col + 1), 100 * (row + 1) + 50))
                        for col in range(3)]
                       for row in range(3)]
        self.circles = [[Circle(Point(100 * (col + 1), 100 * (row + 1) + 50), 25)
                         for col in range(3)]
                        for row in range(3)]
        self.crosses = [[(Line(Point(100 * (col + 1) - 25, 100 * (row + 1) +25),
                               Point(100 * (col + 1) + 25, 100 * (row + 1) +75)),
                          Line(Point(100 * (col + 1) - 25, 100 * (row + 1) +75),
                               Point(100 * (col + 1) + 25, 100 * (row + 1) +25)))
                         for col in range(3)]
                        for row in range(3)]

    def _make_piece(self, center):
        """Set up the grid of pieces."""
        piece = Rectangle(Point(center.getX() - 50, center.getY() - 50),
                          Point(center.getX() + 50, center.getY() + 50))
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
                self.circles[row][col].undraw()
                self.crosses[row][col][0].undraw()
                self.crosses[row][col][1].undraw()

    def update(self, board):
        """Draw board state on this widget."""
        for row in range(3):
            for col in range(3):
                if board[row, col] == -1:
                    self.circles[row][col].undraw()
                    self.circles[row][col].draw(self.window)
                elif board[row, col] == 0:
                    self.pieces[row][col].setFill(self.background_color)
                    self.circles[row][col].undraw()
                    self.crosses[row][col][0].undraw()
                    self.crosses[row][col][1].undraw()
                elif board[row, col] == 1:
                    self.crosses[row][col][0].undraw()
                    self.crosses[row][col][1].undraw()
                    self.crosses[row][col][0].draw(self.window)
                    self.crosses[row][col][1].draw(self.window)


class TicTacToeGUI:
    """Graphical interface for playing Tic-Tac-Toe."""

    def __init__(self, window):
        self.window = window
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
        self.action_buttons = [
            Button(self.window, Point(100, 150), 100, 100, "0"),
            Button(self.window, Point(200, 150), 100, 100, "1"),
            Button(self.window, Point(300, 150), 100, 100, "2"),
            Button(self.window, Point(100, 250), 100, 100, "3"),
            Button(self.window, Point(200, 250), 100, 100, "4"),
            Button(self.window, Point(300, 250), 100, 100, "5"),
            Button(self.window, Point(100, 350), 100, 100, "6"),
            Button(self.window, Point(200, 350), 100, 100, "7"),
            Button(self.window, Point(300, 350), 100, 100, "8"),
            Button(self.window, Point(100, 525), 150, 50, "Restart"),
            Button(self.window, Point(300, 525), 150, 50, "Quit"),
        ]
        self.board = TicTacToeBoard(self.window)

    def show_start(self):
        for b in self.action_buttons:
            b.undraw()
        self.board.undraw()
        self.banner.setText("Tic Tac Toe")
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

    def get_action(self, actions):
        self.banner.setText("Your turn")
        for i in range(3):
            for j in range(3):
                if (i, j) in actions:
                    self.action_buttons[3*i + j].activate()
                else:
                    self.action_buttons[3*i + j].deactivate()
        self.action_buttons[9].activate()
        self.action_buttons[10].activate()
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
        if winner == 0:
            self.banner.setText("It's a tie!")
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
