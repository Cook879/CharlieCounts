from tkinter import *

class NumberLine():
    """ the NumberLine class controls everything related to the number line """
    def __init__(self, gameCanvas, gameWindow):
        self.gameCanvas = gameCanvas
        self.gameWindow = gameWindow

        self.createNumberLineButton()
        
    def createNumberLineButton(self):
        """ creates the "click for number line" button which appears at the start of the game """
        self.gameCanvas.numberLineButton = Button(self.gameWindow, text = "Click for number line", width = 25, anchor = "s", command = lambda:self.generateFirstNumberLine(0, 30))
        self.gameCanvas.numberLineButton.grid(row = 1, column = 1, padx = 5)
        
    def generateFirstNumberLine(self, a, b):
        """ creates the basics of the number line and the other buttons """
        #deletes the createNumberLine button
        self.gameCanvas.numberLineButton.grid_forget()

        #creates the rectangle and line
        self.gameCanvas.create_rectangle(0, 700, 600, 800, fill = "white", tag = "numberLine")
        self.gameCanvas.create_line(10, 750, 590, 750, width = 5, fill = "black", tag = "numberLine")

        #creates the more, less and delete buttons
        self.gameCanvas.moreButton = Button(self.gameWindow, text = "Click for more numbers", width = 25, command = lambda:self.numbers(b, b+30))
        self.gameCanvas.moreButton.grid(row = 1, column = 2, padx = 5)

        self.gameCanvas.lessButton = Button(self.gameWindow, text = "Click for the previous numbers", width = 25, command =lambda:self.numbers(a-30, b-30))
        self.gameCanvas.lessButton.grid(row = 1, column = 0, padx = 5)        

        self.gameCanvas.deleteButton = Button(self.gameWindow, text = "Delete number line", width = 25, command = self.deleteNumberLine)
        self.gameCanvas.deleteButton.grid(row = 1, column = 1, padx = 5)

        #calls the function to add the numbers
        self.numbers(a,b)

        
    def numbers(self, a, b):
        """ creates the numbers on the number line """
        #deletes the previous numbers
        self.gameCanvas.delete("numberLineNumbers")

        #adds the numbers - position relative to the line depends on the number
        i = a
        for i in range(a, b):
            if i % 2 == 0:
                gap = (i-a)*20
                self.gameCanvas.create_line(10+gap, 750, 10+gap, 770, width = 3, fill = "red", tag = "numberLineNumbers")
                self.gameCanvas.create_text(10+gap, 780, text = i, tag = "numberLineNumbers")
            else:
                gap2 = (i-a-1)*20
                self.gameCanvas.create_line(30+gap2, 750, 30+gap2, 730, width = 3, fill = "blue", tag = "numberLineNumbers")
                self.gameCanvas.create_text(30+gap2, 720, text=i, tag = "numberLineNumbers")

        #button status depends on whether there are more numbers to load or not
        if b == 210:
            self.gameCanvas.moreButton.config(state = "disabled")
            self.gameCanvas.lessButton.config(state = "active")
        elif b == 30:
            self.gameCanvas.moreButton.config(state = "active")
            self.gameCanvas.lessButton.config(state = "disabled")
        else:
            self.gameCanvas.moreButton.config(state = "active")
            self.gameCanvas.lessButton.config(state = "active")
        #configures the buttons based on the number 
        self.gameCanvas.moreButton.config(command = lambda:self.numbers(b, b+30))
        self.gameCanvas.lessButton.config(command = lambda:self.numbers(a-30, b-30))
        
    def deleteNumberLine(self):
        """ deletes the number line entirely """
        #deletes the number line and numbers
        self.gameCanvas.delete("numberLine")
        self.gameCanvas.delete("numberLineNumbers")
        
        #calls to delete the buttons
        self.deleteButtons()

        #re-creates the create number line button
        self.createNumberLineButton()

    def deleteButtons(self):
        """ deletes the buttons when the player clicks to delete the number line """
        self.gameCanvas.moreButton.grid_forget()
        self.gameCanvas.lessButton.grid_forget()
        self.gameCanvas.deleteButton.grid_forget()

        
