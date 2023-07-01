import random
import tkinter as tk
import PIL.Image
from PIL import Image, ImageTk
from random import randrange

# determines which card is displayed
def face(x):
    n = x % 13
    if (n >= 0 and n <= 8):
        return str(n + 2)
    elif (n == 9):
        return "jack"
    elif (n == 10):
        return "queen"
    elif (n == 11):
        return "king"
    elif (n == 12):
        return "ace"

# determines the suit of card depending on suit name
def suit(x):
    if x < 14:
        return "clubs"
    elif x >= 14 and x < 27:
        return "diamonds"
    elif x >= 27 and x > 40:
        return "hearts"
    else:
        return "spades"

# according to file names, returns correct card names
def cardName(x):
    return face(x) + "_of_" + suit(x) + ".png"

# loads deck in an array
def LoadDeck():
    x = []
    for i in range(52):
        img = PIL.Image.open("cards/" + cardName(i))
        img = img.resize((80, 120))
        tkimage = ImageTk.PhotoImage(img)
        x.append(hold(img, tkimage, i))
    return x

# shows cardback for hidden cards
def cardBack():
    img = PIL.Image.open("cards/cardback.png")
    img = img.resize((80, 120))
    tkimage = ImageTk.PhotoImage(img)
    return hold(img, tkimage, 0)

#object created for each elt in image list (array)
class hold:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

class House:
    def __init__(self, name):
        self.name = name
        self.deck = self.shuffle(LoadDeck())
        self.back_card = cardBack()

    # picks cards randomly for each round
    def shuffle(self, deck):
        newDeck = []
        while len(deck) > 0:
            new_card = deck.pop(randrange(0, len(deck)))
            newDeck.append(new_card)
        return newDeck

    # deals randomly picked cards
    def dealCard(self):
        return self.deck.pop()

class player:
    def __init__(self, n, balance, bet):
        self.name = n
        self.balance = balance
        self.bet = bet
        self.hand = []