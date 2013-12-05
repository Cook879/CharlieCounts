from coinMovement import CoinMovement

class Coin():
    """ creates a coin """
    def __init__(self, gameCanvas, listPosition, tag, x, y):
        #set up variables
        self.gameCanvas = gameCanvas
        self.coinSize, self.text, self.color, self.shape = coinValues(listPosition)
        self.tag = tag
        self.x = x
        self.y = y
        
        self.generateCoin()
        
        CoinMovement(self.gameCanvas, self.tag, self.x, self.y)
        
    def generateCoin(self):
        """ creates the actual coin """
        if self.shape == "circle":
            self.gameCanvas.create_oval(self.x-self.coinSize, self.y-self.coinSize, self.x+self.coinSize,
                                               self.y+self.coinSize, fill = self.color, outline = self.color, tag = self.tag)
        else:
            self.gameCanvas.create_polygon(self.x, self.y-(self.coinSize*0.9),
                         self.x+(self.coinSize*0.7), self.y-(self.coinSize*0.54),
                         self.x+(self.coinSize*0.84), self.y+(self.coinSize*0.2),
                         self.x+(self.coinSize*0.4), self.y+(self.coinSize*0.8),
                         self.x-(self.coinSize*0.4), self.y+(self.coinSize*0.8),
                         self.x-(self.coinSize*0.84), self.y+(self.coinSize*0.2),
                         self.x-(self.coinSize*0.7), self.y-(self.coinSize*0.54),
                         fill = self.color, outline = self.color, tag = self.tag)
        self.gameCanvas.create_text(self.x, self.y, text = self.text, fill = "white", tag = self.tag)

def coinValues(listPosition):
    """ assigns the relevant information for each coin """
    coinValueList = [[1, 25, "Sienna", "circle"], [2, 50, "Sienna", "circle"], [5, 20, "LightGrey", "circle"], [10, 50, "LightGrey", "circle"],
                     [20, 30, "LightGrey", "heptagon"], [50, 50, "LightGrey", "heptagon"], [100, 40, "Goldenrod", "circle"]]

    coinSize = coinValueList[listPosition][1]

    if coinValueList[listPosition][0] != 100:
        text = str(coinValueList[listPosition][0]) + "p"
    else:
        text = "£1"
        
    color = coinValueList[listPosition][2]
    shape = coinValueList[listPosition][3]
    return coinSize, text, color, shape
