"""
Minesweeper by Jere Koivisto 2020

This module contains the game class and the readFile function.
"""

import tkinter as tk
import game
import scores

def readFile(filename):
    """
    A simple function for reading the contents of a text file into a string.
    Params:
        filename: Filename of the file to be read.
    """
    stats = []
    try:
        with open(filename) as source:
            for row in source.readlines():
                stats.append(row.strip().split(","))
    except FileNotFoundError:
        return False
    else:
        return stats

class Menu:
    """
    One of the four Layer classes. Represents a menu where the player can choose
    to start a game, look at stats from earlier games and quit the program.
    """
    def __init__(self):
        """
        The constructor initializes necessary variables and creates the menus ui using tkinter.
        """
        self.next = None

        self.root = tk.Tk()
        self.root.title("Minesweeper by Jere Koivisto")
        self.root.resizable(False, False)

        self.wLabel = tk.Label(self.root, text = "Insert width")
        self.wLabel.grid(row = 0, column = 0)
        self.hLabel = tk.Label(self.root, text = "Insert height")
        self.hLabel.grid(row = 0, column = 1)
        self.mLabel = tk.Label(self.root, text = "Insert number of mines")
        self.mLabel.grid(row = 0, column = 2)
        self.sLabel = tk.Label(self.root, text = "Insert graphics scale")
        self.sLabel.grid(row = 0, column = 3)

        self.wEntry = tk.Entry(self.root)
        self.wEntry.grid(row = 1, column = 0)
        self.hEntry = tk.Entry(self.root)
        self.hEntry.grid(row = 1, column = 1)
        self.mEntry = tk.Entry(self.root)
        self.mEntry.grid(row = 1, column = 2)
        self.sEntry = tk.Entry(self.root)
        self.sEntry.insert(tk.END, "1.0")
        self.sEntry.grid(row = 1, column = 3)

        self.startButton = tk.Button(self.root, text = "Start", command = self.start)
        self.startButton.grid(row = 3, column = 0)
        self.endButton = tk.Button(self.root, text = "End", command = self.end)
        self.endButton.grid(row = 3, column = 3)
        self.scoresButton = tk.Button(self.root, text = "Statistics", command = self.scores)
        self.scoresButton.grid(row = 3, column = 1)

    def update(self):
        """
        The update methods for these tkinter based layers don't actually do much.
        They mainly serve as a consistant way to switch layers. The application updates
        the layer via it's layer reference.
        """
        self.root.mainloop()
        return self.next

    def start(self):
        """
        Starts a game of minesweeper using values provided in the entry fields.
        Changes the applications current layer into a Game layer.
        Meant to be called by the start button.
        """
        try:
            width = int(float(self.wEntry.get()))
            height = int(float(self.hEntry.get()))
            mines = int(float(self.mEntry.get()))
            scale = float(self.sEntry.get())
            if width <= 0 or height <= 0 or mines <= 0 or scale <= 0:
                raise ValueError
        except ValueError:
            errorLabel = tk.Label(self.root, text = "Input value must be a positive number!")
            errorLabel.grid(row = 2, column = 0)
        else:
            self.root.destroy()
            self.next = game.Game(width, height, mines, scale)

    def end(self):
        """
        Closes the program. Changes the current layer into nothing effectively closing
        the program. Meant to be called by the quit button.
        """
        self.root.destroy()
        self.next = None

    def scores(self):
        """
        Displays statistics of previous games in a neatly organized grid.
        Changes the current layer into a Score layer.
        Meant to be called by the scores button.
        """
        source = readFile("stats.txt")
        if source:
            self.root.destroy()
            self.next = scores.Scores(source)
        else:
            errorLabel = tk.Label(self.root, text = "No stats detected yet!")
            errorLabel.grid(row = 2, column = 1)
