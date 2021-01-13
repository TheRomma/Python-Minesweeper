"""
Minesweeper by Jere Koivisto 2020

This module contains the main function.
"""
import application
import menu

def main():
    """
    The main function of the program.
    """
    app = application.Application()
    app.initializeLayer(menu.Menu())
    app.run()

if __name__ == "__main__":
    main()
