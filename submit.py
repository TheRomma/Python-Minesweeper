"""
Minesweeper by Jere Koivisto 2020

This module contains the submit class.
"""

import datetime
import tkinter as tk
import menu

class Submit:
    """
    One of the layer classes. Represents the name submit screen after a game.
    """
    def __init__(self, filename, isWin, time, numMoves, width, height, numMines):
        """
        The constructor initializes variables and creates the tkinter window and widgets.
        Params:
            filename: Name of the file storing all the statistics.
            isWin: Did the player win the game or not.
            time: The time it took to play the game.
            numMoves: The number of moves played during the game.
            width: The width of the minefield in cells.
            height: The height of the minefield in cells.
            numMines: The number of active mines in the minefield.
        """
        self.next = None

        self.args = {
            "filename": filename,
            "isWin": isWin,
            "time": time,
            "numMoves": numMoves,
            "width": width,
            "height": height,
            "numMines": numMines
        }

        self.root = tk.Tk()
        self.root.geometry("220x100")
        self.root.resizable(False, False)

        message = ""
        title = ""
        if isWin:
            message = "Congratulations you won!"
            title = "You won!"
        else:
            message = "You blew up."
            title = "You lost"

        self.root.title(title)

        self.winLabel = tk.Label(self.root, text = message)
        self.winLabel.pack()

        self.entryLabel = tk.Label(self.root, text = "Input your name.")
        self.entryLabel.pack()

        self.nameEntry = tk.Entry(self.root)
        self.nameEntry.pack()

        self.button = tk.Button(self.root, text = "Submit", command = self.submitStats)
        self.button.pack()

    def update(self):
        """
        The update method called by the application. Effectively changes the current layer
        into a menu layer when the submit window is destroyed.
        """
        self.root.mainloop()
        return menu.Menu()

    def submitStats(self):
        """
        Writes the given name and statistics into
        the specified file and destroys the tkinter window.
        """
        with open(self.args["filename"], "a") as target:
            minutes, seconds = divmod(self.args["time"], 60)
            timeString = str(int(minutes)) + "m " + str(int(seconds)) + "s"
            target.write("{},{},{},{},{},{},{},{},\n".format(
                datetime.datetime.now(),
                self.nameEntry.get().replace(",", "."),
                self.args["isWin"],
                timeString,
                self.args["numMoves"],
                self.args["width"],
                self.args["height"],
                self.args["numMines"],
            ))
        self.root.destroy()
