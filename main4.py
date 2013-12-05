#custom module which deals with the main gameplay
from coinBank2 import CoinBank, GetScore
#custom module to generate and use the number line
from numberLine import NumberLine
#tkinter for GUI
from tkinter import *
#askopenfilename for the mergeFile function
from tkinter.filedialog import askopenfilename
#random numbers used throughout the program
import random
#regular expression module used for validation
import re
#time used for saving time and date to the score file
import time
#winsound used to play sound
import winsound

#globals for unlocking games - bonus game is unlocked with game 3
game2Unlocked = False
game3Unlocked = False
#global variable for window size
canvasX = 500
canvasY = 500
#GetScore object used to retrive the score from the CoinBank module
getScore = None

class MenuSetup():
    """ creates the menu and runs it """
    def __init__(self):
        global cavnasX, canvasY, game2Unlocked, game3Unlocked 
        
        menuWindow = Toplevel()

        menuWindow.title("Menu")
        #random background colors
        backgroundList = ["chartreuse", "cyan", "yellow"]
        backgroundNumber = random.randint(0, len(backgroundList)-1)
        menuCanvas = Canvas(menuWindow, width = canvasX, height = canvasY, bg = backgroundList[backgroundNumber])
        menuCanvas.grid()

        #adds logo
        logoPhoto = PhotoImage(file = "images/logo.gif")
        menuCanvas.logoPhoto = logoPhoto
        menuCanvas.create_image(250, 100, image = logoPhoto, tag = "logo")

        #layout variables
        x = 200
        y = 220
        x2 = 450
        y2 = 475
        fontLarge = ("Arial", 20)
        fontSmall = ("Arial", 15)
        
        #creates clickable game titles        
        menuCanvas.create_text(x, y, text = "Game 1: Paying Exact Amounts", fill = "red", font = fontLarge, tag = "gameTitleOne")
        menuCanvas.tag_bind("gameTitleOne", "<ButtonPress-1>", lambda e: GameSetup(menuWindow, 1))

        if game2Unlocked == True:
            #if unlocked, displays a clickable option for game 2
            menuCanvas.create_text(x, y+40, text = "Game 2: Giving Change", fill = "red", font = fontLarge, tag = "gameTitleTwo")
            menuCanvas.tag_bind("gameTitleTwo", "<ButtonPress-1>", lambda e: GameSetup(menuWindow, 2))
        else:
            #a "fake" title and information telling the user how to unlock game 2
            menuCanvas.create_text(x, y+40, text = "Game 2: LOCKED", fill = "red", font = fontLarge, tag = "gameTitleTwo")
            menuCanvas.create_text(x, y+65, text = "Complete Game One to unlock", fill = "red", font = fontSmall, tag = "gameTitleTwo")
        if game3Unlocked == True:
            #if unlocked, displays a clickable option for game 3 and the bonus game
            menuCanvas.create_text(x, y+115, text = "Game 3: Changing the Price", fill = "red", font = fontLarge, tag = "gameTitleThree")
            menuCanvas.tag_bind("gameTitleThree", "<ButtonPress-1>", lambda e: GameSetup(menuWindow, 3))
            menuCanvas.create_text(x, y+190, text = "Bonus Game!", fill = "red", font = fontLarge, tag = "bonusTitle")
            menuCanvas.tag_bind("bonusTitle", "<ButtonPress-1>", lambda e: BonusGameSetup(menuWindow))
        else:
            #a "fake" title and information telling the user how to unlock game 3 and the bonus game
            menuCanvas.create_text(x, y+115, text = "Game 3: LOCKED", fill = "red", font = fontLarge, tag = "gameTitleThree")
            menuCanvas.create_text(x, y+140, text = "Complete Game Two to unlock", fill = "red", font = fontSmall, tag = "gameTitleThree")
            menuCanvas.create_text(x, y+190, text = "Bonus: LOCKED", fill = "red", font = fontLarge, tag = "bonusTitle")
            menuCanvas.create_text(x, y+215, text = "Complete Game Two to unlock", fill = "red", font = fontSmall, tag = "bonusTitle")
            
        #creates score 'buttons'
        gameScoresPhoto = PhotoImage(file = "images/crown.gif")
        menuCanvas.gameScoresPhoto = gameScoresPhoto
        menuCanvas.create_image(x2, y, image = gameScoresPhoto, tag = "gameScoresOne")
        menuCanvas.tag_bind("gameScoresOne", "<ButtonPress-1>", lambda e: showScores(e, menuWindow, 1))
        menuCanvas.create_image(x2, y+40, image = gameScoresPhoto, tag = "gameScoresTwo")
        menuCanvas.tag_bind("gameScoresTwo", "<ButtonPress-1>", lambda e: showScores(e, menuWindow, 2))
        menuCanvas.create_image(x2, y+115, image = gameScoresPhoto, tag = "gameScoresThree")
        menuCanvas.tag_bind("gameScoresThree", "<ButtonPress-1>", lambda e: showScores(e, menuWindow, 3))
        menuCanvas.create_image(x2, y+190, image = gameScoresPhoto, tag = "bonusScores")
        menuCanvas.tag_bind("bonusScores", "<ButtonPress-1>", lambda e: showScores(e, menuWindow, 4))

        #creates clickable score options title
        menuCanvas.create_text(x-100, y2, text = "Score Options", fill = "red", font = fontSmall, tag = "scoreOptionsMenu")
        menuCanvas.tag_bind("scoreOptionsMenu", "<ButtonPress-1>", lambda e: scoreOptions(e, menuWindow))

        #creates clickable enter code title
        menuCanvas.create_text(x+100, y2, text = "Enter Code", fill = "red", font = fontSmall, tag = "enterCode")
        menuCanvas.tag_bind("enterCode", "<ButtonPress-1>", lambda e: enterCode(e, menuWindow))
    
        menuWindow.mainloop()

