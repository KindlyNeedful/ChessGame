from enum import Enum
import tkinter as tk
from tkinter import *
import pygame

class Type(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

# class Color(Enum):
#     WHITE = 1
#     BLACK = 2

class Piece:
    letter = "" # P for pawn, N for Knight, B for Bishop, R for Rook, Q for Queen, K for King

    def __init__(self, color, Type):
        self.color = color
        self.Type = Type
        self.hasMoved = False

        if self.Type == "PAWN":
            self.letter = "P"
        if self.Type == "KNIGHT":
            self.letter = "N"
        if self.Type == "BISHOP":
            self.letter = "B"
        if self.Type == "ROOK":
            self.letter = "R"
        if self.Type == "QUEEN":
            self.letter = "Q"
        if self.Type == "KING":
            self.letter = "K"

    def getColor(self):
        return self.color

    def getType(self):
        return self.Type

class Square:
    isEmpty = True

    def __init__(self, id, color):
        self.id = id  # integers, 0 - 63
        self.color = color  # white, black
        self.contents = None

    def getContents(self):
        if self.contents == None:
            return None
        else:
            return self.contents


    def addPiece(self, Piece):
        self.contents = Piece
        self.isEmpty = False

    def removePiece(self):
        self.contents = None
        self.isEmpty = True


class Board:
    squares = []
    capturedPieces = []
    def __init__(self):
        print("Initiating board...")
        # populate board with 64 squares
        for x in range(64):
            if isEven(x):
                self.squares.append(Square(x, "White"))
            elif not isEven(x):
                self.squares.append(Square(x, "Black"))

    # # takes src and dest squares. Only runs after the move has been validated.
    # def move(self, src, dest):
    #     print("Moving piece from " + str(src) + " to " + str(dest))
    #     src = self.getSquare(src)
    #     dest = self.getSquare(dest)
    #     print(src)
    #     print(dest)
    #
    #     dest.addPiece(src.getContents)
    #     src.removePiece()

    def getSquare(self, squareString):
        for x in self.squares:
            if str(x.id) == squareString:
                return x



def isEven(num):
    if (num % 2) == 0:
        return True
    else:
        return False

squareNames = {}


def buttonOtb_clickHandler():
    print("OTB button clicked.")

def buttonQuit_clickHandler():
    print("Closing application.")
    gui.destroy()


################




# print(str(len(board.squares)))
# for x in range (64):
#     print(board.squares[x].id)

whiteAtBottom = True    # which way to orient the board.
def printBoard():
    print("")
    if whiteAtBottom:
        for x in range (8, 0, -1):
            printRow(x)
    elif not whiteAtBottom:
        for x in range (1, 9):
            printRow(x)
    print("")

def printRow(rowNum):
    for x in range (8):
        printSquare(board.squares[x + 8 * (rowNum - 1)])
    print ("\n")

squareWidth = 12
def printSquare(square):
    #print(square.id, end=" ")

    if square.isEmpty:
        contentsString = ""
    else:
        piece = square.getContents()
        contentsString = str(str(piece.getColor())[0:2] + " " + piece.Type)
    print(str(square.id).rjust(2) + ":", end="")    # FIXME: replace id with coords
    print(str(contentsString).center(squareWidth, "-"), end=" ")

    # problem: id 8 is shorter than id 18

def playerOffersDraw(color):
    print ("Player " + color + " is offering a draw.")
    if color == "White":
        print("Black, ", end="")
    else:
        print("White, ", end="")
    print("do you accept? [y | n]")
    playerInput = input("> ")
    if playerInput == "y":
        print("The game has ended in a draw.")
        startGame()


def getPlayerMove(color):
    print(str(color) + " to move: [src,dest | d - offer draw | r - resign]")
    playerInput = input("> ")

    if playerInput == "d":
        playerOffersDraw(color)
    elif playerInput == "r":
        print (color + " has resigned!")
        # display victory screen
        startGame()
    else:
        try:
            src = playerInput.split(",")[0]
            dest = playerInput.split(",")[1]

            print("Trying move: " + str(src) + "," + str(dest))
            if validateMove(src,dest, color):
                move(src,dest)
            else:
                getPlayerMove(color)
        except ValueError:
            print("Invalid input.")
            getPlayerMove(color)

    # else:     # FIXME - rework input validation
    #     print("Invalid input.")
    #     getPlayerMove(color)


# src, dest square ids
# ONLY returns true/false whether a move is valid, does not actually move anything
def validateMove(src, dest, playerColor):
    print("tryMove(" + str(src) + ", " + str(dest) + ")...")
    src = board.getSquare(src)
    dest = board.getSquare(dest)
    # ERROR: it's parsing input src,dest as strings.    # implemented board.getSquares() - good.


    # list all the conditions in which this is an invalid move.
    # unless all conditions are met, return False.

    # if there is no piece in the src square
    if (src.isEmpty):
        print ("Invalid move: src is empty.")
        return False
    else:
        # if the src square contains an enemy piece
        # print(src.getContents().color)
        # print(playerColor)
        if not src.getContents().color == playerColor:
            print("Invalid move: src has an enemy piece.\n")
            return False

        # if the destination square has an allied piece
        if not dest.isEmpty:
            # print(dest.getContents().color)
            # print(playerColor)
            if dest.getContents().color == playerColor:
                print("Invalid move: dest has an allied piece.\n")
                return False

    # piece-specific rules
    # pieceType = src.getContents().getType()
    # print(pieceType)
    piece = src.getContents()

    # pawn rules
    blackModifier = 1
    if playerColor == "Black":
        blackModifier = -1
    if piece.Type == "PAWN":
        # moving without capture
        if dest.isEmpty:
            # move one square forward
            if dest.id == src.id + (blackModifier * 8):
                return True
            # move two squares forward
            elif dest.id == src.id + (blackModifier * 16) and not piece.hasMoved:
                return True
            else:
                print("Invalid move.")
                return False
        elif not dest.isEmpty:
            if dest.id == src.id + (blackModifier * 7) or dest.id == src.id + (blackModifier * 9):
                return True
            # FIXME - add en passant capturing

    # rook rules

    # knight rules
    abc = [17, 10, 6, 15]
    if piece.Type == "KNIGHT":
        if dest.id - src.id in abc:
            return True

    # bishop rules

    # queen rules

    # king rules



    return True


def move(src, dest):
    # takes src and dest squares. Only runs after the move has been validated.
    src = board.getSquare(src)
    dest = board.getSquare(dest)
    print("Moving piece from " + str(src) + " to " + str(dest))
    print(src)
    print(dest)

    # capture
    if not dest.isEmpty:
        print("Piece captured!")
        board.capturedPieces.append(dest.getContents())


    piece = src.getContents()
    dest.addPiece(piece)
    src.removePiece()
    piece.hasMoved = True


def populateBoard():
    board.squares[0].addPiece(Piece("White", "ROOK"))
    board.squares[1].addPiece(Piece("White", "KNIGHT"))
    board.squares[2].addPiece(Piece("White", "BISHOP"))
    board.squares[3].addPiece(Piece("White", "QUEEN"))
    board.squares[4].addPiece(Piece("White", "KING"))
    board.squares[5].addPiece(Piece("White", "BISHOP"))
    board.squares[6].addPiece(Piece("White", "KNIGHT"))
    board.squares[7].addPiece(Piece("White", "ROOK"))
    for x in range(8):
        board.squares[x + 8].addPiece(Piece("White", "PAWN"))

    board.squares[56].addPiece(Piece("Black", "ROOK"))
    board.squares[57].addPiece(Piece("Black", "KNIGHT"))
    board.squares[58].addPiece(Piece("Black", "BISHOP"))
    board.squares[59].addPiece(Piece("Black", "QUEEN"))
    board.squares[60].addPiece(Piece("Black", "KING"))
    board.squares[61].addPiece(Piece("Black", "BISHOP"))
    board.squares[62].addPiece(Piece("Black", "KNIGHT"))
    board.squares[63].addPiece(Piece("Black", "ROOK"))
    for x in range(8):
        board.squares[x + 48].addPiece(Piece("Black", "PAWN"))


def gameLoop():
    # main game loop
    whiteToMove = True
    stalemate = False
    playerVictory = None    # will be set to WHITE or BLACK upon victory
    while playerVictory == None and stalemate == False:
        printBoard()
        if whiteToMove:
            getPlayerMove("White")
            whiteToMove = False
        else:
            getPlayerMove("Black")
            whiteToMove = True

print("test".center(10, "*"))
print("testing".center(10, "*"))



def startGame():
    # board = Board()
    # FIXME - may need to clear contents from previous game
    populateBoard()
    gameLoop()





####

# # tkinter GUI
# gui = tk.Tk()
# gui.geometry("400x200") # defines the size of the window
# #w = tk.Button(master, option=value)
# gui.title('Chess Game')
#
# # buttonOtb = tk.Button(gui, text='Play Over-the-Board', command=buttonClicked()) # note: this calls buttonClicked() when executed.
# buttonOtb = tk.Button(gui, text='Play Over-the-Board', command=buttonOtb_clickHandler) # note: this is what you want.
#
# buttonOtb.pack()
# buttonQuit = tk.Button(gui, text='Quit', command=buttonQuit_clickHandler)
# buttonQuit.pack()
#
# # w = MenuButton(gui)   # unresolved reference. look into this.
#
# canvas = Canvas(gui, width=550, height=820)
# canvas.pack()
# canvas.create_rectangle(0,0,50,50, fill='green') # x1, y1, x2, y2
# # https://stackoverflow.com/questions/42039564/tkinter-canvas-creating-rectangle
#
# gui.mainloop()



# pygame GUI
pygame.init()

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
# custom colors
midGray = (128,128,128)
squareColorLight = (222, 206, 162)
squareColorDark = (70, 99, 65)

# defines height/width of the squares
squareSize = 75

# define gameDisplay window size
# gameDisplay = pygame.display.set_mode((800,600))
gameDisplay = pygame.display.set_mode((8 * squareSize, 8 * squareSize))

gameDisplay.fill(midGray)
#pygame.draw.rect(gameDisplay, green, (400,400,50,25))   # where to draw, what color, top left X and Y, width, height
#pygame.draw.rect(gameDisplay, white, (500,500,50,25))


# pygame.draw.rect(gameDisplay, squareColorLight, (0,0,squareSize,squareSize))

# for x in range(0,8):
#     pygame.draw.rect(gameDisplay, squareColorLight, (squareSize * x, squareSize * x, squareSize, squareSize))


# draw chessboard
# for x in range(0,64):

for x in range(0, 8):

    for y in range(0, 8):
        if isEven(x + y):
            color = squareColorLight
        else:
            color = squareColorDark

        pygame.draw.rect(gameDisplay, color, (squareSize * y, squareSize * x, squareSize, squareSize))





while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()



# main game loop
board = Board()
# move("a1", "a2", "")
startGame()