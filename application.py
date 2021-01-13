"""
Minesweeper by Jere Koivisto 2020

This module contains the application class.
"""
class Application:
    """
    A class representing the program as a whole. Contains the main loop of the program.
    """
    def __init__(self):
        """
        Basic constructor.
        """
        self.alive = True
        self.layer = None

    def initializeLayer(self, layer):
        """
        Gives application an instance of a Layer.
        Param:
            layer: A reference to an instance of a Layer.
        """
        self.layer = layer

    def run(self):
        """
        Starts the programs main loop. Continuously updates it's current layer.
        When layers need to be changed, the current layer constructs and returns
        a reference to the new layer before destroying itself.
        """
        while self.alive:
            self.layer = self.layer.update()

            if not self.layer:
                self.alive = False
