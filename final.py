#Vlad Vitalaru
#Final
#cs 121
from tkinter import *
import random

class Player:
    '''Initialization of the aiPlayer class, establishes different attributes
    like OX, tiebreaker rules and dificulty level'''
    def __init__(self, ox, tbt, ply):
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    '''This function returns the opposite ox value given one of the ox values'''
    def opposite(self, ox):
        if ox == "O":
            return "X" #returns X if ox is O
        else:
            return "O" #returns O if ox is not O

    '''scoreBoard analysis a connect4 board and scores it based on if there is 4 in
    a row for your OX or the opponents OX'''
    def scoreBoard(self, ox, b):
        if b.winsFor(ox): #returns 100 if given Ox has won
            return 100
        if b.winsFor(self.opposite(ox)): #returns 0 if opposite OX has won
            return 0
        return 50 #returns 50 for every other move

    '''This is a recursive function that goes into multiple layers of recursion in
    order for the AI player to look ahead and analyze the best move it can make and
    how to counter opponent victory moves'''
    def scoresFor(self, b, ox, ply):
        L = []
        if ply == self.ply: #base case is reached by adding ply values from 0 until reaching given ply
            for col in range(b.width):
                if b.allowsMove(col) == False:
                    L.append(-1)
                else:
                    L.append(self.scoreBoard(ox,b))
            return L #Returns a scored board once reaching base case

        for col in range(b.width): #itteration throughout the collumns
            if b.allowsMove(col) == False:
                L.append(-1) #appends -1 to L if row is filled
            else:
                b.addMove(col,ox) #adds a move for every possible legal move
                if b.winsFor(ox):
                    L.append(100)
                else: #recursion that flips the OX every call, flipping perspective
                    L.append(100 - max(self.scoresFor(b, self.opposite(ox), ply+1)))
                b.delMove(col) #deletes the move after scored value returned
        print(L)
        return L #returns final list with a board score for each column move

    '''nextMove chooses the best (max) value in a list of next move posibilies
     and returns the corresponding column interger'''
    def nextMove(self, b):
        L = self.scoresFor(b, self.ox, 0)
        #Uses scoresfor to obtain a list of
        index = [] #list with the index values of the max scores from scoresFor
        big = max(L)
        for i in range(len(L)): #iterates through scoresFor List
            if L[i] == big: #if the index is equal to the max value, append it to our index list
                index.append(i)
        if self.tbt == "Left":
            return index[0] #if tiebreaker is "Left" return the first value from index
        if self.tbt == "Right":
            return index[-1] #if tiebreaker is "Right" return the last value from index
        if self.tbt == "Random":
            return random.choice(index) #if tiebreaker is "Random" return random value from index



