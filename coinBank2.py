#import custom module coinCreation and its two classes
from coinCreation2 import Coin
#tkinter for GUI
from tkinter import *
#random numbers are used throughout the program
import random
#winsound is used to play sounds (only works in Windows)
import winsound

#global variables
#list of coins in use
coinList = []
#score the user has
score = 0
#price used in the question
price = 0

class CoinBank():
    """ creates the coin bank. This controls the whole programme, including the coins and the questions """
    def __init__(self, gameCanvas, objectList, option):
        #change used in game 2 only
        self.change = 0
        self.gameCanvas = gameCanvas
        #increase used in game 3 only
        self.increase = 0
        self.objectList = objectList
        #the position of the object in the the objectList
        self.objectNo = None
        #the number of the game they are playing
        self.option = option

        #creates an instance of CheckAnswer and QuestionGenerator
        self.checkAnswer = CheckAnswer()
        self.questionGenerator = QuestionGenerator()

        #resets the variables to ensure the program is not storing any previous data values then creates the coins
        self.resetVariables()

    def movedCoin(self, event, i, listPosition):
        """ when a coin is moved the answer is checked and a new coin is created """
        global coinList, price, score

        #get a new value for total, change, increase and objectNo
        self.checkAnswer.setTotal(self.gameCanvas)
        total = self.checkAnswer.getTotal()
        print(total)
        self.change, self.increase, self.objectNo = self.questionGenerator.getQuestion()

        #displays current total
        self.gameCanvas.delete("textTotal")
        self.gameCanvas.create_text(450, 620, text = total, tag = "textTotal", font = ("Times", 14), fill = "blue")

        #checks the total against the expected answer
        if total != 0:
            print("Price:", price)
            print("Change expected:", self.change)
            print("Wanted Value:", price + self.increase)
            if (self.option == 1 and total == price) or (self.option == 2 and total == self.change) or (self.option == 3 and total == price + self.increase):
                #if correct - adds one to score and resets the game
                #calls character status function
                changeCharacterStatus(self.gameCanvas, "correct")
                #increments and displays current score
                self.gameCanvas.delete("textScore")
                score += 1
                self.gameCanvas.create_text(450, 640, text = score, tag = "textScore", font = ("Times", 14), fill = "blue")

                #resets variables
                self.resetVariables()

            elif(self.option == 1 and total < price) or (self.option == 2 and total < self.change) or (self.option == 3 and total < price + self.increase):
                #changes status based on how far away from the answer they are
                if (self.option == 1 and price - total < 10) or (self.option == 2 and self.change - total < 10) or (self.option == 3 and price + self.increase - total < 20):
                    changeCharacterStatus(self.gameCanvas, "nearly there")
                else:
                    changeCharacterStatus(self.gameCanvas, "keep going")
            else:
                changeCharacterStatus(self.gameCanvas, "too high")

        #coin details
        defaultCoinList = [[1,65,240], [2,140,262], [5,65,300], [10,230,262], [20,65,360],
                               [50,140,355], [100,230,355]]
        amount = defaultCoinList[listPosition][0]
        #creates unique coin tag
        tag = str(amount) + "coin" + str(i)

        #checks coin does not already exist
        if tag not in coinList:
            #creates coin
            coinList.append(tag)
            x = defaultCoinList[listPosition][1]
            y = defaultCoinList[listPosition][2]
            Coin(self.gameCanvas, listPosition, tag, x, y)

            #sets up mouse binding which will re-call this function if the coin is moved
            self.gameCanvas.tag_bind(tag, "<ButtonRelease-1>", lambda event: self.movedCoin(event, i+1, listPosition))

    def resetVariables(self):   
        """ resets variables so the player can get another question """
        global coinList
        #remove coins
        for coin in coinList:
            print(type(coin))
            self.gameCanvas.delete(coin)
        coinList = []

        #delete question and rebind the mouse key
        self.gameCanvas.delete("textQuestion")
        binding = self.gameCanvas.bind("<Button-1>", lambda event: self.questionGenerator.setQuestion(event, self.objectList, binding, self.option, self.gameCanvas))
        print(type(binding))

        self.gameCanvas.create_text(450, 300, text = "Click an object!", tag = "textHelp", font = ("Times", 14), fill = "blue")
        
        #creates the first batch of coins in the coin bank
        for i in range(0,7):
            #None corresponds to the mouse event
            #0 to it being the first instance of the coin
            #i is a list position
            self.movedCoin(None, 0, i)
            

