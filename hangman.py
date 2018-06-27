# -*- coding: utf-8 -*-
import os, time, random, unicodedata
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from menu import menu

translation = {'letters': ['Letters already played:\n', 'Letras ya jugadas:\n'],
               'exit': ['Press enter to continue.', 'Presiona enter para continuar.'],
               'won': ['YOU WON!!', 'GANASTE!!'],
               'lost': ['YOU LOST  :(  The word was {}', 'PERDISTE  :(  La palabra era {}'],
               'l_input': ['Write a letter: ', 'Escribe una letra: '],
               'played': ['The letter you wrote was already played.\nWrite another letter: ', 'La letra que escribiste ya la habias jugado.\nEscribe otra letra: '],
               'char': ['Write just one character.\nWrite another letter: ', 'Escribe solo un caracter.\nEscribe otra letra: ']}


def restart():
    """
    Resets all the variables and clears the terminal
    """

    global turn, word, current, played, again, length

    turn = 1
    word = generate_word()
    current = ''.join([' ' for i in range(len(word))])
    os.system('cls' if os.name == 'nt' else 'clear')
    played = []
    again = False
    length = False


def elimina_tildes(s):
    """
    Deletes the accent marks
    """

    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


def letters_played():
    """
    Returns a string with all the letters that have been played
    """

    global played, language

    s = translation['letters'][language - 1]

    for l in played:
        s = s + l.upper() + ' '
    return s + '\n'


def has_been_played(letter):
    """
    Checks if the letter was already been played
    """

    global played

    if letter in played:
        return True
    else:
        played.append(letter)
        return False


def is_a_vowel(letter):
    """
    Checks if the letter played is a vowel
    """

    vowels = ['a', 'e', 'i', 'o', 'u']
    return letter in vowels


def generate_word():
    """
    Makes a request to a webpage and scrapes the random word according to
    the language
    """

    global language

    if language == 2:
        req = Request('https://www.palabrasque.com/palabra-aleatoria.php', headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html5lib")
        temp = soup.find('font', attrs={'data': 'palabra'}).b.text.lower().strip()
    else:
        req = Request('http://creativitygames.net/random-word-generator/randomwords/1')
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html5lib")
        temp = soup.find('li', attrs={'id': 'randomword_1'}).text

    if ' ' in temp:
        generate_word()
    else:
        return temp


def check_letter(word, letter):
    """
    Checks if the given letter is in the given word
    """

    return letter in word


def new_letter(word, letter, current):
    """
    Makes the new current string with the letter played
    """

    s = ''
    if language == 2:
        w = elimina_tildes(word)
        for i in range(len(word)):
            if w[i] == letter:
                s = s + word[i].upper()
            else:
                s = s + current[i].upper()
    else:
        for i in range(len(word)):
            if word[i] == letter:
                s = s + word[i].upper()
            else:
                s = s + current[i].upper()
    return s


def oportunity(n, word):
    os.system('cls' if os.name == 'nt' else 'clear')
    s = ''
    w = ''
    for _ in range(len(word)):
        s = s + '___ '

    for x in range(len(word)):
        w = w + ' ' + word[x] + '  '

    with open(str(n) + '.txt', 'r') as f:
        print(f.read() + '\n' + w + '\n' + s + '\n\n')


def should_end():
    """
    Checks the conditions for the game to end
    """

    global turn, current

    if current == word.upper() or turn == 7:
        if current == word.upper():
            print(translation['won'][language - 1] + '\n' + exit)
        else:
            print(translation['lost'][language - 1].format(word.upper()) + '\n' + exit)
        input()
        os.system('cls' if os.name == 'nt' else 'clear')
        return True
    return False


def read_letter():
    """
    Reads and returns the new letter the user has written
    """

    global again, length

    if not again:
        l = str(input(translation['l_input'][language - 1]))
    else:
        if not length:
            l = str(input(translation['played'][language - 1]))
        else:
            l = str(input(translation['char'][language - 1]))
    return l.lower()


def new_turn():
    """
    If the letter given by the user is in the word, calls the new_letter method
    to generate a new current string, if is not in the word, the user looses a
    turn. If the string is not just one character or has been already played,
    asks for another letter
    """

    global again, length, turn, current

    l = read_letter()

    if len(l) == 1 and not has_been_played(l):
        again = False
        length = False
        if check_letter(word, l):
            current = new_letter(word, l, current)
        else:
            turn = turn + 1
    else:
        again = True
        if len(l) > 1:
            length = True


def game():
    """
    While the user hasn't guessed the word or hasn't lost, the game continues
    """

    global current, turn

    while current != word or turn != 7:
        oportunity(turn, current)

        if should_end():
            break

        print(letters_played())
        new_turn()


if __name__ == '__main__':
    global turn, word, current, language

    first = True
    language = menu(first, 2)
    exit =  translation['exit'][language - 1]

    while language != -1:
        restart()
        first = False

        game()

        language = menu(first, language)
        exit =  translation['exit'][language - 1]
