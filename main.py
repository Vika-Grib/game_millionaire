"""
Main module
"""

import os
from game import Game
from colors import *


def showPrompt(userName):
    """
    Show prompt to play the game
    :param userName: player's name
    :return: player's input
    """
    promptStr = f"\n{userName}, do you want to play a new game? (y/n): "
    startGame = input(promptStr)

    while startGame not in ['y', 'Y', 'n', 'N']:
        printRed("\nIncorrect answer. Please, try again.")
        startGame = input(promptStr)
    return startGame


def main():
    """
    The program starts here
    :return: None
    """
    userName = input("\nPlease, enter your name: ").upper()
    startGame = showPrompt(userName)

    while startGame in ['y', 'Y']:
        game = Game(userName)
        game.start()
        del game
        startGame = showPrompt(userName)

    printBlue(f'\n{userName}, see you next time!')


if __name__ == "__main__":
    main()