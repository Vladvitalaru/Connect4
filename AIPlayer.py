import random


class AIPlayer:
    '''Initialization of the aiPlayer class's OX type, tiebreaker rules and difficulty level'''
    def __init__(self, ox, tbt, ply):
        self.ox = ox    #OX type
        self.tbt = tbt  #tie breaker rules
        self.ply = ply  #difficulty level

    '''opposite() returns the opposite OX value given an OX value'''
    def opposite(self, ox):
        if ox == "O":
            return "X" #returns X if ox is O
        else:
            return "O" #returns O if ox is not O

    '''scoreBoard() reads the board state and returns a score based on if 
    there is win condition for your OX or opponents OX'''
    def scoreBoard(self, ox, b):
        if b.winsFor(ox): #returns 100 if given Ox has won
            return 100
        if b.winsFor(self.opposite(ox)): #returns 0 if opposite OX has won
            return 0
        return 50 #returns 50 for every other move

    '''scoresFor() is a recursive function which uses the ply parameter to determine 
    how many moves the AI will look ahead and analyze the best move it can make'''
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

    '''nextMove() chooses the max value in a list of next move 
     and returns the corresponding column integer'''
    def nextMove(self, b):
        L = self.scoresFor(b, self.ox, 0)
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

