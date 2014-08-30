from Tkinter import *
from PIL import ImageTk, Image
import random
import copy
import time
import os
import math


#code prints out a lot of stuff to aid decoding and
#understand whats happening
from Country import *
from Player import *
class Risk(object):
    
    #Controller Funcitons 
    
    def mousePressed(self,event):
        #magic nos
        if(self.gameOver == True):
            return
        self.startScreen = False
        self.redrawAll() 
        if(self.gotNosPlayers == True
            and self.gotNosArtificialPlayers == True):
            self.selection = None 
            if(event.x>=200 and event.x<=1400):
                self.findCountrySelected(event.x,event.y)
            self.redrawAll()

    def keyPressed(self,event):
        if(event.keysym == 'p'):
            self.placeAI()
            self.redrawAll()
        elif(event.keysym == 'a'):
            self.attackAI()
            self.redrawAll()
        elif(event.keysym == 'f'):
            self.fortifyAI()
            self.redrawAll()
        elif(event.keysym == 'h'):
            self.help()
        elif(event.keysym == 'r'):
            self.init(self.nosOfPlayers,self.nosOfArtificialPlayers)

    def timerFired(self):
        self.redrawAll()
        self.timerFiredDelay = 250 #miliseconds
        self.canvas.after(self.timerFiredDelay, self.timerFired)

    def buttonPressedPlace(self):
        if(self.gameOver == True):
            return 
        self.bPressedCards = False
        self.bPressedAttack = False
        self.bPressedFortify = False         
        self.bPressedEndTurn = False
        if(self.bPressedPlace == True):
            self.bPressedPlace = False
        else:
            self.bPressedPlace = True
            self.message = "Click on Country to Place Armies There"
        self.redrawAll()
        


    def buttonPressedCards(self):
        if(self.gameOver == True):
            return 
        self.bPressedPlace = False
        self.bPressedAttack = False
        self.bPressedFortify = False         
        self.bPressedEndTurn = False
        self.bPressedCards = True
        self.message = "Click on Turn In to Turn In Cards"
        self.redrawAll()

    def buttonPressedCardsExit(self):
        if(self.gameOver == True):
            return 
        self.bPressedCards = False
        self.redrawAll()
        return

    def buttonPressedCardsTurnIn(self):
        if(self.gameOver == True):
            return 
        if(self.turnIn() == False):
            self.message =  "Illegal Combination of Cards"
        self.bPressedCards = True
        self.redrawAll()
        return

    def buttonPressedAttackCountry(self):
        if(self.gameOver == True):
            return 
        if(self.board[self.fromCountry].player != self.currentPlayer
           or self.board[self.toCountry].player == self.currentPlayer):
            self.message = "Select Another Country"
            return
        if(self.toCountry not in self.board[self.fromCountry].neighbours):
            self.message =  "Not a neighbour! Choose another country"
        elif(self.board[self.fromCountry].nosArmy == 1):
            self.message =  "Need more army to attack"
        else:
            #calling Model Function
            self.attack()
            self.bPressedFortify = True
            self.nosClick = 3
        return 
        
    def buttonPressedAttack(self):
        if(self.firstRound == True):
            return 
        if(self.players[self.currentPlayer-1].nosArmy>0):
            return
        if(self.gameOver == True):
            return 
        self.fromCountry = None
        self.toCountry = None
        self.nosClick = 0
        self.bPressedPlace = False
        self.bPressedCards = False
        self.bPressedFortify = False         
        self.bPressedEndTurn = False
        self.bPressedAttack = True
        self.message = "Select from Country"
        self.nosClick = 0
        self.redrawAll()
        

    def buttonPressedFortify(self):
        if(self.gameOver == True):
            return 
        if(self.firstRound == True):
            return 
        self.nosClick = 0
        self.fromCountry = None
        self.toCountry = None
        self.bPressedPlace = False
        self.bPressedCards = False
        self.bPressedAttack = False         
        self.bPressedEndTurn = False
        if(self.bPressedFortify == True):
            self.bPressedFortify = False
        else:
            self.bPressedFortify = True
        self.fromCountry = None
        self.toCountry = None
        self.redrawAll()
        
    def buttonPressedEndTurn(self):
        if(self.firstRound == True and 
            self.players[self.currentPlayer-1].nosArmy != 0):
            return 
        if(self.gameOver == True):
            return 
        self.fromCountry = None
        self.toCountry = None 
        self.bPressedPlace = False
        self.bPressedCards = False
        self.bPressedAttack = False
        self.bPressedFortify = False         
        self.bPressedEndTurn = True
        temp = copy.deepcopy(self.players[self.currentPlayer-1].cards)
        if(self.conquered == True):
            card = self.randomCard()
            temp.add(card)
            if(card[0] in self.players[self.currentPlayer-1].countries):
                self.players[self.currentPlayer-1].nosArmy+=1
                self.board[card[0]].nosArmy+=1
        self.players[self.currentPlayer-1].cards = temp
        if(len(self.players[self.currentPlayer-1].cards)>5):
            void = self.turnIn()
        self.nextPlayer()
        self.bPressedEndTurn = False
        if(self.firstRound == False):
            self.startNextTurn() 
        self.turnCount+=1
        if(self.firstRound == True and 
            self.turnCount == self.nosOfPlayers):
            self.firstRound = False
        print self.turnCount
        if(self.players[self.currentPlayer-1].nosArmy == 0):
            self.message = "No More Armies Left. Click on Another Button"
        else:
            self.message = "Click Place to Place Armies on the Board"
        self.redrawAll()
        #implementing AI Player
        if(self.players[self.currentPlayer-1].typeOfPlayer == 1):
            #function which plays AI's Turn
            self.message = ""
            self.playAI()
            # to get armies etc and setting up next turn in
        return 
    
    #from Controller to Model
    def findCountrySelected(self,x,y):
        self.selection = None
        for country in self.board:
            radius = 15
            cx,cy = self.board[country].position
            left = cx - radius
            top = cy - radius
            right = cx  + radius
            bottom = cy + radius
            if(x>=left and y>=top and x<=right and y<=bottom):
                self.selection = country
                if(self.bPressedPlace == True):
                    #placing Armies
                    self.place(country)
                elif(self.bPressedFortify == True):
                    if(country in 
                            self.players[self.currentPlayer-1].countries):
                        self.nosClick+=1
                        if(self.nosClick == 1):
                            self.fromCountry = country
                            self.message = "Select to Country"
                        elif(self.nosClick == 2):
                            self.toCountry = country
                        elif(self.toCountry == country):
                            if(self.fromCountry != None and
                               self.toCountry != None and 
                                self.board[self.fromCountry].nosArmy>1
                               and self.isConnected(self.fromCountry,
                                                    self.toCountry,set())):
                                self.message = "Click on to country to fortify"
                                self.board[self.fromCountry].nosArmy-=1
                                self.board[self.toCountry].nosArmy+=1
                            elif(self.board[self.fromCountry].nosArmy<=1):
                                self.message = "Can't Fortify for lack of Armies"
                elif(self.bPressedAttack == True):
                    if(country in 
                            self.players[self.currentPlayer-1].countries):
                        if(self.nosClick == 0):
                            self.fromCountry = country
                            self.message = "Select to Country"
                            self.nosClick+=1
                    else:
                        if(self.nosClick == 1):
                            self.toCountry = country
                            self.message = "Click on Attack Country to Attack"
                            self.nosClick = 0
                return 
            else:
                self.selection = None 
        return

    #View Fucntions 
        
    def redrawAll(self):
        #MAGIC NUMBERS
        self.canvas.delete(ALL)
        if(self.startScreen == True):
            self.canvas.create_rectangle(0,0,self.canvasWidth,
                                         self.canvasHeight, fill = "Red")
            self.canvas.create_text(self.canvasWidth/2,self.canvasHeight/2,
                text = "Risk", font = "Arial 400 bold")
            self.canvas.create_text(self.canvasWidth/2,self.canvasHeight-200,
                text = "Click anywhere on screen to continue",
                font = "Times 28")
        elif(self.gotNosPlayers == False):
            self.canvas.create_rectangle(0,0,self.canvasWidth,
                                         self.canvasHeight, fill = "Red")
            self.canvas.create_text(250,50,
                                    text = "Enter number of players:",
                                    font = "Times 18")
            self.canvas.create_window(200, 100, window = self.b3)
            self.canvas.create_window(300, 100, window = self.b4)
            self.canvas.create_window(400, 100, window = self.b5)
            self.canvas.create_window(500, 100, window = self.b6)
        elif(self.gotNosArtificialPlayers == False):
            self.canvas.create_rectangle(0,0,self.canvasWidth,
                                         self.canvasHeight, fill = "Red")
            self.canvas.create_text(250,50,
                                    text = "Enter number of Artificial players:",
                                    font = "Times 18")
            self.canvas.create_window(200, 100, window = self.b0AI)
            self.canvas.create_window(300, 100, window = self.b1AI)
            self.canvas.create_window(400, 100, window = self.b2AI)
            self.canvas.create_window(500, 100, window = self.b3AI)
            if(self.nosOfPlayers>=4):
                self.canvas.create_window(600, 100, window = self.b4AI)
            if(self.nosOfPlayers>=5):
                self.canvas.create_window(700, 100, window = self.b5AI)
            if(self.nosOfPlayers==6):
                self.canvas.create_window(800, 100, window = self.b6AI)
        else:
            self.drawGame()
            self.drawCountry()
            self.drawSidebar()
            self.canvas.create_text(1300,20,text = "Press h for help",
                font = "Times 24 bold", fill = "White")
        if(self.gameOver == True):
            text = "Player %d wins!!" % self.currentPlayer
            self.canvas.create_text(800,400, text = text, 
                font = "Times 30", fill = "Yellow")


    def drawHelp(self):
        self.canvas.create_oval(400,200,1200,600,fill = "Cyan",
                                     outline = "Black")
        self.canvas.create_text(800,250,text = "Instructions",
         font = "Times 30 bold",fill = "Black")
        self.canvas.create_text(800,280,text = "Click on Place to Place Armies",
         font = "Times 18 bold",fill = "Black")
        self.canvas.create_text(800,310,text = "Click on Cards to see your Cards",
         font = "Times 18 bold",fill = "Black")
        self.canvas.create_text(800,340,text = "Click on Attack to Attack Country",
         font = "Times 18 bold",fill = "Black")
        self.canvas.create_text(800,370,text = "Click again on Attack to Attack new Country",
         font = "Times 18 bold",fill = "Black")
        self.canvas.create_text(800,400,text = "Click on Fortify to Fortify",
         font = "Times 18 bold",fill = "Black")
        self.canvas.create_text(800,430,text = "Click on to country to send army",
         font = "Times 18 bold",fill = "Black")
        self.canvas.create_text(800,460,text = "Click again on Fortify to Fortify new Country",
         font = "Times 18 bold",fill = "Black")
        self.canvas.create_text(800,490,text = "Click on End Turn to End turn",
         font = "Times 18 bold",fill = "Black")
        self.canvas.create_text(800,520,text = "Click on any other Button to deselect",
         font = "Times 18 bold",fill = "Black")
        self.canvas.create_text(800,550,text = "Click on r to restart",
         font = "Times 18 bold",fill = "Black")
        self.canvas.create_text(800,575,text = "Click anywhere on the screen to exit",
         font = "Times 18 bold",fill = "Black")
        #self.canvas.create_window(800, 500, window = self.helpB)
            
    def drawDice(self):
        #MAGIC NUMBERS
        self.canvas.create_rectangle(400,200,1200,600,fill = "Black",
                                     outline = "Red")
        start = 450
        increment = 150
        for i in xrange(self.diceRed):
            self.canvas.create_rectangle(start, 250, start+100,350,fill = "Red")
            text = "%d" % self.diceRedList[i]
            self.canvas.create_text(start+50,300, text = text, font = "Times 18")
            start+=increment
        start = 450
        increment = 150
        for i in xrange(self.diceWhite):
            self.canvas.create_rectangle(start, 450, start+100,550,fill = "Red")
            text = "%d" % self.diceWhiteList[i]
            self.canvas.create_text(start+50,500, text = text, font = "Times 18")
            start+=increment

    def drawCountry(self):
        for country in self.board:
            radius = 15
            cx,cy = self.board[country].position
            left = cx - radius
            top = cy - radius
            right = cx  + radius
            bottom = cy + radius
            text = "%d" % self.board[country].nosArmy
            color = self.players[self.board[country].player-1].color
            self.canvas.create_oval(left,top,right,bottom,fill = color)
            self.canvas.create_text(cx,cy, text = text, fill = "Black",
                                    font = "Times 18")

    def drawSidebar(self):
        #magic numbers
        self.canvas.create_rectangle(0,0,200,800, fill = "Red")
        turn = "Player %d's turn" %self.currentPlayer
        self.canvas.create_text(100,50, text = turn,
                                font = "Times 20 bold")
        self.canvas.create_text(100,80, anchor = N, text = "Army:",
                                font = "Times 18 bold")
        cx,cy = 100,150
        radius = 15
        left = cx - radius
        top = cy - radius
        right = cx  + radius
        bottom = cy + radius
        color = self.players[self.currentPlayer-1].color
        nosArmy = "%d" % self.players[self.currentPlayer-1].nosArmy
        self.canvas.create_rectangle(50,100,150,200, fill = "Black")
        self.canvas.create_oval(left,top,right,bottom,fill = color)
        self.canvas.create_text(cx,cy, text = nosArmy, fill = "Black",
                                    font = "Times 18")
        #self.canvas.create_window(window = self.enterArmy, x = 50, y = 200)
        if(self.selection == None):
            selected = "Nothing selected"
        else:
            selected = "%s" % self.selection
        self.canvas.create_text(100,700, anchor = N, text = "Selected:",
                                font = "Times 18 bold")
        self.canvas.create_text(100,720, anchor = N, text = selected,
                                font = "Times 18 bold")
        if(self.bPressedEndTurn == True):
            pass
        elif(self.bPressedCards == True):
            self.drawCards()
        if(self.bPressedPlace == True):
            self.canvas.create_text(100,300,text = "ON",
                                    font = "Times 18 bold")
        if(self.bPressedFortify == True):
            self.drawFortify()
        if(self.bPressedAttack == True):
            self.drawAttack()
        self.canvas.create_window(100, 250, window = self.bPlace)
        self.canvas.create_window(100, 350, window = self.bCards)
        self.canvas.create_window(100, 450, window = self.bAttack)
        self.canvas.create_window(100, 550, window = self.bFortify)
        self.canvas.create_window(100, 650, window = self.bEndTurn)

    def drawAttack(self):
        self.canvas.create_text(250,600,
                                text = "From:", fill = "White",
                                font = "Times 18 bold")
        self.canvas.create_text(250,700,
                                text = "To:", fill = "White",
                                font = "Times 18 bold")
        if(self.fromCountry != None):
            self.canvas.create_text(300,650,
                                text = "%s"%self.fromCountry, fill = "White",
                                font = "Times 18 bold")
        if(self.toCountry != None):
            self.canvas.create_text(300,750,
                                text = "%s"%self.toCountry, fill = "White",
                                font = "Times 18 bold")
        if(self.fromCountry != None and self.toCountry != None):
            self.canvas.create_window(300, 550, window = self.bAttackCountry)


    def drawFortify(self):
        self.canvas.create_text(250,600,
                                text = "From:", fill = "White",
                                font = "Times 18 bold")
        self.canvas.create_text(250,700,
                                text = "To:", fill = "White",
                                font = "Times 18 bold")
        if(self.fromCountry != None):
            self.canvas.create_text(300,650,
                                text = "%s"%self.fromCountry, fill = "White",
                                font = "Times 18 bold")
        if(self.toCountry != None):
            self.canvas.create_text(300,750,
                                text = "%s"%self.toCountry, fill = "White",
                                font = "Times 18 bold")


    def drawCards(self):
        #MAGIC NUMBERS
        self.canvas.create_rectangle(400,200,1200,600,fill = "White",
                                     outline = "Red")
        if(len(self.players[self.currentPlayer-1].cards) == 0):
            increment = 0
            self.canvas.create_text(800,400, text = "No Cards",
                                    font = "Times 30")
        else:
            increment = 800/len(self.players[self.currentPlayer-1].cards)
            start = 400-increment
            for card in self.players[self.currentPlayer-1].cards:
                country = card[0]
                armyType = card[1]
                start+=increment
                self.canvas.create_rectangle(start,250,start+100,
                    450, fill = "Red")
                if(country != None):
                    name = country.split()
                    nos = 300
                    for i in xrange(len(name)):
                        self.canvas.create_text(start+50,nos,
                                            text = name[i],
                                        font = "Times 18 bold")
                        nos+=20
                self.canvas.create_text(start+50,400,
                                        text = armyType,
                                    font = "Times 18 bold")
                text = "No of Armies you can get: %d" % (
                    self.cardReturnValuesList[self.cardReturnValue])
                self.canvas.create_text(800,550,
                                        text = text, font = "Times 18 bold")
        if(self.bPressedCards == True):
            self.canvas.create_window(1150, 50, window = self.bCardsExit)
            self.canvas.create_window(800, 500,
                                      window = self.bCardsTurnIn)
                

    def drawGame(self):
        #drawing image as background
        #magic number
        self.canvas.create_image(200,0, anchor = NW, image = self.im)
        if(self.message !=  ""):
            self.canvas.create_text(800, 770, 
                text = self.message, font = "Times 18 bold", fill = "White")

    #AI Functions

    def playAI(self):
        if(self.gameOver == True):
            self.redrawAll()
            return 
        #turns in cards as soon as it has them 
        if(self.turnIn()):
            print "Turned in cards"
        #places based on most nos of enemy neighbours 
        self.placeAI()
        #trying to show screen before moving on ahead
        self.redrawAll()
        self.canvas.update()
        time.sleep(3)
        #attacks as much as possible 
        #without care for defense 
        if(self.firstRound == False):
            self.attackAI()
            self.redrawAll()
            #based on same theory as placement 
            self.fortifyAI()
            self.canvas.update()
            time.sleep(3)
            #ends turn and gets a card 
        self.endTurnAI()
        self.redrawAll()
        """
        print 'Ends Turn'
        self.buttonPressedEndTurn()

        """

    def placeAI(self):
        if(self.gameOver == True):
            self.redrawAll()
            return 
        #diving placement of armies proportionately by counting 
        #no of Enemy neighbours each country that a player owns has 
        #and placing 
        #changed to counting NBSR instead of nos of Enemy neighbours
        self.message = "Placing Armies"
        if(self.players[self.currentPlayer-1].nosArmy == 0):
            return 
        print "Placing: "
        print "Total Armies: %d" % (
            self.players[self.currentPlayer-1].nosArmy)
        listOfCountries = []
        listOfNBSRs = []
        for country in self.players[self.currentPlayer-1].countries:
            listOfCountries+=[country]
            print country
            listOfNBSRs+=[(
                self.calculateNBSR(self.currentPlayer,country))]
        nosArmy = self.players[self.currentPlayer-1].nosArmy
        army = 0
        for i in xrange(len(listOfCountries)):
            if(self.players[self.currentPlayer-1].nosArmy>0):
                army = int(listOfNBSRs[i]*nosArmy)
                self.board[listOfCountries[i]].nosArmy+=army
                self.players[self.currentPlayer-1].nosArmy-=army
        #placing the remaining army in the country with the the highest NBSR
        index = listOfNBSRs.index(max(listOfNBSRs))
        self.board[listOfCountries[index]].nosArmy+=(
            self.players[self.currentPlayer-1].nosArmy)
        self.players[self.currentPlayer-1].nosArmy = 0
        for i in xrange(len(listOfCountries)):
            print "%s : %d" %(listOfCountries[i],
             self.board[listOfCountries[i]].nosArmy)
        return 

    def findNosOfEnemyNeighbours(self, country, player):
        #counting using a counter 
        ctr = 0
        for neighbour in self.board[country].neighbours:
            if(self.board[neighbour].player != player):
                ctr+=1
        return ctr

    def attackAI(self):
        if(self.gameOver == True):
            self.redrawAll()
            return 
        #select from countries of current player 
        #select one which has more than 1 nosArmy
        #a from country : self.fromCountry = country
        #from from country's neighbours an ENEMY neighbour
        #a to country: self.toCountry = country
        countries = copy.deepcopy(
            self.players[self.currentPlayer-1].countries)
        for country in countries:
                for neighbour in self.board[country].neighbours:
                    if(self.board[country].nosArmy>1):
                        self.fromCountry = country
                        if(self.board[neighbour].player != self.currentPlayer):
                            self.toCountry = neighbour
                            if(self.attackMakesSense()):
                                self.message = "Attacking From %s To %s" %(
                                    self.fromCountry,self.toCountry)
                                print "Attacking",
                                print "From: %s" % self.fromCountry,
                                print "To: %s" % self.toCountry,
                                print "%d \t %d" %(
                                    self.board[self.fromCountry].nosArmy,
                                    self.board[self.toCountry].nosArmy)
                                self.attack()
                            
        return 

    def attackMakesSense(self):
        if(self.board[self.fromCountry].nosArmy >
            self.board[self.toCountry].nosArmy):
            #implementing different ones for each 
            prevScore = self.evaluateBoard()
            temp = copy.deepcopy(self.players[self.currentPlayer-1].countries)
            temp.add(self.toCountry)
            self.players[self.currentPlayer-1].countries = temp
            newScore = self.evaluateBoard()
            self.players[self.currentPlayer-1].countries.remove(self.toCountry)
            flag = False
            if(newScore>=prevScore):
                flag = True
            if((self.calculateBSR(self.currentPlayer,self.toCountry)<=
                self.calculateBSR(self.currentPlayer, self.fromCountry)) or
                    flag == True):
                return True
        return False


    #idea of these calculate functions are derived from 
    #Evaluating Heuristics in the Game Risk An Aritifical Intelligence Perspective
    #by Franz Hahn
    #paper found online and suggested to me by Zach Piscelli 

    def calculateBST(self,player,country):
        value = 0
        for neighbour in self.board[country].neighbours:
            if(self.board[neighbour].player!= player):
                value+=self.board[neighbour].nosArmy
        return value

    def calculateBSR(self,player,country):
        value = 0
        numerator = self.calculateBST(player,country)
        value = (numerator*1.0)/self.board[country].nosArmy
        return value

    def calculateNBSR(self,player, country):
        numerator = self.calculateBSR(player,country)
        sum = 0
        for xcountry in self.players[player-1].countries:
            sum+=self.calculateBSR(player,xcountry)
        value = (numerator*1.0)/sum
        print country,
        print value
        return value

    def fortifyAttackAI(self):
        if(self.gameOver == True):
            self.redrawAll()
            return 
        if(self.calculateBSR(self.currentPlayer,self.toCountry)>
            self.calculateBSR(self.currentPlayer, self.fromCountry)):
            if(self.board[self.fromCountry].nosArmy == 1):
                return
            if(self.fromCountry == self.toCountry):
                return 
            print "Placing %d in %s from %s" %(
                (self.board[self.fromCountry].nosArmy-1),
                self.toCountry,
                self.fromCountry)
            self.board[self.toCountry].nosArmy+=(
                self.board[self.fromCountry].nosArmy-1)
            self.board[self.fromCountry].nosArmy = 1
            

    def fortifyAI(self):
        if(self.gameOver == True):
            self.redrawAll()
            return 
        #finding country with most nos of Army after a turn
        #does it only once not very effective 
        #copied parts from placeAI
        highestBSR = 0
        highestCountryBSR = ""
        for country in self.players[self.currentPlayer-1].countries:
            if(self.calculateBSR(self.currentPlayer,country)>highestBSR):
                highestBSR = self.calculateBSR(self.currentPlayer,country)
                highestCountryBSR = country
        if(highestCountryBSR == ""):
            return 
        maxArmy = 0
        maxArmyCountry = ""
        for country in self.players[self.currentPlayer-1].countries:
            if(highestCountryBSR != country and self.isConnected(highestCountryBSR,country)):
                if(self.board[country].nosArmy>maxArmy):
                    maxArmy = self.board[country].nosArmy
                    maxArmyCountry = country
        if(maxArmyCountry == ""):
            return 
        self.board[highestCountryBSR].nosArmy+=(maxArmy-1)
        self.board[maxArmyCountry].nosArmy = 1
        print "Placing: "
        print "%d from %s to %s" % (
            (maxArmy-1), maxArmyCountry, highestCountryBSR)
        self.message = "Placing %d form %s to %s" % (
            (maxArmy-1), maxArmyCountry, highestCountryBSR)
        self.redrawAll()
        return 

    def endTurnAI(self):
        if(self.firstRound == True and 
            self.players[self.currentPlayer-1].nosArmy != 0):
            return 
        if(self.gameOver == True):
            self.redrawAll()
            return 
        #copied from buttonPressedVersion
        if(self.gameOver == True):
            return 
        temp = copy.deepcopy(self.players[self.currentPlayer-1].cards)
        if(self.conquered == True):
            card = self.randomCard()
            temp.add(card)
            if(card[0] in self.players[self.currentPlayer-1].countries):
                self.players[self.currentPlayer-1].nosArmy+=1
                self.board[card[0]].nosArmy+=1
        self.players[self.currentPlayer-1].cards = temp
        if(len(self.players[self.currentPlayer-1].cards)>5):
            void = self.turnIn()
        self.nextPlayer()
        if(self.firstRound == False):
            self.startNextTurn() 
        self.turnCount+=1
        if(self.firstRound == True and 
            self.turnCount == self.nosOfPlayers):
            self.firstRound = False
        print self.turnCount
        self.redrawAll()
        self.redrawAll()
        #implementing AI Player
        if(self.players[self.currentPlayer-1].typeOfPlayer == 1):
            #function which plays AI's Turn
            self.playAI()
            # to get armies etc and setting up next turn in
        return 

    def evaluateBoard(self):
        #based upon number of armies you get nextTurn
        #drawBacks no reinforcement
        #make according to country ratings 
        nosArmy = 0
        nosArmy+=int(len(self.players[self.currentPlayer-1].countries)/3)
        nosArmy+=self.armyFromContinent()
        if(nosArmy<3):
            nosArmy = 3
        return nosArmy

        
    #Model Fucntions

    def armyFromContinent(self):
        nosArmy = 0
        nosInContinent = [0,0,0,0,0,0]
        for country in self.players[self.currentPlayer-1].countries:
            for i in xrange(len(self.continents)):
                if(self.board[country].continent == self.continents[i]):
                    nosInContinent[i]+=1
        for i in xrange(len(nosInContinent)):
            if(nosInContinent[i] == self.nosCountriesInContinents[i]):
                nosArmy+=self.nosCountriesInContinents[i]
                print self.continents[i]
        return nosArmy

    def startNextTurn(self):
        self.conquered = False
        if(self.turnCount<self.nosOfPlayers-1):
            return 
        nosArmy = 0
        nosArmy+=int(len(self.players[self.currentPlayer-1].countries)/3)
        nosArmy+=self.armyFromContinent()
        if(nosArmy<3):
            nosArmy = 3
        self.players[self.currentPlayer-1].nosArmy+=nosArmy
        return 

    def checkForWin(self):
        if(len(self.players[self.currentPlayer-1].countries) == 42):
            print "Game Over"
            self.gameOver = True
        self.redrawAll()
        return 

    def playerEliminated(self):
        ctr = 0
        for i in xrange(self.nosOfPlayers):
            if(len(self.players[i].countries) == 0):
                ctr+=1
        eliminatedPlayer = None
        if(ctr>len(self.playerEliminatedList)):
            for i in xrange(self.nosOfPlayers):
                if(len(self.players[i].countries) == 0 and 
                    (i+1) not in self.playerEliminatedList):
                    eliminatedPlayer = i+1
            self.players[self.currentPlayer-1].cards.union(
                self.players[eliminatedPlayer-1].cards)
            self.players[eliminatedPlayer-1].cards = set()
            print "Eliminated Player: %d" % eliminatedPlayer
            self.playerEliminatedList.add(eliminatedPlayer)
        else:
            return 

    def attack(self):
        fromCountry = self.fromCountry
        toCountry = self.toCountry
        if(toCountry == fromCountry):
            assert(False)
            return 
        if(self.board[fromCountry].nosArmy == 2):
            self.diceRed = 1
        elif(self.board[fromCountry].nosArmy == 3):
            self.diceRed = 2
        elif(self.board[fromCountry].nosArmy > 3):
            self.diceRed = 3
        else:
            print "problem in self.diceRed"
            assert(False)
        if(self.board[toCountry].nosArmy == 1):
            self.diceWhite = 1
        elif(self.board[toCountry].nosArmy >= 2):
            self.diceWhite = 2
        else:
            print "problem in self.diceWhite"
            assert(False)
        for i in xrange(self.diceRed):
            self.diceRedList+=[random.randint(1,6)]
        for i in xrange(self.diceWhite):
            self.diceWhiteList+=[random.randint(1,6)]
        self.diceRedList = sorted(self.diceRedList)[::-1]
        self.diceWhiteList = sorted(self.diceWhiteList)[::-1]
        #calling draw function
        if(self.players[self.currentPlayer-1].typeOfPlayer == 0): 
            self.drawDice()
        self.canvas.update()
        time.sleep(2)
        #self.redrawAll()
        nosAttacker = 0
        nosDefender = 0
        if(self.diceRed>=self.diceWhite):
            length = self.diceWhite
        else:
            length = self.diceRed
        for i in xrange(length):
            print self.diceRedList[i],self.diceWhiteList[i]
            if(self.diceRedList[i]>self.diceWhiteList[i]):
                nosDefender+=1
            else:
                nosAttacker+=1
        self.board[fromCountry].nosArmy-=nosAttacker
        self.board[toCountry].nosArmy-=nosDefender
        if(self.board[toCountry].nosArmy == 0):
            self.conquered = True
            if(self.players[self.currentPlayer-1].typeOfPlayer != 1):
                self.message = "Click on Conquered Country to Send Army There"
            t = self.board[toCountry].player - 1
            self.players[t].countries.discard(toCountry)
            self.board[toCountry].player = self.currentPlayer
            self.players[self.currentPlayer-1].countries.add(toCountry)
            self.board[toCountry].nosArmy+=1
            self.board[fromCountry].nosArmy-=1
            self.checkForWin()
            self.playerEliminated()
            if(self.players[self.currentPlayer-1].typeOfPlayer == 1):
                self.fortifyAttackAI()
                self.attackAI()
        self.diceRed = 3
        self.diceRedList = []
        self.diceWhite = 2
        self.diceWhiteList = []
        self.redrawAll()
        
    ##inspired by Magic Gerbels 
    def isConnected(self,fromCountry,toCountry,alreadyVisited = set()):
        alreadyVisited.add(fromCountry)
        if(toCountry in self.board[fromCountry].neighbours):
            return True
        else:
            for country in self.board[fromCountry].neighbours:
                if((self.board[country].player ==
                   self.board[fromCountry].player)
                   and (country not in alreadyVisited)):
                    if(self.isConnected(country,toCountry)):
                        return True
            return False
                    
    #taken from 15-112 recursion notes :)
    #its really cool code - Really!!
    def powerset(self,a):
        # returns a list of all subsets of the list a
        if (len(a) == 0):
            return [[]]
        else:
            allSubsets = [ ]
            for subset in self.powerset(a[1:]):
                allSubsets += [subset]
                allSubsets += [[a[0]] + subset]
            return allSubsets
        
    # model function convert to rule function 
    def checkTurnIn(self):
        #combinations possible without wildCard
        #do automatically for 5
        #strategically better to keep wild card
        self.cardReturnCombinations = [
            ["Artillery","Cavalry","Infantry"],
            ["Infantry","Infantry","Infantry"],
            ["Cavalry","Cavalry","Cavalry"],
            ["Artillery","Artillery","Artillery"],
            ["Artillery","Artillery","WildCard"],
            ["Cavalry","Cavalry","WildCard"],
            ["Infantry","Infantry","WildCard"],
            ["Artillery","Cavalry","WildCard"],
            ["Artillery","Infantry","WildCard"],
            ["Cavalry","Infantry","WildCard"],
            ]
        if(len(self.players[self.currentPlayer-1].cards)<3):
            print 'less than 3'
            return []
        temp = []
        for card in self.players[self.currentPlayer-1].cards:
            temp+=[card[1]]
        temp = sorted(temp)
        allSubsets = self.powerset(temp)
        for subset in allSubsets:
            if(subset in self.cardReturnCombinations):
                return subset
        return []

    def turnIn(self):
        temp = self.checkTurnIn()
        if(temp == []):
            return False
        if(self.cardReturnValue>5):
            self.players[self.currentPlayer-1].nosArmy+=(
                self.cardReturnValuesList[5]+(
                    (self.cardReturnValue-5)*5))
        else:
            self.players[self.currentPlayer-1].nosArmy+=(
                self.cardReturnValuesList[self.cardReturnValue])
        self.cardReturnValue+=1
        ctr = 0
        cards = []
        for playerCard in self.players[self.currentPlayer-1].cards:
            if(ctr == 3):
                break
            if(playerCard[1] in temp):
                cards+=[playerCard]
                ctr+=1
        for i in xrange(3):
            self.players[self.currentPlayer-1].cards.discard(cards[i])
            self.cards+=[cards[i]]
            self.totalCards+=1
        return True

    def place(self,country):
        if(self.players[self.currentPlayer-1].nosArmy>0):
            if(country in
               self.players[self.currentPlayer-1].countries):
                self.players[self.currentPlayer-1].nosArmy-=1
                self.board[country].nosArmy+=1
        else:
            if(self.firstRound == False):
                self.message = "No More Armies Left. Click on Another Button"
            else:
                self.message = "End Turn"
            
    def randomCard(self):
        randomIndex = random.randint(0,self.totalCards-1)
        self.totalCards-=1
        return self.cards.pop(randomIndex)

    def getPlayerColor(self):
        return self.armyColors[self.currentPlayer-1]

    def nextPlayer(self):
        self.message = "Click Place to Place Armies on the Board"
        self.currentPlayer+=1
        if(self.currentPlayer>self.nosOfPlayers):
            self.currentPlayer = 1
        print "Player Eliminated List",
        print self.playerEliminatedList
        if(self.currentPlayer in self.playerEliminatedList):
            print "Moving 1 player ahead"
            self.nextPlayer()

    def getPlayer(self):
        return self.currentPlayer

    def assignCountries(self):
        newList = copy.deepcopy(self.cards)
        newListNos = 42
        for i in xrange(self.nosOfPlayers):
            temp = []
            for j in xrange(self.nosCards/self.nosOfPlayers):
                randomIndex = random.randint(0,newListNos-1)
                temp.append(newList[randomIndex][0])
                newListNos-=1
                newList.remove(newList[randomIndex])
            self.players[i].countries = set(temp)
        for i in xrange(self.nosCards%self.nosOfPlayers):
            randomIndex = random.randint(0,newListNos-1)
            temp = (newList[randomIndex][0])
            self.players[i].countries.add(temp)
            newListNos-=1
            newList.remove(newList[randomIndex])
        return

    def assignArmies(self):
        nosArmy = 0
        nosOfPlayers = self.nosOfPlayers
        if(nosOfPlayers == 3):
            nosArmy = 35
        elif(nosOfPlayers == 4):
            nosArmy = 30
        elif(nosOfPlayers == 5):
            nosArmy = 25
        elif(nosOfPlayers == 6):
            nosArmy = 20
        else:
            print "No of players are out of bounds"
            assert(False)
        for i in xrange(nosOfPlayers):
            self.players[i].nosArmy = nosArmy
        return

    def placeArmiesOnBoardStart(self):
        for i in xrange(self.nosOfPlayers):
            for country in self.players[i].countries:
                self.board[country].nosArmy+=1
                self.board[country].player = i+1
                self.players[i].nosArmy-=1
        return 


    def openManual(self,file):
        os.startFile(file)


    def help(self):
        self.drawHelp()  
        
    def init(self,nosOfPlayers,nosOfPlayersAI):
        #print nosOfPlayers
        self.nosClick = 0
        self.startScreen = False
        self.gotNosArtificialPlayers = True
        self.gameOver = False
        self.bPressedPlace = False
        self.bPressedCards = False
        self.bPressedAttack = False
        self.bPressedFortify = False         
        self.bPressedEndTurn = False
        self.firstRound = True 
        self.firstRoundTurnCount = 0
        self.turnCount = 0
        self.conquered = False
        self.selection = None
        self.fromCountry = None
        self.toCountry = None 
        self.message = "Click Place to Place Armies on the Board"
        self.cardReturnValue = 0
        self.playerEliminatedList = set()
        self.loadBoard()
        self.generateCards()
        self.nosOfPlayers = nosOfPlayers
        self.nosOfArtificialPlayers = nosOfPlayersAI
        self.players = []
        for i in xrange(nosOfPlayers):
            self.players+=[Player(self.armyColors[i])]
        for i in xrange(nosOfPlayers-nosOfPlayersAI,nosOfPlayers):
            self.players[i].typeOfPlayer = 1
        self.assignCountries()
        self.assignArmies()
        self.placeArmiesOnBoardStart()
        self.currentPlayer = 1
        if(self.players[self.currentPlayer-1].typeOfPlayer == 1):
            self.message = ""
            self.playAI()
        self.redrawAll()


    def getNosArtificialPlayers(self,nosofPlayers):
        self.gotNosPlayers = True
        self.nosOfPlayers = nosofPlayers
        self.b0AI = Button(self.canvas, text = "0", command = lambda:self.init(self.nosOfPlayers,0))
        self.b1AI = Button(self.canvas, text = "1", command = lambda:self.init(self.nosOfPlayers,1))
        self.b2AI = Button(self.canvas, text = "2", command = lambda:self.init(self.nosOfPlayers,2))
        self.b3AI = Button(self.canvas, text = "3", command = lambda:self.init(self.nosOfPlayers,3))
        self.b4AI = Button(self.canvas, text = "4", command = lambda:self.init(self.nosOfPlayers,4))
        self.b5AI = Button(self.canvas, text = "5", command = lambda:self.init(self.nosOfPlayers,5))
        self.b6AI = Button(self.canvas, text = "6", command = lambda:self.init(self.nosOfPlayers,6))
        self.redrawAll()

    def run(self):
        #creating canvas
        root = Tk()
        self.root = root
        self.canvasWidth = 1400
        self.canvasHeight = 800
        self.canvas = Canvas(root,width = self.canvasWidth,
                              height = self.canvasHeight)
        self.canvas.pack()
        #(PIL code derived from
        #http://spider.wadsworth.org/spider_doc/
        #spider/docs/python/spipylib/tkinter.html)
        #getting image and packaging it for Tkinter
        #image procured from google search
        im = Image.open("map.jpg")
        #resizing
        size = (1200,800)
        im = im.resize(size)
        imtk = ImageTk.PhotoImage(im)
        #storing
        self.im = imtk
        self.b3 = Button(self.canvas, text = "3", command = lambda:self.getNosArtificialPlayers(3))
        self.b4 = Button(self.canvas, text = "4", command = lambda:self.getNosArtificialPlayers(4))
        self.b5 = Button(self.canvas, text = "5", command = lambda:self.getNosArtificialPlayers(5))
        self.b6 = Button(self.canvas, text = "6", command = lambda:self.getNosArtificialPlayers(6))
        self.bPlace = Button(self.canvas, text = "Place",
                             command = self.buttonPressedPlace)
        self.bCards = Button(self.canvas, text = "Cards",
                             command = self.buttonPressedCards)
        self.bCardsExit = Button(self.canvas, text = "X",
                                 command = self.buttonPressedCardsExit)
        self.bCardsTurnIn = Button(self.canvas, text = "Turn In",
                                 command = self.buttonPressedCardsTurnIn)
        self.bAttack = Button(self.canvas, text = "Attack",
                        command = self.buttonPressedAttack)
        self.bAttackCountry = Button(self.canvas, text = "Attack Country",
                        command = self.buttonPressedAttackCountry)
        self.bFortify = Button(self.canvas, text = "Fortify",
                        command = self.buttonPressedFortify)
        self.bEndTurn = Button(self.canvas, text = "End Turn",
                        command = self.buttonPressedEndTurn)
        #self.enterArmy = Entry(self.canvas)
        self.redrawAll()
        #calling init to run Game
        #self.init()
        root.bind("<Button-1>", self.mousePressed)
        root.bind("<Key>", self.keyPressed)
        #self.timerFired()
        root.mainloop()

    def __init__(self):
        self.startScreen = True
        self.gotNosPlayers = False
        self.gotNosArtificialPlayers = False
        self.gameOver = False
        self.board = None
        self.diceRed = 3
        self.diceRedList = []
        self.diceWhite = 2
        self.diceWhiteList = []
        self.playerCards = [set(),set(),set(),set(),set(),set()]
        self.armyColors = ["Yellow", "Green", "Blue", "Red", "White", "Orange"]
        self.pieceNames = ["Infantry","Cavalry","Artillery"]
        self.pieceValue = [1,5,10]
        self.cardReturnValuesList = [4,6,8,10,12,15]                                        
        self.nosCards = 42
        self.wildCards = 2
        self.totalCards = 44


    # Model Generating Functions to be called each time

    def generateCards(self):
        #generating cards with country and army piece
        cards = []
        counter = 0
        armyType = 0
        for country in self.board:
            if(counter>(self.nosCards/len(self.pieceValue))):
                counter = 0
                armyType+=1
            element = (country,self.pieceNames[armyType])
            cards+=[(country,self.pieceNames[armyType])]
            counter+=1
        #adding wildCards
        nosOfWildCards = 2
        for i in xrange(nosOfWildCards):
            cards+=[(None,"WildCard")]
        self.cards = cards
        self.armies = [None, None, 35, 30, 25, 20]

    def loadBoard(self):
        #this funciton is going to be insanely long
        #Can Shorten by putting each continent in a separate function
        #But its kind of wasteful to do that

        #list of continents
        self.continents = ["North America", "South America", "Europe", "Africa",
                           "Asia", "Australia"]
        self.nosCountriesInContinents = [9, 4, 7, 6, 12, 4]
        #dictionary with countries and their positions
        d = {}
        
        #North America
        #Positions not entered
        d["Alaska"] = Country((275,150),
                              "North America",
                        set(["Kamchatka","Northwest Territory","Alberta"]),
                              None, 0)
        
        d["Northwest Territory"] = Country((400,150),
                                           "North America",
                        set(["Alaska","Alberta","Ontario","Greenland"]),
                              None, 0)
        
        d["Alberta"] = Country((400,215),
                               "North America",
                     set(["Alaska","Northwest Territory","Ontario",
                          "Western United States"]),
                              None, 0)
        
        d["Greenland"] = Country((675,100),
                                 "North America",
                            set(["Northwest Territory","Ontario","Quebec",
                                 "Iceland"]),
                              None, 0)
        
        d["Ontario"] = Country((475,215),
                               "North America",
                        set(["Northwest Territory","Alberta","Greenland",
                             "Quebec","Eastern United States",
                             "Western United States"]),
                              None, 0)
        
        d["Quebec"] = Country((575,215),
                              "North America",
                        set(["Ontario","Greenland","Eastern United States"]),
                              None, 0)
        
        d["Western United States"] = Country((400,300),
                                             "North America",
                            set(["Alberta","Ontario","Eastern United States",
                                 "Central America"]),
                              None, 0)
        
        d["Eastern United States"] = Country((490,310),
                                             "North America",
                            set(["Central America","Western United States",
                                 "Ontario","Quebec"]),
                              None, 0)
        
        d["Central America"] = Country((425,375),
                                       "North America",
                            set(["Eastern United States",
                                 "Western United States",
                                 "Venezuela"]),
                              None, 0)

        #South America
        #Positions not entered
        d["Venezuela"] = Country((465,465),
                                       "South America",
                            set(["Central America","Peru","Brazil"]),
                                     None, 0)
        d["Peru"] = Country((490,575),
                                       "South America",
                            set(["Brazil", "Venezuela","Argentina"]),
                              None, 0)
        d["Brazil"] = Country((570,550),
                                       "South America",
                            set(["Peru", "Venezuela","Argentina",
                                 "North Africa"]),
                              None, 0)
        d["Argentina"] = Country((490,650),
                                       "South America",
                            set(["Peru","Brazil"]),
                              None, 0)

        #Australia
        #Positions not entered
        d["Indonesia"] = Country((1150,550),
                                       "Australia",
                            set(["Siam","New Guinea",
                                 "Western Australia"]),
                              None, 0)
        d["New Guinea"] = Country((1270,560),
                                       "Australia",
                            set(["Indonesia",
                                "Eastern Australia","Western Australia"]),
                              None, 0)
        d["Eastern Australia"] = Country((1250,675),
                                       "Australia",
                            set(["New Guinea",
                                 "Western Australia"]),
                              None, 0)
        d["Western Australia"] = Country((1150,670),
                                       "Australia",
                            set(["New Guinea","Indonesia",
                                 "Eastern Australia"]),
                              None, 0)

        #Africa
        #Positions not entered
        d["Madagascar"] = Country((890,675),
                                       "Africa",
                            set(["South Africa", "East Africa"]),
                              None, 0)
        d["South Africa"] = Country((800,675),
                                       "Africa",
                            set(["Madagascar", "East Africa",
                                 "Congo"]),
                              None, 0)
        d["Congo"] = Country((795,575),
                                       "Africa",
                            set(["South Africa", "East Africa",
                                 "North Africa"]),
                              None, 0)
        d["East Africa"] = Country((850,525),
                                       "Africa",
                            set(["South Africa", "Madagascar",
                                 "Congo","North Africa","Egypt",
                                 "Middle East"]),
                              None, 0)
        d["Egypt"] = Country((800,425),
                                       "Africa",
                            set(["East Africa","North Africa",
                                 "Middle East", "Southern Europe"]),
                              None, 0)
        d["North Africa"] = Country((725,475),
                                       "Africa",
                            set(["Congo","East Africa","Egypt",
                                 "Brazil", "Western Europe",
                                 "Southern Europe"]),
                              None, 0)

        #Europe
        d["Western Europe"] = Country((705,350),
                                       "Europe",
                            set(["North Africa","Southern Europe",
                                 "Great Britain", "Northern Europe"]),
                              None, 0)
        d["Southern Europe"] = Country((775,325),
                                       "Europe",
                            set(["Middle East","Egypt",
                                 "North Africa","Western Europe",
                                 "Northern Europe","Ukraine"]),
                              None, 0)
        d["Ukraine"] = Country((875,225),
                                       "Europe",
                            set(["Ural", "Afghanistan","Middle East",
                                 "Southern Europe","Northern Europe",
                                 "Scandinavia"]),
                              None, 0)
        d["Northern Europe"] = Country((775,270),
                                       "Europe",
                            set(["Southern Europe","Western Europe",
                                 "Great Britain","Scandinavia",
                                 "Ukraine"]),
                              None, 0)
        d["Great Britain"] = Country((715,250),
                                       "Europe",
                            set(["Iceland","Scandinavia",
                                 "Northern Europe","Western Europe"]),
                              None, 0)
        d["Iceland"] = Country((705,175),
                                       "Europe",
                            set(["Greenland", "Scandinavia","Great Britain"]),
                              None, 0)
        d["Scandinavia"] = Country((775,175),
                                       "Europe",
                            set(["Ukraine","Northern Europe",
                                 "Great Britain","Iceland"]),
                              None, 0)
        #Asia
        #Positions not entered
        d["Ural"] = Country((1000,200),
                                       "Asia",
                            set(["Ukraine","Afghanistan",
                                 "China", "Siberia"]),
                              None, 0)
        d["Afghanistan"] = Country((975,300),
                                       "Asia",
                            set(["Ural","Ukraine","Middle East",
                                 "India", "China"]),
                              None, 0)
        d["Middle East"] = Country((900,385),
                                       "Asia",
                            set(["East Africa", "Egypt", "Southern Europe",
                                 "Ukraine","Afghanistan",
                                 "India"]),
                              None, 0)
        d["India"] = Country((1025,425),
                                       "Asia",
                            set(["Middle East","Afghanistan",
                                 "China", "Siam"]),
                              None, 0)
        d["Siam"] = Country((1110,440),
                                       "Asia",
                            set(["Indonesia","India","China"]),
                              None, 0)
        
        d["China"] = Country((1100,350),
                                       "Asia",
                            set(["Siam","India","Afghanistan",
                                 "Ural","Siberia","Mongolia"]),
                              None, 0)
        d["Mongolia"] = Country((1175,290),
                                       "Asia",
                            set(["China","Siberia","Irkutsk",
                                 "Kamchatka", "Japan"]),
                              None, 0)
        d["Japan"] = Country((1250,325),
                                       "Asia",
                            set(["Mongolia","Kamchatka"]),
                              None, 0)
        d["Kamchatka"] = Country((1300,150),
                                       "Asia",
                            set(["Alaska","Japan","Mongolia",
                                 "Irkutsk", "Yakutsk"]),
                              None, 0)
        d["Yakutsk"] = Country((1190,150),
                                       "Asia",
                            set(["Kamchatka","Irkutsk","Siberia"]),
                              None, 0)
        d["Irkutsk"] = Country((1150,225),
                                       "Asia",
                            set(["Yakutsk","Kamchatka",
                                 "Mongolia","Siberia"]),
                              None, 0)
        d["Siberia"] = Country((1080,200),
                                       "Asia",
                            set(["Yakutsk","Irkutsk",
                                 "Mongolia","China","Ural"]),
                              None, 0)
        self.board = d

#run the game
Risk().run()