class GameSetup():
    """ creates the game interface and runs it """
    def __init__(event, menuWindow, option):
        global getScore
        #deletes menuWindow
        menuWindow.withdraw()

        #creates gameWindow
        gameWindow = Toplevel()
        if option == 1:
            gameWindow.title("Game 1: Paying Exact Amounts")
        elif option == 2:
            gameWindow.title("Game 2: Giving Change")
        else:
            gameWindow.title("Game 3: Changing the Price")
      
        
        #set up canvas - uses random background color
        backgroundList = ["chartreuse", "cyan", "orange", "red", "yellow"]
        backgroundNumber = random.randint(0,len(backgroundList)-1)
        gameCanvas = Canvas(gameWindow, width = 700, height = 800, bg = backgroundList[backgroundNumber])
        #gameWindow.winfo_screenheight()-50
        gameCanvas.grid(columnspan = 3)

        #prevent exit using the window button
        #only allowed to exit through the home button
        preventExit(gameWindow)
        homeArrow(gameCanvas, gameWindow, "GameSetup")
        
        #create basic GUI
        gameCanvas.create_rectangle(300,375,600,600,tag="answerArea", fill="lawngreen", outline="red", width=4)
        gameCanvas.create_rectangle(47,40,652,170,tag="objectArea", fill="darkorange", outline="red", width=4)
        gameCanvas.create_rectangle(35,210,290,400,tag="coinBankArea", fill="cyan", outline="red", width=4)
        gameCanvas.create_rectangle(10, 429, 281, 672, tag="characterArea", fill="yellow", outline="red", width=6)

        #waits for user to start the game
        messagebox.showinfo("Ready to start?", "Click to start the game")

        #selects objects, puts them on the screen and then assigns them a price
        objectList = ["bird", "boat", "car", "chocolate", "dinosaur", "dog", "football", "plane", "soldier", "train"]
        usedList = []
        gameObjectList = []
        #selects six random objects
        for i in range(0,6):
            #None will be replaced later on
            gameObjectList.append([None, None])
            unusedNumber = False
            #chooses a random number and checks if it's already been used
            while unusedNumber == False:
                number = random.randint(0,9)
                if number not in usedList:
                    unusedNumber = True
                    
            #gets the image file and adds it to the screen
            fileName = "images/objects/" + objectList[number] + ".gif"
            locals()["image" + str([i])] = PhotoImage(file = fileName)
            globals()["gameCanvas.image" + str(i)] = locals()["image" + str([i])]
            gameCanvas.create_image((i+1)*100, 100, image = locals()["image" + str([i])], tag = objectList[number])

            #adds object number to usedList
            usedList.append(number)
            
            #creates a random price
            #adds object and price to the gameObjectList
            gameObjectList[i][0] = objectList[number]
            gameObjectList[i][1] = random.randint(25,175)
            
            #converts price into a string to display on-screen
            #differentiates between using pound or pennies based off of the value
            if gameObjectList[i][1] > 99:
                strPrice = "£1." + str(gameObjectList[i][1])[1:3]
            else:
                strPrice = str(gameObjectList[i][1]) + "p"
                
            gameCanvas.create_text((i+1)*100, 155, text = strPrice, tag = "textPrice", font = ("Times", 14), fill = "white")

        #adds the first character image, sound and text
        #changes to this will be provided through changeCharacterStatus in the coinBank module
        characterPhoto = PhotoImage(file = "images/characters/characterNeutral.gif")
        gameCanvas.characterPhoto = characterPhoto
        gameCanvas.create_image(145, 550, image = characterPhoto, tag = "characterImage")
        gameCanvas.create_text(200, 480, text = "Click an object!", tag = "characterText")
        winsound.PlaySound("sounds/ready.wav",winsound.SND_FILENAME)

        #creates label for answer area
        gameCanvas.create_text(430, 360, text="Pay Here", tag="textPayHere", font = ("Times", 14), fill = "blue")

        #creates labels for total, score and time left
        gameCanvas.create_text(380, 620, text="Current Total: ", tag="textCurrentTotal", font = ("Times", 14), fill = "blue")
        gameCanvas.create_text(380, 640, text="Current Score: ", tag="textCurrentScore", font = ("Times", 14), fill = "blue")
        gameCanvas.create_text(380, 660, text="Remaining Time", tag="textRemainingTime", font = ("Times", 14), fill = "blue")
        #creates the start value for the score
        gameCanvas.create_text(450, 640, text="0", tag="textScore", font = ("Times", 14), fill = "blue")
        #the other values are created within the coinBank module and timer function

    
        #calls the NumberLine module
        NumberLine(gameCanvas, gameWindow)
        #calls the CoinBank module
        CoinBank(gameCanvas, gameObjectList, option)
        
        #set up timer
        #time in milliseconds
        if option == 1:
            #4 minutes
            timeValue = 240000
        else:
            #5 minutes
            timeValue = 300000

        #ends the game after time completed
        gameCanvas.after(timeValue, endGame, option, gameWindow, None)
        #calls function to display time remaining on screen
        timer(timeValue/1000, gameCanvas)

        #calls the instance of GetScore, then uses it to reset the score to ensure it is 0
        getScore = GetScore()
        getScore.resetScore()
      

