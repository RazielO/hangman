# -*- coding: utf-8 -*-
import os

def menu(first, language):
    """
    Shows the menu at the beginning of the game to select the language.

    If its the first time, it only shows the language menu, otherwise, it
    asks the user if he wants to continue.

    Returns 1, 2 or -1 (English, Spanish, Stop the game)
    """
    selection = 0

    language_selection = """Select the language / Selecciona el idioma
Write the number of the language / Escribe el número del idioma
    1. English
    2. Español"""

    again = "Do you want to play again? [y/n]" if language == 1 else "¿Quiéres jugar de nuevo? [y/n]"

    if first:
        print(language_selection)
        selection = int(input())
        return selection
    else:
        print(again)
        response = str(input())
        try:
            if response == 'y' or response == 'Y':
                os.system('clear')
                print(language_selection)
                selection = int(input())
                return selection
            else:
                return -1
        except ValueError:
            return -1
