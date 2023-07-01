import tkinter as tk
import PIL.Image
from PIL import ImageTk
from tkinter import *
import random
from Class import*

# using states, we will determine when the player is allowed to do certain actions
gameState = "start"

# variables for betting
totalMoney = 500
moneyWon = 00

# calculates score of each card
def totalScore(hand):
    score = 0
    numAce = 0
    for i in range(len(hand)):
        card = hand[i].c
        value = card % 13
        value = int(value)
        value = value + 2
        if value >= 11 and value <= 13:
            value = 10
        elif value > 13:
            value = 11
            numAce += 1
        score = score + value
      # decreases ace score if bust
        while score > 21 and numAce > 0:
            score -= 10
            numAce -= 1
    return score

#sets up everything on the gameboard other than the deck
class background:
    def __init__(self, root):
        self.root = root
        self.y = []
        img = PIL.Image.open("cards/" + "green2.png")
        img = img.resize((80, 120))
        tkimage = PIL.ImageTk.PhotoImage(img)
        self.y.append(hold(img, tkimage, -1))
        for i in range(12):
            for j in range(5):
                tk.Label(self.root, background='green4',
                         image=self.y[0].b).grid(
                             row=j, column=i) 

# Create Buttons
        button1 = Button(root, text="Start", command=lambda: Start())
        button1.grid(row=0, column=5)

        button2 = Button(root, text="Hit", command=lambda: hitFunc(p))
        button2.grid(row=0, column=7)

        button3 = Button(root, text="Stay", command=lambda: stayFunc())
        button3.grid(row=0, column=6)

        button4 = Button(root, text="Clear", command=lambda: clearDeck(self))
        button4.grid(row=0, column=8)


        # Player score
        self.playerScore = tk.Entry(self.root, width=5)
        self.playerScore.grid(row=2, column=1)
        self.playerScore.delete(0, tk.END)
        self.playerScore.insert(0, "Score")

        playerlabel = tk.Label (self.root, text="Player", width = 7) 
        playerlabel.grid(row=2,column=0)
      
        # Dealer score
        self.dealerScore = tk.Entry(self.root, width=5)
        self.dealerScore.grid(row=0, column=1)
        self.dealerScore.delete(0, tk.END)
        self.dealerScore.insert(0, "Score")

        dealerlabel = tk.Label (self.root, text="Dealer", width = 7) 
        dealerlabel.grid(row=0,column=0)

        #Player Amount
        newlabel = tk.Label (self.root,text = "Total",width = 7) 
        newlabel.grid(row=2,column=3)
        self.totalAmount = tk.Entry(self.root, width=6)
        self.totalAmount.grid(row=2, column=4)
        self.totalAmount.delete(0, tk.END)
        if gameState == 'start':
          self.totalAmount.insert(0, "500")

        #Betting
        newlabel2 = tk.Label (self.root,text = "Betted",width = 7) 
        newlabel2.grid(row=2,column=6)
        self.betAmount = tk.Entry(self.root, width=7)
        self.betAmount.grid(row=2, column=7)
        self.betAmount.delete(0, tk.END)
        self.betAmount.insert(0, "Enter bet")

        #Winner Label
        newlabel3 = tk.Label (self.root,text = "Winner",width = 7) 
        newlabel3.grid(row=4,column=4)
        self.winnerName = tk.Entry(self.root, width=6)
        self.winnerName.grid(row=4, column=5)
        self.winnerName.delete(0, tk.END)
        self.winnerName.insert(0, "")



# Function that starts the game and deals two cards to each party
def Start():
  global totalMoney, moneyWon
  global gameState
  playerBet = table.betAmount.get()
  if gameState == "start":
      gameState = "playing"
      # If player forgets to bet a specific amount, the house will automatically bet $10 for the player
      if playerBet == "Enter bet" :
        table.betAmount.delete(0, tk.END)
        playerBet = "10"
        table.betAmount.insert(1, str(playerBet))
        
      for i in range(2):
          p.hand.append(h.dealCard())
          d.hand.append(h.dealCard())
      #hide one dealer card
      dealerHand(hide=True)
      playerHand()
      
     
      score = totalScore(p.hand)
      if score == 21:
          dealerSc = totalScore(d.hand)
          dealerHand()
          dScore()

          if dealerSc == 21:
            winner = "Tie"
            table.winnerName.insert(1, winner)
            dealerSc = totalScore(d.hand)
          
# deals player hand
def playerHand():
    x = p.hand
    for i in range(len(x)):
        tk.Label(root, image=x[i].b).grid(row=3, column=i)
    # calculates player score
    score = totalScore(p.hand)
    table.playerScore.delete(0, tk.END)
    table.playerScore.insert(1, str(score))

# deals dealer hand
def dealerHand(hide=False):
    x = d.hand
    for i in range(len(x)):
        if i == len(x) - 1 and hide:
          # When hide is true, a card back is shown instead 
            tk.Label(root, image=h.back_card.b).grid(row=1, column=i)
        else:
            tk.Label(root, image=x[i].b).grid(row=1, column=i)