class BonusGameSetup():
    """ creates the bonus game and runs it """
    def __init__(self, menuWindow):
        #deletes menuWindow
        menuWindow.withdraw()

        #creates variables used throughout the class
        #three-dimensional array storing tagName, coordinates and the image variable
        self.usedTags = []
        #list for tiles the user has clicked on (and so is trying to match)
        self.selectedList = [None, None]
        #score is a variable that checks the number of matches
        #and is updated at the start of every level
        #turns is the variable that will be used in the score files
        self.score = 0
        #n is the number of objects in the level
        #hence level number would be n-1
        self.n = 2
        self.turns = 0
        
        #creates gameWindow
        self.gameWindow = Toplevel()
        self.gameWindow.title("Bonus Game!")

        #set up canvas - uses random background color
        backgroundList = ["chartreuse", "cyan", "orange", "red", "yellow"]
        backgroundNumber = random.randint(0,4)
        self.gameCanvas = Canvas(self.gameWindow, width = 700, height = 700, bg = backgroundList[backgroundNumber])
        self.gameCanvas.grid(columnspan = 3)
        
        #prevent exit using the window button
        #only allowed to exit through the home button
        preventExit(self.gameWindow)
        homeArrow(self.gameCanvas, self.gameWindow, "BonusGameSetup")
        
        #displaying number of turns on screen
        self.gameCanvas.create_text(450, 550, text="Number of turns:", tag="textTurnsHeading", font = ("Times", 14), fill = "blue")
        self.gameCanvas.create_text(450, 570, text="0", tag="textTurns", font = ("Times", 14), fill = "blue")

        #calls level creation function
        self.createLevel()

        #displays the character image, with accompanying sound and text        
        characterPhoto = PhotoImage(file = "images/characters/characterNeutral.gif")
        self.gameCanvas.characterPhoto = characterPhoto
        self.gameCanvas.create_image(145, 550, image = characterPhoto, tag = "characterImage")
        self.gameCanvas.create_text(210, 475, text = "Good Luck!", tag = "characterText")
        winsound.PlaySound("sounds/ready.wav",winsound.SND_FILENAME)
        
    def createLevel(self):
        """ creates each level of the bonus game """
        objectList = ["bird", "boat", "car", "chocolate", "dinosaur", "dog", "football", "plane", "soldier", "train"]
        #default coordinate list for level one
        coordList = [[75,100],[75,200],[175,100],[175,200]]
        #sets up grid for the specific number of objects
        #default grid
        #[_][_]
        #[_][_]
        if self.n >= 3:
            #adds an extra column
            coordList.append([275,100])
            coordList.append([275,200])
            #current grid
            #[_][_][_]
            #[_][_][_]
        if self.n >= 4:
            #adds an extra column
            coordList.append([375,100])
            coordList.append([375,200])
            #current grid
            #[_][_][_][_]
            #[_][_][_][_]
        if self.n >= 5:
            #adds an extra column
            coordList.append([475,100])
            coordList.append([475,200])
            #current grid
            #[_][_][_][_][_]
            #[_][_][_][_][_]
        if self.n >= 6:
            #removes the last column
            #adds a new row
            coordList.pop()
            coordList.pop()
            coordList.append([75,300])
            coordList.append([175,300])
            coordList.append([275,300])
            coordList.append([375,300])
            #current grid
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_][_][_]
        if self.n >= 7:
            #adds the start of another row
            coordList.append([75,400])
            coordList.append([175,400])
            #current grid
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_]
        if self.n >= 8:
            #completes the row
            coordList.append([275,400])
            coordList.append([375,400])
            #current grid
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_][_][_]
        if self.n >= 9:
            #starts final row
            coordList.append([475,100])
            coordList.append([475,200])
            #current grid
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_]
        if self.n == 10:
            #completes final row
            coordList.append([475,300])
            coordList.append([475,400])
            #final grid
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_][_][_]
            #[_][_][_][_]
        #set up lists which will be used in the creation loop    
        usedList = []
        usedCoords = []
        
        for i in range(0,self.n):
            #selects a random object
            unusedNumber = False
            while unusedNumber == False:
                number = random.randint(0,9)
                #check the object is not already in use
                if number not in usedList:
                    unusedNumber = True
                    
            #creates two tiles for the object
            for j in range(0,2):
                #sets up object image
                fileNameTurned = "images/objects/" + objectList[number] + ".gif"
                locals()["imageTurned" + str(i) + str(j)] = PhotoImage(file = fileNameTurned)
                globals()["gameCanvas.imageTurned" + str(i) + str(j)] = locals()["imageTurned" + str(i) + str(j)]
                
                #selects a random coordinate pair for the tile
                unusedCoords = False
                while unusedCoords == False:
                    coordNumber = random.randint(0, len(coordList)-1)
                    #checks the coordinate pair has not already been used
                    if coordNumber not in usedCoords:
                        unusedCoords = True
                        
                tagName = objectList[number] + str(j)

                #creates the actual tiles
                fileNameQuestionMark = "images/questionMark.gif"
                locals()["image" + str(i) + str(j)] = PhotoImage(file = fileNameQuestionMark)
                globals()["self.gameCanvas.image" + str(i) + str(j)] = locals()["image" + str(i) + str(j)]
                self.gameCanvas.create_image(coordList[coordNumber], image = locals()["image" + str(i) + str(j)], tag = tagName)

                #adds information to lists for future reference
                usedCoords.append(coordNumber)
                self.usedTags.append([tagName, coordList[coordNumber], locals()["imageTurned" + str(i) + str(j)]])

                #sets up mouse bind through the bindTag class
                self.bindTag(tagName, coordList[coordNumber], locals()["imageTurned" + str(i) + str(j)])

            #adds information to lists for future reference    
            usedList.append(number)
        
    def clicked(self, event, tagName, coords, fileName):
        """ the called function when a tile is clicked - it adds the tile to the selectedList
            it then checks if the player has already has an active tile, and if so will compare the values
            if not it will do nothing else"""
        #'turns over' the tile by creating the actual image and placing it on top
        tagName = tagName + "actual"
        self.gameCanvas.create_image(coords, image = fileName, tag = tagName)

        #unbind to try and stop player from breaking game
        #one of two measures to do this
        for tag in self.usedTags:
            self.gameCanvas.tag_unbind(tag[0], "<ButtonPress-1>")
            
        #checks that the tile has not already been selected
        if tagName not in self.selectedList:
            #checks what position to place it in
            if self.selectedList[0] == None:
                self.selectedList[0] = tagName
            elif self.selectedList[1] == None:
                #list full; game will check for a match

                #updates number of turns
                self.turns += 1
                self.gameCanvas.delete("textTurns")
                self.gameCanvas.create_text(450, 570, text=self.turns, tag="textTurns", font = ("Times", 14), fill = "blue")
                
                #checks whether the two selected tiles match
                self.selectedList[1] = tagName
                if self.selectedList[0][0:-7] == self.selectedList[1][0:-7]:
                    #resets selectedList
                    self.selectedList[0] = None
                    self.selectedList[1] = None
                    
                    self.score += 1
                    
                    #checks whether level is completed
                    if self.score == self.n:
                        self.gameCanvas.after(1000, self.deleteLevel)
                        
                else:
                    #if no match, delete the turned over tiles
                    self.gameCanvas.after(1000, self.deleteImages)
            else:
                #the second anti-breaking measure, this one deletes any image selected when the list is full
                self.gameCanvas.delete(tagName)

        for tag in self.usedTags:
            #re-binds the tags so the player can select again
            self.bindTag(tag[0], tag[1], tag[2])
        
    def deleteImages(self):
        """ if the answer if not correct this function will delete the turned tiles to reveal the original '?' ones """
        self.gameCanvas.delete(self.selectedList[0], self.selectedList[1])
        self.selectedList[0] = None
        self.selectedList[1] = None 

    def deleteLevel(self):
        """ congratulates the player on completing the level then clears the GUI
            depending on the level in question, it will then create the next level or end the game """
        #congratulates user
        self.gameCanvas.delete("characterText")
        characterStatusNumber = random.randint(0,1)
        characterStatusList = [["Good Work!", "sounds/wellDone.wav"], ["Correct - Well Done!", "sounds/correct.wav"]]
        self.gameCanvas.create_text(210, 475, text = characterStatusList[characterStatusNumber][0], tag = "characterText")
        winsound.PlaySound(characterStatusList[characterStatusNumber][1],winsound.SND_FILENAME)                   

        #deletes the tiles
        for tag in self.usedTags:
            tagActual = tag[0] + "actual"
            self.gameCanvas.delete(tag[0])
            self.gameCanvas.delete(tagActual)
            
        #resets level score
        self.score = 0
        #increases number of tiles
        self.n += 1
        if self.n == 11:
            #ends the game
            endGame(4, self.gameWindow, self.turns)            
        else:
            #moves to next level
            self.createLevel()

    def bindTag(self, tagName, coords, fileName):
        """ sets up the mouse bind """
        self.gameCanvas.tag_bind(tagName, "<ButtonPress-1>", lambda e: self.clicked(e, tagName, coords, fileName))
                        