class CheckAnswer():
    """ checks the value of the coins in the designated area """
    def setTotal(self, gameCanvas):
        """ calculates the total value of the coins in the answer box """
        global coinList

        self.total = 0
        #calculates total
        #for i in range(0, len(coinList)):
        for coin in coinList:
            #gets coin's coordinates and work out the centre
            coinCoords = gameCanvas.bbox(coin)
            coinCentreX = int((coinCoords[0] + coinCoords[2])/2)
            coinCentreY = int((coinCoords[1] + coinCoords[3])/2)
            #checks if it is in the answer box
            if coinCentreX in range(300, 600):
                if coinCentreY in range(375, 600):
                    #get coin value and add to total
                    currentValue = int(self.obtainAmount(coin))
                    self.total += currentValue

    def getTotal(self):
        return self.total

    def obtainAmount(self, coinTag):
        """ obtains the value of the selected coin """
        amount = ""
        #takes the first 3 characters of the tag to work out the value of the coin
        valueEnded = False
        i = 0
        while valueEnded == False and i < 3:
            if coinTag[i] != "c":
                amount += coinTag[i]
                i += 1
            else:
                valueEnded = True
        return amount
        
        
class QuestionGenerator():
    """ checks if an object is selected, and if it has it creates a question based off of it """
    def __init__(self):
        self.question = None
        self.change = 0
        self.increase = 0
        self.objectNo = None
    def setQuestion(self, event, objectList, binding, option, gameCanvas):
        global price

        #resets increase variable - this is the only one that needs manual resetting due to
        #the complex generation of the increase value
        self.increase = 0
        
        #compares the mouse coordinates with the coordinates of each object image
        objectSelected = False
        i = 0
        while objectSelected == False and i < len(objectList):
            #gets the object's coordinates
            objectCoords = gameCanvas.bbox(objectList[i][0])
            print(type(objectCoords))
            #checks if the mouse is in this area
            if event.x in range(objectCoords[0], objectCoords[2]):
                if event.y in range(objectCoords[1], objectCoords[3]):
                    #if x and y are in range, the object is used to generate the question
                    #gets price from corresponding price list position
                    price = objectList[i][1]

                    #unbinds the mouse to stop the user selecting another object
                    gameCanvas.unbind("<Button-1>", binding)

                    #converts price into a string
                    if price > 99:
                        strPrice = "£1." + str(price)[1:3]
                    else:
                        strPrice = str(price) + "p"

                    #generates question
                    self.question = "The " + objectList[i][0] + " costs " + strPrice + ".\n" 
                    if option == 1:
                        #question one just uses the price
                        self.question += "Pay the exact amount needed."
                    elif option == 2:
                        #question two uses the change the price gives from £2.00
                        self.change = 200 - price
                        print("200 - ", price)
                        print(self.change)
                        self.question += "You pay £2.\n How much change will you get?"
                    else:
                        #question three uses a price increase or decrease
                        #generate an increase value not equal to zero
                        #(-1*price)+10 ensures a decrease does not become zero or less
                        #the rest of the calculations ensure the number is appropriate to the ability level of the students
                        while self.increase == 0:
                            if price > 100:
                                self.increase = random.randint(-100, 100)
                            else:
                                self.increase = random.randint((-1*price)+10, 100)
                        if not(self.increase <= 20 and self.increase >= -20) and self.increase % 5 != 0:
                            modulus = self.increase % 10
                            if modulus <= 2:
                                if self.increase > 0:
                                    self.increase = int(str(self.increase)[0:-1] + "0")
                                else:
                                    self.increase = int(str(self.increase-10)[0:-1] + "0")
                            elif modulus >=8:
                                if self.increase > 0:
                                    self.increase = int(str(self.increase+10)[0:-1] + "0")
                                else:
                                    self.increase = int(str(self.increase-10)[0:-1] + "0")

                            else:
                                self.increase = int(str(self.increase)[0:-1] + "5")
                

                        #converts increase into a string
                        #removes any negative signs (modulus)
                        increaseMod = self.increase
                        if self.increase < 0:
                            increaseMod = int(str(self.increase)[1:3])
                        #converts to pound and pence
                        if self.increase == 100 or self.increase == -100 :
                            strIncrease = "£1.00"
                        else:
                            strIncrease = str(increaseMod) + "p"

                        #adds to question
                        if self.increase < 0:
                            self.question += "The shop decreases the price by " + strIncrease + ".\n Work out the new price."
                        else:
                            self.question += "The shop increases the price by " + strIncrease + ".\n Work out the new price."

                    #displays on screen
                    gameCanvas.delete("textHelp")
                    gameCanvas.create_text(500, 300, text = self.question, tag = "textQuestion", font = ("Times", 14), fill = "blue")
                    #plays "ready" sound
                    winsound.PlaySound("Sounds/Character/Ready.wav", winsound.SND_FILENAME)
                    changeCharacterStatus(gameCanvas, "start")
                    
                    #exit loop     
                    self.objectNo = i
                    objectSelected = True
            i += 1
            
    def getQuestion(self):
        return self.change, self.increase, self.objectNo

            
