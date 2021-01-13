"""
Minesweeper by Jere Koivisto 2020

This module contains the grid class.
"""
import random
import pyglet
import cell

class Grid:
    """
    A class representing the minefield. Essentially a grid build from
    cells.
    """
    def __init__(self, width, height, numMines, spriteScale = 1.0):
        """
        The constructor initializes variables.
        Params:
            width: Width of the grid in cells.
            hieght: Height of the grid in cells.
            numMines: Number of mines to be armed.
            spriteScale: Scales the width of sprites by a factor.
        """
        self.width = width
        self.height = height
        self.numMines = numMines
        if numMines >= width * height:
            self.numMines = width * height - 1
        self.moveCounter = 0
        self.isArmed = False
        self.hasEnded = False
        self.hasFailed = False
        self.images = self.loadImages("spritet")
        self.drawBuffer = pyglet.graphics.Batch()
        self.visibleCellCounter = 0

        self.field = []
        for i in range(height):
            self.field.append([])
            for j in range(width):
                self.field[i].append(cell.Cell(self, j, i, False, spriteScale))

    def loadImages(self, path):
        """
        Loads images from a folder and returns them.
        Params:
            path: Filepath to the folder.
        """
        pyglet.resource.path = [path]
        images = {}
        images["hidden"] = pyglet.resource.image("ruutu_selka.png")
        images["0"] = pyglet.resource.image("ruutu_tyhja.png")
        for i in range(1, 9):
            images[str(i)] = pyglet.resource.image("ruutu_{}.png".format(i))
        images["mine"] = pyglet.resource.image("ruutu_miina.png")
        images["flag"] = pyglet.resource.image("ruutu_lippu.png")

        return images

    def getImage(self, imgName):
        """
        A getter for images.
        Params:
            imgName: Name of the image to be retrieved.
        """
        return self.images[imgName]

    def arm(self, safeCoord):
        """
        Arms the minefield with numMines number of mines. One cell is quaranteed safe and
        it's going to be the first clicked cell.
        Params:
            safeCoord: A tuple containing the (x, y) coordinates of the one
                        quaranteed safe cell.
        """
        self.isArmed = True

        freelist = []
        for i in range(self.height):
            for j in range(self.width):
                freelist.append((j, i))

        freelist.remove(safeCoord)

        random.seed()
        for k in range(self.numMines):
            index = random.randint(0, len(freelist) - 1)
            pos = freelist[index]
            del freelist[index]
            self.field[pos[1]][pos[0]].isMine = True

        for i in range(self.height):
            for j in range(self.width):
                self.field[i][j].countNeighbours()

    def clickCell(self, x, y, button):
        """
        A method called in the game layer. Determines what happens when a cell is clicked.
        """
        cell = self.field[y][x]
        if cell.isVisible:
            pass
        else:
            if not self.isArmed:
                self.arm((x, y))

            if button == 4:
                cell.toggleFlag()
                self.moveCounter += 1
            else:
                if cell.isFlag:
                    pass
                else:
                    self.moveCounter += 1
                    self.revealCell(cell)


        if self.checkWin() and not self.hasFailed:
            self.win()

    def checkWin(self):
        """
        Checks if the win condition of minesweeper (All safe cells are revealed) is met.
        """
        cellCount = self.width * self.height - self.numMines
        return self.visibleCellCounter == cellCount

    def win(self):
        """
        A method for initiating the victory proceedings.
        """
        self.showAll()
        self.hasFailed = False
        self.hasEnded = True

    def fail(self):
        """
        A method for initiating the failure proceedings.
        """
        self.showAll()
        self.hasFailed = True
        self.hasEnded = True

    def draw(self):
        """
        Calls the draw function of the pyglet batch drawBuffer.
        """
        self.drawBuffer.draw()

    def showAll(self):
        """
        Sets all cells visible.
        """
        for i in range(self.height):
            for j in range(self.width):
                self.field[i][j].setVisibility(True)

    def revealCell(self, cell):
        """
        Calls cells reveal method and is in charge of flooding.
        """
        arr = [cell]

        while arr:
            c = arr[-1]
            arr.pop()
            startFlood = c.reveal()
            if startFlood:
                arr.extend(c.flood())