def askName(score, option):
    """ creates a popup and asks for the player's name """
    popup = Toplevel()
    popupText = Label(popup, text = "Enter you name for the scoreboard!")
    popupText.grid(row = 0, column = 0)
    popupEntry = Entry(popup, width = 50)
    popupEntry.grid(row = 1, column = 0)
    popupEntry.focus_set()
    popupButton = Button(popup, text = "Enter", command = lambda: exitPopup(popup, popupEntry, score, option))
    popupButton.grid(row = 2, column = 0)

    preventExit(popup)
    
    #plays congratulations sound
    winsound.PlaySound("sounds/congratulations.wav",winsound.SND_FILENAME)

def checkCode(popup, popupEntry):
    """ checks the code is correct """
    global game2Unlocked, game3Unlocked

    #fetches the code from the popup
    userCode = popupEntry.get()
    
    #delete popup window
    popup.destroy()

    #opens passcode file
    codeFile = open("unlockCodes.txt", "r")

    #gets codes from file
    codeList = []
    for code in codeFile:
        codeList.append(code[0:-1])

    if userCode == codeList[0]:
        game2Unlocked = True
        unlockedPopup(2)
    elif userCode == codeList[1]:
        game2Unlocked = True
        game3Unlocked = True
        unlockedPopup(3)
    else:
        messagebox.showerror("Invalid code", "Sorry, that is not a valid code.")
        
    #close file
    codeFile.close()

    #recreates menu
    MenuSetup()

def dummy():
    """ dummy function which stops the user from exiting the name submission which breaks the game
        this function doesn't actually do anything"""
    None
    
def endGame(option, gameWindow, score):
    """ a function which displays the player's score """
    global getScore
    gameWindow.withdraw()
    
    if option != 4:
        #in this scenario the score has been passed through as None
        #calls the returnScore function in the GetScore class of the coinBank module to get the score
        score = getScore.getScore()
        score = str(score)
        messagebox.showinfo("Well done!", ("You scored: " + score + "!"))
    else:
        #bonus game has score passed through
        score = str(score)
        messagebox.showinfo("Well done!", ("You took: " + score + "turns!"))
        
    #launches askName function to get the player's name
    askName(score, option)

