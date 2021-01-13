"""
Minesweeper by Jere Koivisto 2020

This module contains the cell class.
"""
import pyglet

SPRITE_WIDTH = 40
SPRITE_HEIGHT = 40

class Cell:
    """
    A class representing a cell.
    """
    def __init__(self, gridRef, x, y, isMine = False, spriteScale = 1.0):
        """
        The constructor initializes variables and creates a sprite.
        Params:
            gridRef: A reference to the grid the cell is a part of.
            x: X location of the cell in the grid.
            y: Y location of the cell in the grid.
            isMine: Is the cell a mine or not.
            spriteScale: Scales the sprite by a factor.
        """
        self.master = gridRef
        self.isMine = isMine
        self.isFlag = False
        self.isVisible = False
        self.numNeighbours = False
        self.x = x
        self.y = y
        self.sprite = pyglet.sprite.Sprite(
            self.master.getImage("hidden"),
            x = self.x * SPRITE_WIDTH * spriteScale,
            y = self.y * SPRITE_HEIGHT * spriteScale,
            batch = self.master.drawBuffer)
            
        self.sprite.scale = spriteScale
        self.hasFlooded = False

    def setVisibility(self, isVisible):
        """
        Params:
            isVisible: Is the cell visible or not.
        """
        self.isVisible = isVisible
        self.master.visibleCellCounter += 1
        if self.isMine:
            self.sprite.image = self.master.getImage("mine")
        else:
            self.sprite.image = self.master.getImage(str(self.numNeighbours))

    def toggleFlag(self):
        """
        Toggles flag on and off.
        """
        if self.isFlag:
            self.isFlag = False
            self.sprite.image = self.master.getImage("hidden")
        else:
            self.isFlag = True
            self.sprite.image = self.master.getImage("flag")

    def countNeighbours(self):
        """
        Counts the neighbouring mines and assigns numNeighbours with the resulting number.
        """
        field = self.master.field
        xLimit = self.master.width
        yLimit = self.master.height
        count = 0
        x = self.x - 1
        y = self.y - 1

        for i in range(3):
            for j in range(3):
                if x + j == self.x and y + i == self.y:
                    pass
                elif x + j < 0 or y + i < 0:
                    pass
                elif x + j >= xLimit or y + i >= yLimit:
                    pass
                elif field[y + i][x + j].isMine:
                    count += 1

        self.numNeighbours = count

    def reveal(self):
        """
        Reveals the cell either because it was clicked or because it was flooded.
        """
        if self.isVisible or self.isFlag:
            pass
        else:
            self.setVisibility(True)
            if self.isMine:
                self.master.fail()
            elif self.numNeighbours == 0:
                #Continues flooding by returning True
                return True

    def flood(self):
        """
        Called in the grids checkCell method. Returns floodable neighbours.
        """
        field = self.master.field
        xLimit = self.master.width
        yLimit = self.master.height
        x = self.x - 1
        y = self.y - 1

        arr = []

        for i in range(3):
            for j in range(3):
                if x + j == self.x and y + i == self.y:
                    pass
                elif x + j < 0 or y + i < 0:
                    pass
                elif x + j >= xLimit or y + i >= yLimit:
                    pass
                elif field[y + i][x + j].hasFlooded:
                    pass
                elif field[y + i][x + j].isVisible:
                    pass
                elif field[y + i][x + j].isFlag:
                    pass
                elif not field[y + i][x + j].isMine:
                    field[y + i][x + j].hasFlooded = True
                    arr.append(field[y + i][x + j])

        return arr
        