"""A Connect Four game."""

import numpy as np

from .agents import MCTSAgent
from .graphics import GraphWin, Text, Point, Rectangle, Circle
from .gui import Button


class ConnectFourEnv:
    """An environment for two-player connect-four."""

    def __init__(self):
        self.players = 2
        self.reset()

    def reset(self):
        """Initialize a new game."""
        self.board = np.zeros((6, 7), dtype=np.int)
        self.done = False
        self.actions = list(range(7))
        self.turn = 0

    def step(self, action):
        """Perform action and return new board, rewards, done, and turn."""
        move = (max([i for i in range(6) if self.board[i, action] == 0]), action)
        assert self.board[move] == 0
        self.board[move] = (-1) ** self.turn
        winner = self.winner(move)
        if winner is not None:
            rewards = np.array([winner, (-1) * winner])
        else:
            rewards = np.array([0, 0])
        self.done = winner is not None or np.all(self.board != 0)
        self.turn = (self.turn + 1) % 2
        if self.done:
            self.actions = []
        else:
            self.actions = [i for i in range(7) if self.board[0, i] == 0]
        return self.board.copy(), rewards, self.done, self.turn

    def copy(self):
        copy = ConnectFourEnv()
        copy.board = self.board.copy()
        copy.turn = self.turn
        copy.done = self.done
        copy.actions = self.actions.copy()
        return copy

    def render(self):
        print(self.board)

    def winner(self, move):
        if (self.rcheck(move), self.ccheck(move), self.dcheck(move), self.acheck(move)) != (0, 0, 0, 0):
            return np.sign(self.board[move])
        return None

    def rcheck(self, move):
        for i in range(4):
            if np.sum(self.board[move[0]][i:i+4]) == 4 * self.board[move]:
                return 1
        return 0

    def ccheck(self, move):
        if np.sum(self.board[move[0]:min(move[0] + 4, 6), move[1]]) == 4 * self.board[move]:
            return 1
        return 0

    def dcheck(self, move):
        l = self.board.copy().diagonal(move[1] - move[0])
        for i in range(len(l) - 3):
            if np.sum(l[i:i+4]) == 4 * self.board[move]:
                return 1
        return 0

    def acheck(self, move):
        l = self.board.copy()[::-1, :].diagonal(move[1] + move[0] - 5)
        for i in range(len(l) - 3):
            if np.sum(l[i:i+4]) == 4 * self.board[move]:
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
                        action = int(action) - 1
                else:
                    action = agent.act(self.env)
                _, rewards, _, _ = self.env.step(action)
                total_rewards += rewards
            self.interface.update_board(self.env.board)
            if total_rewards[0] == 0:
                self.interface.show_winner(0)
            else:
                self.interface.show_winner(np.argmax(total_rewards) + 1)
            choice = self.interface.want_to_replay()
            if choice[0].lower() == 'q':
                return


class ConnectFourTUI:
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
        if winner == 0:
            print("It's a tie!")
        else:
            print("\nPlayer {0} wins".format(winner))

    def want_to_replay(self):
        return input("Choose (R)estart or (Q)uit: ")

    def close(self):
        print("\nThanks for playing!")


class ConnectFourBoard:
    """Graphical widget for a Connect Four board."""

    def __init__(self, win, center):
        self.window = win
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


class ConnectFourGUI:
    """Graphical interface for playing Connect Four."""

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
            Button(self.window, Point(50, 450), 50, 50, "1"),
            Button(self.window, Point(100, 450), 50, 50, "2"),
            Button(self.window, Point(150, 450), 50, 50, "3"),
            Button(self.window, Point(200, 450), 50, 50, "4"),
            Button(self.window, Point(250, 450), 50, 50, "5"),
            Button(self.window, Point(300, 450), 50, 50, "6"),
            Button(self.window, Point(350, 450), 50, 50, "7"),
            Button(self.window, Point(100, 525), 150, 50, "Restart"),
            Button(self.window, Point(300, 525), 150, 50, "Quit"),
        ]
        self.board = ConnectFourBoard(self.window, Point(200, 250))

    def show_start(self):
        for b in self.action_buttons:
            b.undraw()
        self.board.undraw()
        self.banner.setText("Connect Four")
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
        for i in range(7):
            if i in actions:
                self.action_buttons[i].activate()
            else:
                self.action_buttons[i].deactivate()
        self.action_buttons[7].activate()
        self.action_buttons[8].activate()
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