def enterCode(event, menuWindow):
    """ allows the user to enter a code to unlock games they unlocked in a previous game
        like the codes in old-fashioned games that took you back to the level you were on """
    #deletes window
    menuWindow.destroy()

    #creates a popup box to enter the code
    popup = Toplevel()
    popupText = Label(popup, text = "Enter your code")
    popupText.grid(row = 0, column = 0)
    popupEntry = Entry(popup, width = 50)
    popupEntry.grid(row = 1, column = 0)
    popupEntry.focus_set()
    popupButton = Button(popup, text = "Enter", command = lambda: checkCode(popup, popupEntry))
    popupButton.grid(row = 2, column = 0)
    #bind enter key as welll as the built in button
    popup.bind("<Return>", lambda e: checkCode(popup, popupEntry))

    preventExit(popup)

def exitPopup(popup, popupEntry, score, option):
    """ validates the inputed name and then exits the askName popup """
    global game2Unlocked, game3Unlocked

    #fetches the name from the popup
    name = popupEntry.get()

    if validateName(name) == True:
        saveData(name, score, option)

        #delete popup window
        popup.destroy()
        
        #checks if there is a game to unlock
        #if so, calls a function to inform the user
        if option == 1 and game2Unlocked == False:
            game2Unlocked = True
            unlockedPopup(2)
        elif option == 2 and game3Unlocked == False:
            game3Unlocked = True
            unlockedPopup(3)
                
        #recreates menu
        MenuSetup()
    else:
        #delete popup window
        popup.destroy()
        #recreate popup window by re-calling the function
        askName(score, option)              

def home(event, window):
    """ takes user back to the main menu """
    #deletes window
    window.destroy()
    #recreates menu
    MenuSetup()

def homeArrow(canvas, window, source):
    if source == "GameSetup":
        x = 600
        y = 650
    elif source == "BonusGameSetup":
        x = 600
        y = 600
    else:
        x = 400
        y = 400
    homeArrow = chr(8592)
    canvas.create_text(x, y, text = homeArrow, tag = "homeLink", font = ("Times", 100), fill = "black")
    canvas.create_text(x+10, y+30, text = "home", tag = "homeLink", font = ("Times", 15), fill = "black")
    if source == "searchName":
        canvas.tag_bind("homeLink", "<ButtonPress-1>", lambda e: scoreOptions(e, window))
    else:
        canvas.tag_bind("homeLink", "<ButtonPress-1>", lambda e: home(e, window))

def mergeFiles(event, option, scoreMenuWindow):
    """ merges two score files together """
    #deletes scoreMenuWindow
    scoreMenuWindow.destroy()
    
    #select file to merge into based upon the option selected
    if option == 1:
        saveFileName = "gameHighScoresOne.txt"
        strOption = "One"
    elif option == 2:
        saveFileName = "gameHighScoresTwo.txt"
        strOption = "Two"
    elif option == 3:
        saveFileName = "gameHighScoresThree.txt"
        strOption = "Three"
    else:
        saveFileName = "gameHighScoresBonus.txt"
        strOption = None

    #creates message box
    if strOption != None:
        messagebox.showinfo("Choose the file", ("Choose the file you want to merge with the file for Game" + strOption + "."))
    else:
        messagebox.showinfo("Choose the file", "Choose the file you want to merge with the file for the Bonus Game.")

    #opens a file dialog so the user can select the file they want    
    mergeFileFound = False

    status = None
    
    while mergeFileFound == False:
        mergeFileName = filedialog.askopenfilename(title="Choose the file")
        error = validateFile(mergeFileName)
        if error == None:
            mergeFileFound = True
            #appends the details from mergeFile to saveFile        
            saveFile = open(saveFileName, "a")
            mergeFile = open(mergeFileName, "r")
            for record in mergeFile:
                mergeFields = record.split(",")
                mergeFields[2] = mergeFields[2][0:-1]

            #close both files
            saveFile.close()
            mergeFile.close()

            #tell user it has been a success
            messagebox.showinfo("Merge complete", "Merge complete.")
    
            #takes them back to scoreOptionsWindow
            scoreOptions(None, None)            
        elif error == "no file":
            #if no file is selected take then back to the scoreOptionsMenu
            status = messagebox.askretrycancel("Error", "You did not select a file.", icon = "error")
        elif error == "invalid file":
            status = messagebox.askretrycancel("Error", "You did not select a text file.", icon = "error")
        elif error == "incompatible file":
            status = messagebox.askretrycancel("Error", "The contents of your file in not compatible.", icon = "error")
            
        if status == False:
            #user doesn't want to try again, takes back to the score options menu
            mergeFileFound = True
            scoreOptions(None, None)

def printData(scoreWindow, scoreCanvas, saveList, recordNumber):
    """ prints data on screen """
    #uses number of records (from selectData) and the amount of space granted each record (20 pixels high)
    #and adds an offset of 75 to account for the space taken up by titles
    windowLength = 20*recordNumber + 75

    #scrollbar created - will only be active if windowLength exceeds the height of the window (500 pixels)
    scrollbar = Scrollbar(scoreWindow)
    scrollbar.grid(row = 0, column = 5, sticky = N+S)
    scoreCanvas.config(yscrollcommand=scrollbar.set, scrollregion=(0,0,100,windowLength))
    scrollbar.config(command=scoreCanvas.yview)

    x = 50
    y = 50
    fontHeading = ("Times", 20)
    fontData = ("Times", 14)
    
    #creates headings at the top of each column
    scoreCanvas.create_text(x, y, text = "Score", tag = "scoreHeading", font = fontHeading, fill = "red")
    scoreCanvas.create_text(x+100, y, text = "Name", tag = "nameHeading", font = fontHeading, fill = "red")
    scoreCanvas.create_text(x+300, y, text = "Date", tag = "dateHeading", font = fontHeading, fill = "red")

    #prints each record on screen
    for i in range(0, len(saveList)):
        scoreString = str(saveList[i][1])
        nameString = str(saveList[i][0])
        dateString = str(saveList[i][2])[:-1]

        scoreCanvas.create_text(x, (20*i)+75, text = scoreString, tag = "scoresText", font = fontData, fill = "blue")
        scoreCanvas.create_text(x+100, (20*i)+75, text = nameString, tag = "namesText", font = fontData, fill = "blue")
        scoreCanvas.create_text(x+300, (20*i)+75, text = dateString, tag = "datesText", font = fontData, fill = "blue")
 