# shows dealer's score seperately as it is initially hidden
def dScore():
  dealerSc = totalScore(d.hand) 
  table.dealerScore.delete(0, tk.END)
  table.dealerScore.insert(1, str(dealerSc))

# hit function adds card to player deck
def hitFunc(player):
    global gameState, totalMoney, moneyWon 
    if gameState == "playing":
        score = totalScore(player.hand)

        # Deals cards only if it is under 21
        if score < 21:
            player.hand.append(h.dealCard())
            new_score = totalScore(player.hand)
            playerHand()

            # if player busts, dealer's cards are revealed
            if new_score >= 21:
                dealerHand()
                dealerSc = totalScore(d.hand)
                dScore()

                # ff dealer has natural, dealer wins
                if dealerSc == 21:
                    winner = "Dealer"

                    # Calculates player amount and bet
                    playerBet = table.betAmount.get()
                    moneyWon -= int(playerBet)
                    totalMoney -= int(playerBet)
                    table.totalAmount.delete(0, tk.END)
                    table.totalAmount.insert(1, str(totalMoney))
                    # displays dealer as winner
                    table.winnerName.delete(0, tk.END)
                    table.winnerName.insert(1, winner)
                else:
                    # if dealer is under 17, they have to hit
                    while dealerSc < 17:
                        d.hand.append(h.dealCard())
                        dealerSc = totalScore(d.hand)
                        dealerHand()
                        dScore()
                    winner = isWinner()
                    playerBet = table.betAmount.get()

                    if winner == "Player":
                      totalMoney += int(playerBet)
                      moneyWon += int(playerBet)
                    elif winner == "Dealer":
                      totalMoney -= int(playerBet)
                      moneyWon -= int(playerBet)
                    else:
                      totalMoney = int(totalMoney)
                      moneyWon = int(moneyWon)

                    dScore()

                    table.totalAmount.delete(0, tk.END)
                    table.totalAmount.insert(1, str(totalMoney))
                    
                    table.winnerName.delete(0, tk.END)
                    table.winnerName.insert(1, winner)

#adds cards to dealer deck until 17
def stayFunc():
    global gameState, totalMoney, moneyWon
    if gameState == "playing":
        gameState = "end"
        dealerHand()
        dScore()
        dealerSc = totalScore(d.hand)
        
        while dealerSc < 17:
            dealerHand()
            d.hand.append(h.dealCard())
            dealerHand()
            dealerSc = totalScore(d.hand)
            dScore()
            
        winner = isWinner()
        playerBet = table.betAmount.get()
        if winner == "Player":
          totalMoney += int(playerBet)
          moneyWon += int(playerBet)
        elif winner == "Dealer":
          totalMoney -= int(playerBet)
          moneyWon -= int(playerBet)
        else:
          totalMoney = int(totalMoney)
          moneyWon = int(moneyWon)
        table.totalAmount.delete(0, tk.END)
        table.totalAmount.insert(1, str(totalMoney))
        table.winnerName.delete(0, tk.END)
        table.winnerName.insert(1, winner)


# checks score and compares. Winner is chosen.
def isWinner():
    winner = ""   
    if totalScore(p.hand) == 21 and totalScore(d.hand) != 21:
      winner = "Player"

    elif totalScore(p.hand) > totalScore(d.hand) and totalScore(
        p.hand) < 21:
      winner = "Player"
    
    elif totalScore(d.hand) > totalScore(p.hand) and totalScore(d.hand) > 21:
      winner = "Player"
  
    elif totalScore(d.hand) == 21 and totalScore(p.hand) != 21:
      winner = "Dealer"

    elif totalScore(p.hand) > totalScore(d.hand) and totalScore(p.hand) > 21:
      winner = "Dealer"

    elif totalScore(d.hand) > totalScore(p.hand) and totalScore(d.hand) < 21:
      winner = "Dealer"
        
    else:
      winner = "Tie"
      
    return winner

# clears deck for next round
def clearDeck(self):
  global gameState
  global p, d, h, table

  gameState = "start"
  
  p = player("Player", 500,0)
  d = player("Dealer", 10000,0)
  h = House("House")

  table.winnerName.delete(0, tk.END)
  self.winnerName.insert(0, "Winner")

  table.dealerScore.delete(0, tk.END)
  table.playerScore.delete(0, tk.END)

  self.dealerScore.insert(0, "Score")
  self.playerScore.insert(0, "Score")
  

  # green background replaces previous cards
  for i in range(12):
      tk.Label(self.root, background='green4',
               image=self.y[0].b).grid(row=1, column=i)
      tk.Label(self.root, background='green4',
               image=self.y[0].b).grid(row=3, column=i)

root = tk.Tk()
# load = LoadDeck()
p = player("Player", 500, 0)
d = player("Dealer", 10000,0)
h = House("House")
table = background(root)