class Connect4:
    '''Initialization of class Connect4's dimensions and board'''
    def __init__(self, width, height, window):
        self.width = width
        self.height = height
        self.data = []

        self.gameOn = False
        self.playerTurn = False
        self.ai = None
        self.plyValue = 0
        self.ox = "X"
        self.opp = "O"

        self.window = window
        self.frame = Frame(window, bg = "DodgerBlue2")
        self.frame.pack(fill = BOTH, expand = True)
        self.messageSize = 25
        self.diameter = 70
        self.initialColor = 'snow'
        self.CanvasHeight = 480
        self.CanvasWidth = 560
        
        self.quitButton = Button(self.frame, text='Quit', command=self.quitGame, bg = "Red", font = "Helvetica 15")
        self.quitButton.pack(side=LEFT, ipady = 10, ipadx = 10, padx = 3)

        self.newGameButton = Button(self.frame, text = "New Game", bg = "DodgerBlue2", command=self.NewGame, font = "Helvetica")
        self.newGameButton.pack(side=RIGHT, padx=3)

        self.draw = Canvas(window, height=self.CanvasHeight, width=self.CanvasWidth, bg = "DodgerBlue2",
        highlightbackground = "DodgerBlue2")
        self.draw.bind('<Button-1>', self.mouseInput)
        self.draw.pack(fill = BOTH, expand = True)

        self.plyslider = Scale(self.frame, from_=0, to=5, orient = HORIZONTAL, bg = "DodgerBlue2",
        label = "Dificulty", troughcolor = "Red",length = 150, highlightbackground = "DodgerBlue2",
        cursor = "arrow", activebackground = "DodgerBlue2", fg = "White", command = self.setply, font = "Helvetica 15")
        self.plyslider.pack(side = LEFT )

        self.message = Label(text='Choose a dificulty level!',bg="DodgerBlue2",fg="White", font='Helvetica 35')
        self.message.pack(fill=X)

        for row in range(height): #6
            boardRow = []
            for col in range(width): #7
                boardRow += [' ']
            self.data += [boardRow] #creating the 2d gameboard
        self.Update()

    '''setply obtains a ply value from the slider and changed the type to an int'''
    def setply(self,ply):
        self.plyValue = int(ply)

    '''New game initilizes the AI player based on the plyValue given from the plyslider,
    then it turns the game on and allows the player to click which places an X, it also clears
    the board and replaces every circle with the initial color'''
    def NewGame(self):
        self.ai = Player('O','Random', self.plyValue)
        self.gameOn = True
        self.playerTurn = True
        self.message.config(text="Choose a column!")
        self.clear()
        self.Update()

    '''Update is called everytime a move is made, it iterates through the board and
    fills the circles with their respective colors for X and O, and also fills the
    initial color when an empty space is found'''
    def Update(self):
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

    '''Mouseinput puts the game together, if the game is on it allows the player to make a move,
    then turns the game off and playerTurn off until the AI has made a move then turns it back on allowing
    the player to go again, once someone wins/theres a tie, the game ends and no clicks can be made after'''
    def mouseInput(self, event):
        #self.window.bell()
        if self.gameOn == True:
            col = int(event.x/80)
            if self.playerTurn == True: #If playerTurn is True, it allows the player to make a move
                if self.allowsMove(col):
                    self.addMove(col,self.ox)
                    self.message.config(text = "AI Thinking...")
                    self.playerTurn = False #switches player turn to false, not allowing player to play until ai has placed a move
                    self.gameOn = False #turns game off, not allowing player to spam 2 quick moves before ai can move
                    self.Update()
                    if self.winsFor(self.ox):
                        self.message.config(text = "Red Wins!")
                        self.playerTurn = True  #after player wins, switches playerturn to ON, not allowing ai to place a move after
                    if self.playerTurn == False:
                        oMove = self.ai.nextMove(self) #calls nextMove from the PLayer class
                        self.addMove(oMove,self.opp)
                        self.Update()
                        self.playerTurn = True #after ai has moved, player may now place another move
                        self.gameOn = True
                        self.message.config(text = "Choose a column")
                        if self.winsFor(self.opp):
                            self.message.config(text = "Yellow Wins!")
                            self.gameOn = False #turns game off so player cannot move after ai wins
                    if self.isFull():
                        self.message.config(text = "Its a tie!")
                        self.gameOn = False

    '''Function that returns the respective color for the circle fill based on X, O or
    a space on the board data'''
    def getNextColor(self, row, col):
        if self.data[row][col] == "X":
            return "Red"
        if self.data[row][col] == "O":
            return "Yellow"
        else:
            return self.initialColor

    '''Simple function that closes the window, used for quitGame button'''
    def quitGame(self):
        self.window.destroy()

    '''Represents an object in the terminal, creates the skeleton of the game board'''
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

    '''Simple function that clears game  by replacing evey spot with a space'''
    def clear(self):
        for row in range(self.height):
            for col in range(self.width): #iterates through every spot on the gameboard
                self.data[row][col] = ' ' #replaces every spot with an empty space

    '''Adds an OX to a column if the move is legal using allowsMove function'''
    def addMove(self,col,ox):
        if self.allowsMove(col):
            for row in range(self.height):
                if self.data[row][col] != ' ': #checks to see if column spot has an OX
                    self.data[row-1][col] = ox #places OX above another OX in column
                    return
            self.data[self.height-1][col] = ox

    '''Function that assists addMove by checking if a move is within boundaries and
    if the column is not filled'''
    def allowsMove(self,col):
        if 0 <= col < self.width: #Checks if move is within boundaries
            return self.data[0][col] == ' ' #returns True if top row is not full
        else:
            return False #returns falls is column is full

    '''Checks column for OX and removes the last OX placed in that column'''
    def delMove(self,col):
            for row in range(self.height):
                if self.data[row][col] != ' ':
                    self.data[row][col] = ' '
                    return

    '''Function that uses allowsMove to check if all the columns are filled,
    resulting in  tie game'''
    def isFull(self):
        for row in range(self.width):
            if self.allowsMove(row): #checks if every top row is full
                return False
        return True

    '''Function that checks all win conditions, horizontal, vertical and diagonal'''
    def winsFor(self,ox):
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

    '''Main function that puts Connect4 Game together using all of its helper functions
    within a while loop'''
    def hostGame(self):
        Count = 0
        while True:
            print(self)
            opp = (Count % 2) #opp alternates between 1 and 0 for switching turns
            odd = 1
            even = 0
            if opp == even: #Alternates between X and O turns
                OX = "X"
            else:
                OX = "O"
            print("Pick a Row")
            ox = int(input())
            if self.allowsMove(ox): #If move is legal, add it to the column
                self.addMove(ox,OX)
            else:
                while True: #loop that doesnt switch OX turn until a legal move is made
                    print("You cant do that! Try again")
                    ox = int(input()) #takes a new column input (hopefully a legal one this time)
                    print(self)
                    if self.allowsMove(ox):
                        self.addMove(ox,OX)
                        break
            if self.winsFor(OX): #If win condition is met, print which player won
                if OX == "X":
                    print("X Won!")
                if OX == "O":
                    print("O Won!")
                print(self)
                print("Play again? Y or N")
                choice = str(input()) #askes to play again, and takes a user input
                if choice in "Yy": #starts a new game if input is y or Y
                    self.clear()
                    self.hostGame()
                    return
                if choice in "Nn": #breaks game loop if input is n or N
                    return False
                else: #if anything else besides Yy or Nn is inputted, program will stop
                    break
            if self.isFull(): #If the top row has all columns filled, its a tie
                print(self)
                print("It's a Tie!")
                break
            Count = Count + 1
            print(Count)

    def playGameWith(self,aiPlayer):
        Count = 0
        while True:
            print(self)
            opp = (Count % 2) #opp alternates between 1 and 0 for switching turns
            odd = 1
            even = 0
            if opp == even: #Alternates between X and O turns
                OX = "X"
            else:
                OX = "O"
            if opp == even:
                print("Pick a Row")
                ox = int(input())
                if self.allowsMove(ox):
                    self.addMove(ox,OX)
                else:
                    while True: #loop that doesnt switch OX turn until a legal move is made
                        print("You cant do that! Try again")
                        ox = int(input()) #takes a new column input (hopefully a legal one this time)
                        print(self)
                        if self.allowsMove(ox):
                            self.addMove(ox,OX)
                            break
                if self.winsFor(OX):
                    if OX == "X":
                        print("X Won!")
                    if OX == "O":
                        print("O Won!")
                    print(self)
                    print("Play again? Y or N")
                    choice = str(input()) #askes to play again, and takes a user input
                    if choice in "Yy": #starts a new game if input is y or Y
                        self.clear()
                        self.playGameWith(aiPlayer)
                        return
                    if choice in "Nn": #breaks game loop if input is n or N
                        return False
                    else: #if anything else besides Yy or Nn is inputted, program will stop
                        break
                if self.isFull(): #If the top row has all columns filled, its a tie
                    print(self)
                    print("It's a Tie!")
                    break
            oMove = aiPlayer.nextMove(self)
    #creating a variable that calls nextmove using the object from Player class that is being passed through "aiPlayer"
            if opp == odd:
                self.addMove(oMove,OX) #passing oMove to obtain the nextMove col number for the AI add move
            if self.winsFor(OX):
                print("Computer wins!")
                print(self)
                print("Play again? Y or N")
                choice = str(input()) #askes to play again, and takes a user input
                if choice in "Yy": #starts a new game if input is y or Y
                    self.clear()
                    self.playGameWith(aiPlayer)
                    return
                if choice in "Nn": #breaks game loop if input is n or N
                    return False
                else: #if anything else besides Yy or Nn is inputted, program will stop
                    break
            if self.isFull(): #if gameboard is full, game ends with a tie
                print("It's a tie!")
                break
            Count = Count + 1 #adds a count everyturn in order to alternate turns

def main():
    window = Tk()
    window.title('Connect4')
    board = Connect4(7,6, window)
    window.mainloop()
if __name__ == '__main__':
    main()