def preventExit(window):
    #prevent exit using the corner "X" button
    window.protocol('WM_DELETE_WINDOW', dummy)

def saveData(name, score, option):
    """ saves the score details to the correct file """
    #uses option to open the correct file
    if option == 1:
        saveFile = open("gameHighScoresOne.txt", "a")
    elif option == 2:
        saveFile = open("gameHighScoresTwo.txt", "a")
    elif option == 3:
        saveFile = open("gameHighScoresThree.txt", "a")
    else:
        saveFile = open("gameHighScoresBonus.txt", "a")

    #prints name, score and the current time/date to the end of the file    
    print(name, score, time.asctime(), file = saveFile, sep = ",")

    #closes the file
    saveFile.close()

def scoreOptions(event, window):
    """ shows score options menu """
    global canvasX, canvasY
    try:
        #deletes menuWindow
        window.withdraw()
    except:
        #avoids crashing if they didn't come from the main menu or search results, as there's no window to withdraw
        None
    
    #creates scoreMenuWindow
    scoreMenuWindow = Toplevel()
    scoreMenuWindow.title("Score Options")

    #set up canvas - uses random background color
    backgroundList = ["chartreuse", "cyan", "yellow"]
    backgroundNumber = random.randint(0,2)
    scoreMenuCanvas = Canvas(scoreMenuWindow, width = canvasX, height = canvasY, bg = backgroundList[backgroundNumber])
    scoreMenuCanvas.grid(columnspan = 3)

    preventExit(scoreMenuWindow)

    x = 200
    y = 50
    fontBig = ("Arial", 32)
    fontMiddle = ("Arial", 20, "bold")
    fontSmall = ("Arial", 15)
    
    #creates the options and sets up the binding
    scoreMenuCanvas.create_text(x, y, text = "Score Options", fill = "blue", font = fontBig)
    scoreMenuCanvas.create_text(x, y+50, text = "Merge Save Files", fill = "red", font = fontMiddle, tag = "menuMergeFiles")
    scoreMenuCanvas.create_text(x, y+75, text = "Game One", fill = "red", font = fontSmall, tag = "menuMergeFilesOne")
    scoreMenuCanvas.create_text(x, y+100, text = "Game Two", fill = "red", font = fontSmall, tag = "menuMergeFilesTwo")
    scoreMenuCanvas.create_text(x, y+125, text = "Game Three", fill = "red", font = fontSmall, tag = "menuMergeFilesThree")
    scoreMenuCanvas.create_text(x, y+150, text = "Bonus Game", fill = "red", font = fontSmall, tag = "menuMergeFilesBonus")

    scoreMenuCanvas.tag_bind("menuMergeFilesOne", "<ButtonPress-1>", lambda e: mergeFiles(e, 1, scoreMenuWindow))
    scoreMenuCanvas.tag_bind("menuMergeFilesTwo", "<ButtonPress-1>", lambda e: mergeFiles(e, 2, scoreMenuWindow))
    scoreMenuCanvas.tag_bind("menuMergeFilesThree", "<ButtonPress-1>", lambda e: mergeFiles(e, 3, scoreMenuWindow))
    scoreMenuCanvas.tag_bind("menuMergeFilesBonus", "<ButtonPress-1>", lambda e: mergeFiles(e, 4, scoreMenuWindow))
    
    scoreMenuCanvas.create_text(x, y+200, text = "Search Save Files", fill = "red", font = fontMiddle, tag = "menuSearchFiles")
    scoreMenuCanvas.create_text(x, y+225, text = "Game One", fill = "red", font = fontSmall, tag = "menuSearchFilesOne")
    scoreMenuCanvas.create_text(x, y+250, text = "Game Two", fill = "red", font = fontSmall, tag = "menuSearchFilesTwo")
    scoreMenuCanvas.create_text(x, y+275, text = "Game Three", fill = "red", font = fontSmall, tag = "menuSearchFilesThree")
    scoreMenuCanvas.create_text(x, y+300, text = "Bonus Game", fill = "red", font = fontSmall, tag = "menuSearchFilesBonus")

    scoreMenuCanvas.tag_bind("menuSearchFilesOne", "<ButtonPress-1>", lambda e: searchFiles(e, 1, scoreMenuWindow))
    scoreMenuCanvas.tag_bind("menuSearchFilesTwo", "<ButtonPress-1>", lambda e: searchFiles(e, 2, scoreMenuWindow))
    scoreMenuCanvas.tag_bind("menuSearchFilesThree", "<ButtonPress-1>", lambda e: searchFiles(e, 3, scoreMenuWindow))
    scoreMenuCanvas.tag_bind("menuSearchFilesBonus", "<ButtonPress-1>", lambda e: searchFiles(e, 4, scoreMenuWindow))

    homeArrow(scoreMenuCanvas, scoreMenuWindow, "scoreOptions")

