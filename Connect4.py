#Vlad Vitalaru

from tkinter import *
from AIPlayer import *

class Connect4:
    '''Initialization of class Connect4's dimensions and board data'''
    def __init__(self, width, height, window):
        self.width = width
        self.height = height
        self.data = []

        self.gameOn = False         #Game state
        self.playerTurn = False     #Human player turn
        self.ai = None              #Assigned to AI class once game begins
        self.plyValue = 0           #Difficulty level value
        self.ox = "X"               #Human player is X    
        self.opp = "O"              #AI is O

        self.window = window
        self.frame = Frame(window, bg = "DodgerBlue2")
        self.frame.pack(fill = BOTH, expand = True)
        self.messageSize = 25
        self.diameter = 70
        self.initialColor = "snow"
        self.CanvasHeight = 480
        self.CanvasWidth = 560
        
        #Quit button
        self.quitButton = Button(self.frame, text='Quit', command=self.quitGame, bg ="Red4", fg="White smoke", font="SegoeUI 16 bold")
        self.quitButton.pack(side=RIGHT,padx=10, ipadx=30, ipady=1,)
        
        #New Game button
        self.newGameButton = Button(self.frame, text="New Game", bg ="green4", fg="white smoke", command=self.newGame, font="SegoeUI 16 bold")
        self.newGameButton.pack(side=RIGHT, padx=2, ipady=1)

        #Canvas background
        self.draw = Canvas(window, height=self.CanvasHeight, width=self.CanvasWidth, bg ="DodgerBlue2",
        highlightbackground = "DodgerBlue2")
        self.draw.bind('<Button-1>', self.mouseInput)
        self.draw.pack(fill=BOTH, expand=True)
        
        #Difficulty slider 
        self.plyslider = Scale(self.frame, from_=0, to=5, orient=HORIZONTAL, showvalue=0, bg="DodgerBlue2",
        label= " Difficulty:", troughcolor="snow", length=150, highlightbackground="DodgerBlue2",
        cursor="arrow", activebackground="DodgerBlue2", fg="White", command=self.setply, font="SegoeUI 16 bold")
        self.plyslider.pack(side = LEFT, padx=8)

        #Bottom text
        self.message = Label(text='Choose a difficulty level!',bg="DodgerBlue2",fg="White", font='SegoeUI 20 bold')
        self.message.pack(fill=BOTH, ipady=12)

        #creating the 2d gameboard    
        self.data = [[' ' for _ in range(width)] for _ in range(height)]
        self.update()
        
        
    '''Represents 2D array of game board data in terminal'''
    def __repr__(self):
        s = ''
        for row in range(self.height): #creates rows
            s += "|"
            for col in range(self.width): #creates columns
                s += self.data[row][col] + '|'
            s += '\n'
        s += '--'*self.width + '-\n' #creates bottom level

        for col in range(self.width): #creates bottom column numbers
            s += ' ' + str(col % 10)
        s += '\n'
        return s

    '''mouseInput() controls the game state, allowing a player to make a move then passing the 
    turn over to the AI. After each move, the gameboard is updated and checked for win conditions.'''
    def mouseInput(self, event):
        if self.gameOn:
            col = int(event.x/80)
            if self.playerTurn: #If playerTurn is True, it allows the player to make a move
                if self.allowsMove(col):
                    self.addMove(col,self.ox)
                    self.message.config(text = "AI Thinking...")
                    self.playerTurn = False #switches player turn to false, not allowing player to play until ai has placed a move
                    self.gameOn = False #locks gameboard, not allowing player to spam 2 quick moves before ai can move
                    self.update()
                    if self.winsFor(self.ox):
                        self.message.config(text = "Red Wins!")
                        self.playerTurn = True  #after player wins, switches playerturn to ON, not allowing ai to place a move after
                    elif self.playerTurn == False:
                        oMove = self.ai.nextMove(self) #calls nextMove from the Player class
                        self.addMove(oMove,self.opp)
                        self.update()
                        self.playerTurn = True #after ai has moved, player may now place another move
                        self.gameOn = True
                        self.message.config(text = "Choose a column")
                        if self.winsFor(self.opp):
                            self.message.config(text = "Yellow Wins!")
                            self.gameOn = False #turns game off so player cannot move after ai wins
                    elif self.isFull():
                        self.message.config(text = "Its a tie!")
                        self.gameOn = False


    '''newGame() clears the game state and initilizes the AI player based on the given plyValue,
    then starts the game and allows the player to begin placing X's.'''
    def newGame(self):
        self.ai = AIPlayer('O','Random', self.plyValue)
        self.gameOn = True
        self.plyslider.config(label= " Difficulty: " + str(self.plyValue))
        self.playerTurn = True
        self.message.config(text="Choose a column!")
        self.clear()
        self.update()
        
        
    '''setply() sets the ply int value from the slider'''
    def setply(self,ply):
        self.plyValue = int(ply)


    '''update() is called after a move is made, iterating through the board 
    filling the circles with their respective colors for X, O or an empty space'''
    def update(self):
        self.circles = []

        y = 10
        for row in range(self.height):
            circleRow = []
            colorRow = []
            x = 15
            for col in range(self.width):
                    circleRow += [self.draw.create_oval(x,y,x+self.diameter,y+self.diameter,fill=self.getNextColor(row,col))]
                    colorRow += [self.initialColor]
                    x += self.diameter + 7

            self.circles+= [circleRow]
            y+= self.diameter + 7
            self.window.update()


    '''getNextColor() returns the respective chip color 
    based on X, O or an empty space on the board data'''
    def getNextColor(self, row, col):
        if self.data[row][col] == "X":
            return "Red"
        elif self.data[row][col] == "O":
            return "Yellow"
        else:
            return self.initialColor


    '''quitGame() is used for quitGame button which closes the window'''
    def quitGame(self):
        self.window.destroy()


    '''clear() resets the game board by replacing every game cell with an empty space'''
    def clear(self):
        for row in range(self.height):
            for col in range(self.width): #iterates through every spot on the gameboard
                self.data[row][col] = ' ' #replaces every spot with an empty space


    '''addMove() adds an O/X to a column if the move is legal using allowsMove function'''
    def addMove(self, col, ox):
        if self.allowsMove(col):
            for row in range(self.height):
                if self.data[row][col] != ' ': #checks to see if column spot has an OX
                    self.data[row-1][col] = ox #places OX above another OX in column
                    return
            self.data[self.height-1][col] = ox


    '''allowsMove() checks for full columns and gameboard width boundaries'''
    def allowsMove(self, col):
        if 0 <= col < self.width: #Checks if move is within boundaries
            return self.data[0][col] == ' ' #returns True if top row is not full
        else:
            return False #returns falls is column is full


    '''delMove() removes the last OX placed in the given column'''
    def delMove(self, col):
            for row in range(self.height):
                if self.data[row][col] != ' ':
                    self.data[row][col] = ' '
                    return


    '''isFull() checks for full gameboard resulting in a tie'''
    def isFull(self):
        for row in range(self.width):
            if self.allowsMove(row): #checks if every top row is full
                return False
        return True


    '''winsFor() checks horizontal, vertical & diagonal win conditions for the given ox'''
    def winsFor(self, ox):
        for row in range(0,self.height):
            for col in range(0,self.width-3): #Checks for horizontal Win
                if self.data[row][col] == ox and \
                self.data[row][col+1] == ox and \
                self.data[row][col+2] == ox and \
                self.data[row][col+3] == ox:
                    return True
        for row in range(0,self.height-3):
            for col in range(0,self.width): #Checks for vertical win
                if self.data[row][col] == ox and \
                self.data[row+1][col] == ox and \
                self.data[row+2][col] == ox and \
                self.data[row+3][col] == ox:
                    return True
        for row in range(0,self.height-3):
            for col in range(0,self.width-3): #Checks for NW->SE diagonal win
                if self.data[row][col] == ox and \
                self.data[row+1][col+1] == ox and \
                self.data[row+2][col+2] == ox and \
                self.data[row+3][col+3] == ox:
                    return True
        for row in range(0,self.height-3): #Checks for SW->NE diagonal win
            for col in range(3,self.width):
                if self.data[row][col] == ox and \
                self.data[row+1][col-1] == ox and \
                self.data[row+2][col-2] == ox and \
                self.data[row+3][col-3] == ox:
                    return True
        return False


def main():
    window = Tk()
    window.title('Connect4')
    Connect4(7,6, window)
    window.mainloop()
if __name__ == '__main__':
    main()
