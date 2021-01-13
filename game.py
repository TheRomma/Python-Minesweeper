"""
Minesweeper by Jere Koivisto 2020

This module contains the game class.
"""

import pyglet
import grid
import menu
import submit

SPRITE_WIDTH = 40
SPRITE_HEIGHT = 40

class Game:
    """
    The most important layer class. This layer encaptulates a game of minesweeper.
    """
    def __init__(self, width, height, numMines, spriteScale = 1.0):
        """
        The contructor initializes variables including a pyglet window,
        sets event handlers and schedules the simulation method.
        Params:
            width: Width of the minefield in cells.
            height: Height of the minefield in cells.
            numMines: Number of mines to be armed.
            spriteScale: Scales graphics by a factor.
        """
        self.next = self

        self.timer = 0
        self.endTimer = 0

        self.input = {
            "hasInput": False,
            "button": 0,
            "x": 0,
            "y": 0
        }

        mines = numMines
        if mines >= width * height:
            mines = width * height - 1

        self.window = pyglet.window.Window(
            int(width * SPRITE_WIDTH * spriteScale),
            int(height * SPRITE_HEIGHT * spriteScale),
            fullscreen = False
            )
        self.window.set_caption("W:" + str(width) + " H:" + str(height) + " M:" + str(mines))

        self.minefield = grid.Grid(width, height, numMines, spriteScale)

        pyglet.clock.schedule_interval(self.simulate, 1/60)

        @self.window.event
        def on_close():
            self.next = menu.Menu()

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self.input["x"] = int(x / (SPRITE_WIDTH * spriteScale))
            self.input["y"] = int(y / (SPRITE_HEIGHT * spriteScale))
            self.input["button"] = button
            self.input["hasInput"] = True

            if self.input["x"] < 0:
                self.input["x"] = 0
            if self.input["y"] < 0:
                self.input["y"] = 0
            if self.input["x"] >= self.minefield.width - 1:
                self.input["x"] = self.minefield.width - 1
            if self.input["y"] >= self.minefield.height - 1:
                self.input["y"] = self.minefield.height - 1

        #print("game created")

    def update(self):
        """
        The update function called by the application. Progresses pyglets clock and
        processes events.
        """
        pyglet.clock.tick()

        event = self.window.dispatch_events()

        if not self.next == self:
            pyglet.clock.unschedule(self.simulate)
            self.window.close()
            del self.window

        return self.next

    def __del__(self):
        #print("game destroyed")
        pass

    def simulate(self, delta):
        """
        The scheduled simulation function. Checks for input and calls
        the input handling method.
        """
        self.timer += delta
        self.draw()

        if self.minefield.hasEnded:
            self.endTimer += delta
            if self.endTimer > 2:
                self.next = submit.Submit(
                    "stats.txt",
                    not self.minefield.hasFailed,
                    self.timer,
                    self.minefield.moveCounter,
                    self.minefield.width,
                    self.minefield.height,
                    self.minefield.numMines)
        else:
            if self.input["hasInput"]:
                self.handleInput()

    def draw(self):
        """
        Draws the minefield.
        """
        self.window.clear()

        self.minefield.draw()

        self.window.flip()

    def handleInput(self):
        """
        Handles input and progresses the game.
        """
        self.minefield.clickCell(self.input["x"], self.input["y"], self.input["button"])
        self.input["hasInput"] = False