class GetScore():
    """ returns the score to the main program at the end of the game """
    def getScore(self):
        global score
        return score
    def resetScore(self):
        global score
        score = 0
        
def changeCharacterStatus(gameCanvas, status):
    """ changes the character image and text """
    gameCanvas.delete("characterImage")
    gameCanvas.delete("characterText")
    if status == "correct":
        characterPhoto = PhotoImage(file = "images/characters/characterPositive.gif")
        characterStatusList = [["Good Work!", "sounds/wellDone.wav"], ["Nice One!", "sounds/wellDone.wav"],
                               ["Ready For Another One?", "sounds/correct.wav"], ["Correct - Well Done!", "sounds/correct.wav"]]
    elif status == "too high":
        characterPhoto = PhotoImage(file = "images/characters/characterNegative.gif")
        characterStatusList = [["Too High!", "sounds/tooHigh.wav"], ["Keep Trying!", None],
                             ["Try Using The \n Number Line!", "sounds/numberLine.wav"], ["Too Large!", None]]        
    else:
        characterPhoto = PhotoImage(file = "images/characters/characterNeutral.gif")
        if status == "nearly there":
            characterStatusList = [["Nearly There!", "sounds/nearlyDone.wav"], ["You've Nearly Done It!", None],
                                   ["You Can Do This!", None]]
        elif status == "keep going":
            characterStatusList = [["You Can Do It!", None], ["Remember To Use The \n Number Line!", "sounds/numberLine.wav"],
                                   ["Keep Going!", "sounds/keepGoing.wav"]]
        else:
            characterStatusList = [["On Your Marks! \n Get Set! Go!", None], ["Ready For A Hard One?", None], ["How About This One?", None]]
            
    characterStatusNumber = random.randint(0,len(characterStatusList)-1)        
 
    gameCanvas.characterPhoto = characterPhoto
    gameCanvas.create_image(145, 550, image = characterPhoto, tag = "characterImage")
    gameCanvas.create_text(210, 480, text = characterStatusList[characterStatusNumber][0], tag = "characterText")
    if characterStatusList[characterStatusNumber][1] != None:
        winsound.PlaySound(characterStatusList[characterStatusNumber][1],winsound.SND_FILENAME)

            
 
