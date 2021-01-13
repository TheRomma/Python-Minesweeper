"""
Minesweeper by Jere Koivisto 2020

This module contains the scores class.
"""

import tkinter as tk
import menu

class Scores:
    """
    A class that represents a stats screen. One of the four layer classes.
    """
    def __init__(self, source):
        """
        The constructor creates and fills the grid with statistics.
        Params:
            source: The statistics in a list in list two dimentional matrix.
        """
        self.next = None

        self.root = tk.Tk()
        self.root.title("Game stats")
        self.root.resizable(False, False)

        self.stats = source

        tk.Label(self.root, text = "Date").grid(row = 0, column = 0)
        tk.Label(self.root, text = "Name").grid(row = 0, column = 1)
        tk.Label(self.root, text = "Win").grid(row = 0, column = 2)
        tk.Label(self.root, text = "Time").grid(row = 0, column = 3)
        tk.Label(self.root, text = "Moves").grid(row = 0, column = 4)
        tk.Label(self.root, text = "Width").grid(row = 0, column = 5)
        tk.Label(self.root, text = "Height").grid(row = 0, column = 6)
        tk.Label(self.root, text = "Mines").grid(row = 0, column = 7)

        for i, row in enumerate(reversed(self.stats)):
            for j, element in enumerate(row):
                tk.Label(self.root, text = str(element)).grid(row = i + 1, column = j)

    def update(self):
        """
        Serves as a way to change the layer back to a menu.
        """
        self.root.mainloop()
        return menu.Menu()