def searchFiles(event, option, scoreMenuWindow):
    """ calls the popup which will allow the user to search for a name in the save files """
    if scoreMenuWindow != None:
        #deletes scoreMenuWindow
        scoreMenuWindow.destroy()

    #choose file to search based
    if option == 1:
        fileName = "gameHighScoresOne.txt"
    elif option == 2:
        fileName = "gameHighScoresTwo.txt"
    elif option == 3:
        fileName = "gameHighScoresThree.txt"
    else:
        fileName = "gameHighScoresBonus.txt"

    #creates search popup
    popup = Toplevel()
    popupText = Label(popup, text = "Enter the name you're looking for.")
    popupText.grid(row = 0, column = 0)
    popupEntry = Entry(popup, width = 50)
    popupEntry.grid(row = 1, column = 0)
    popupEntry.focus_set()
    popupButton = Button(popup, text = "Enter", command = lambda: searchName(popup, popupEntry, option, fileName))
    popupButton.grid(row = 2, column = 0)
    popup.bind("<Return>", lambda e: searchName(popup, popupEntry, option, fileName))
    
    preventExit(popup)
    
def searchName(popup, popupEntry, option, fileName):
    """ searchs the file for the name, providing it's valid, and then sorts and displays any matches """
    #gets value from popup
    search = popupEntry.get()

    if validateName(search) == True:
        #delete popup
        popup.destroy()
        
        #open relevant file
        file = open(fileName, "r")

        #gets data from selectData
        #recordNumber not needed, but selectData returns it for the standard display score
        saveList, recordNumber = selectData(file)

        #checks the name against the file data
        #foundList stores the position of the data in the list
        foundList = []
        #len(saveList[0]-1 as the list starts at 0
        for n in range (0, len(saveList)):
            #lower case to avoid case errors
            if search.lower() in saveList[n][0].lower():
                foundList.append(n)

        if len(foundList) > 0:
            #gathers the actual data from the list using the found positions
            saveListFound = []
            i = 0
            for item in foundList:
                saveListFound.append([])
                saveListFound[i].append(saveList[item][0])
                saveListFound[i].append(saveList[item][1])
                saveListFound[i].append(saveList[item][2])
                i += 1
            #creates window        
            scoreWindow = Toplevel()
            #choose the correct title for the game
            if option == 1:
                scoreWindow.title("Search results: Game One")
                strOption = "One"
            elif option == 2:
                scoreWindow.title("Search results: Game Two")
                strOption = "Two"
            elif option == 3:
                scoreWindow.title("Search results: Game Three")
                strOption = "Three"
            else:
                scoreWindow.title("Search results: Bonus Game")
                strOption = None

            #set up canvas - uses random background color
            backgroundList = ["chartreuse", "cyan", "yellow"]
            backgroundNumber = random.randint(0,2)

            #grid for canvas
            scoreCanvas = Canvas(scoreWindow, width = 700, height = 500, bg = backgroundList[backgroundNumber])
            scoreCanvas.grid(columnspan = 3, sticky = N+S+E+W)

            preventExit(scoreWindow)
            
            #page title
            if strOption != None:
                scoreCanvas.create_text(300, 20, text = ("Search results for " + search + " for Game " + strOption), tag = "searchResultsTitle", font = ("Times", 20), fill = "red")
            else:
                scoreCanvas.create_text(200, 20, text = ("Search results for " + search + " for the Bonus Game"), tag = "searchResultsTitle", font = ("Times", 20), fill = "red")

            #sort and then print data using respective functions
            if len(saveListFound) != 0:
                saveListFound = sortData(saveListFound)
                #len(foundList) used as recordNumber counted every record, not just the found ones.
                printData(scoreWindow, scoreCanvas, saveListFound, len(saveListFound))

            homeArrow(scoreCanvas, scoreWindow, "searchName")
        else:
            messagebox.showerror("No results", ("No search results for " + search + "."))
            popup.destroy()
            scoreOptions(None, None)
        
        #close save file
        file.close()
        
    else:
        #not valid
        #delete popup
        popup.destroy()
        #recall the search field
        searchFiles(None, option, None)
        
def selectData(file):
    """ selects data from the score file """
    #saveList will store all the data in the file
    saveList = []
    #variable that puts the save data into the right position in the list
    recordNumber = 0
    
    for record in file:
        #creates the list inside saveList for the record
        saveList.append([])
        #splits the record into its three components
        fields = record.split(",")
        #adds each field into the list
        for i in range(0, 3):
            if i == 0:
                saveList[recordNumber].append(fields[i])
            elif i == 1:
                saveList[recordNumber].append(fields[i])
            else:
                saveList[recordNumber].append(fields[i])

        recordNumber += 1
        #returns values for sorting and printing
    return saveList, recordNumber

def showScores(event, menuWindow, option):
    """ displays a score file """
    global cavnasX, canvasY

    #deletes menuWindow
    menuWindow.withdraw()

    #creates scoreWindow
    scoreWindow = Toplevel()
    #selects both the scoreWindow title and the file to open based off of the option
    if option == 1:
        scoreWindow.title("Game Scores 1: Paying Exact Amounts")
        saveFile = open("gameHighScoresOne.txt", "r")
    elif option == 2:
        scoreWindow.title("Game Scores 2: Giving Change")
        saveFile = open("gameHighScoresTwo.txt", "r")
    elif option == 3:
        scoreWindow.title("Game Scores 3: Changing the Price")
        saveFile = open("gameHighScoresThree.txt", "r")
    else:
        scoreWindow.title("Game Scores - Bonus Game")
        saveFile = open("gameHighScoresBonus.txt", "r")
    
    preventExit(scoreWindow)
       
    #set up canvas - uses random background color
    backgroundList = ["chartreuse", "cyan", "yellow"]
    backgroundNumber = random.randint(0,2)

    scoreCanvas = Canvas(scoreWindow, width = canvasX, height = canvasY, bg = backgroundList[backgroundNumber])
    scoreCanvas.grid(columnspan = 3, sticky = N+S+E+W)

    #selects, sorts and prints the data using three seperate functions
    saveList, recordNumber = selectData(saveFile)
    saveList = sortData(saveList)
    printData(scoreWindow, scoreCanvas, saveList, recordNumber)

    homeArrow(scoreCanvas, scoreWindow, "showScores")

    #close save file
    saveFile.close()

