#!/usr/bin/env python
"""Entry point for all games."""

from mcts.connectfour import ConnectFourApp, ConnectFourGUI
from mcts.graphics import GraphWin, Point, Text
from mcts.gui import Button
from mcts.tictactoe import TicTacToeApp, TicTacToeGUI
from mcts.checkers import CheckersApp, CheckersGUI


class GraphicalInterface:
    """Top-level graphical interface."""

    def __init__(self):
        self.window = GraphWin("MCTS Games", 400, 575)
        self.banner = Text(Point(200, 50), "Select Game")
        self.banner.setSize(25)
        self.banner.setFill("black")
        self.banner.setStyle("bold")
        self.buttons = [
            Button(self.window, Point(200, 200), 150, 50, "Tic Tac Toe"),
            Button(self.window, Point(200, 275), 150, 50, "Connect Four"),
            Button(self.window, Point(200, 350), 150, 50, "Checkers"),
            Button(self.window, Point(200, 425), 150, 50, "Quit"),
        ]

    def run(self):
        """Run the main application."""
        while True:
            choice = self.choose_game()
            if choice == "Tic Tac Toe":
                app = TicTacToeApp(TicTacToeGUI(self.window))
                self.run_game(app)
            elif choice == "Connect Four":
                app = ConnectFourApp(ConnectFourGUI(self.window))
                self.run_game(app)
            elif choice == "Checkers":
                app = CheckersApp(CheckersGUI(self.window))
                self.run_game(app)
            else:
                self.window.close()
                break

    def choose_game(self):
        """Return the user selected game."""
        self.banner.draw(self.window)
        for b in self.buttons:
            b.draw(self.window)
            b.activate()
        while True:
            p = self.window.getMouse()
            for b in self.buttons:
                if b.clicked(p):
                    return b.getLabel()

    def run_game(self, app):
        """Run the given game app in this window."""
        self.banner.undraw()
        for b in self.buttons:
            b.undraw()
        app.run()


if __name__ == "__main__":
    GraphicalInterface().run()
