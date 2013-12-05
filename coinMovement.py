class CoinMovement():
    """ assigns and controls the movement of coins """
    def __init__(self, gameCanvas, tag, x, y):
        #creates variables
        self.gameCanvas = gameCanvas
        self.tag = tag
        self.x = x
        self.y = y

        #sets up mouse control
        self.gameCanvas.tag_bind(self.tag, "<B1-Motion>", lambda event: self.moveCoin(event))
        
    def moveCoin(self, event):
        """ moves the selected coin """
        #find the difference between the mouse position and the coin's current position
        offsetX = event.x-self.x
        offsetY = event.y-self.y

        #move the coin by this difference so it ends up in the mouse position
        self.gameCanvas.move(self.tag,offsetX,offsetY)

        #set the coin's position to the mouse position
        self.x = event.x
        self.y = event.y

                
    
        