def sortData(saveList):
    """ sorts data by score - bubble sort """

    #length of list (-1 as the list starts at 0)
    n = len(saveList)-1

    #standard bubble sort algorithm
    #sorts by score (item 1 in the list) and changes the rest of the values accordingly
    swaps = True
    while swaps == True:
        swaps = False
        for i in range(0, n):
            if int(saveList[i][1]) < int(saveList[i+1][1]):
                tempName = saveList[i][0]
                saveList[i][0] = saveList[i+1][0]
                saveList[i+1][0] = tempName

                tempScore = saveList[i][1]
                saveList[i][1] = saveList[i+1][1]
                saveList[i+1][1] = tempScore

                tempDate = saveList[i][2]
                saveList[i][2] = saveList[i+1][2]
                saveList[i+1][2] = tempDate
                
                swaps = True
        n-=1    
    return saveList

def timer(i, gameCanvas):
    """ creates a timer which displays on screen """
    #delete previous value of textTimer
    gameCanvas.delete("textTimer")

    #converts time into minutes and seconds
    timeLeft = float(i/60)
    timeLeftMinutes = int(str(timeLeft)[0])
    timeLeftSeconds = (timeLeft - timeLeftMinutes)*60

    #works out how to display it on screen
    if str(int(timeLeftSeconds)) == "0":
        strTime = str(timeLeftMinutes) + ":" + "00"
    elif int(timeLeftSeconds) <= 9:
        strTime = str(timeLeftMinutes) + ":0" + str(int(timeLeftSeconds))        
    else:
        strTime = str(timeLeftMinutes) + ":" + str(int(timeLeftSeconds))

    #displays on screen
    gameCanvas.create_text(460, 660, text = strTime, tag="textTimer", font = ("Times", 14), fill = "blue")

    #if still time left, call function again
    if i > 0:
        gameCanvas.after(1000, timer, i-1, gameCanvas)

def unlockedPopup(gameUnlocked):
    """ creates a messagebox announcing the unlocked game """
    
    #plays congratulations sound
    winsound.PlaySound("sounds/congratulations.wav",winsound.SND_FILENAME)    

    #opens passcode file
    codeFile = open("unlockCodes.txt", "r")

    #gets data from file
    codeList = []
    for code in codeFile:
        #[0:-1] to avoid getting whitespace on the end
        codeList.append(code[0:-1])

    #adds the game name and the unlock code
    if gameUnlocked == 2:
        unlockedText = "Game #2: Giving Change. \n Your unlock code is: " + codeList[0] + ". Be sure to write it down!"
    else:
        unlockedText = "Game #3: Changing the Price and the Bonus Game! \n Your unlock code is: " + codeList[1] + ". Be sure to write it down!"
        
    messagebox.showinfo("Congratulations - New Game Unlocked!", ("Congratulations! You've unlocked " + unlockedText))
    
    #closes file
    codeFile.close()

def validateFile(file):
    if file == "":
        return "no file"
    else:
        textFile = file.find(".txt")
        if textFile != -1:
            #takes the records from the text file to check its structure matches
            mergeFile = open(file, "r")
            recordList = []
            for record in mergeFile:
                recordList.append(record)
            mergeFile.close()
            recordsValid = True

            #checks each record has three components
            i = 0
            while recordsValid == True and i < len(recordList):
                splitRecord = recordList[i].split(",")
                if len(splitRecord) == 3:
                    i+=1
                else:
                    #incompatible text file
                    recordsValid = False
                    return "incompatible file"
                
            if recordsValid == True:
                #valid file
                return None
        else:
            #not a text file
            return "invalid file"

def validateName(name):
    #checks the length of the name is not over 20 characters
    if len(name) <= 20: 
        #validates name to ensure there is actually content and not a blank input or spaces
        #^ means start, $ means end, \s means any space type
        spaceInName = re.match("^$|\s+", name)
        if spaceInName == None:
            #spaceInName equalling None means that the name is not empty
            #validates to ensure there is only alphabet characters and spaces
            #it does this by using the start and end regex codes
            validName = re.search("^[a-zA-Z .,'-]+$", name)
            if validName != None:
                #in this case None works as False, with a match being represented as something along
                #the lines of "<_sre.SRE_Match object at 0x02955B60>"
                return True
            else:
                messagebox.showerror("Invalid name", ("Invalid name - unacceptable character(s)." + 
                                                      "Please only use letters, spaces, periods (.), commas (,), apostrophes (') and dashes (-)."))
                return False
        else:
            messagebox.showerror("Invalid name", ("Invalid name - empty string. Please enter some text."))
            return False          
    else:
        messagebox.showerror("Invalid name", ("Invalid name - too long. Please enter a name less than or equal to 20 characters long."))
        return False

#program starts here    
#hides the unused Tk() level
unusedTk = Tk()
unusedTk.title("Charlie Counts: Money Matters")
unusedTk.withdraw()

#calls menu to run for the first time
MenuSetup()
