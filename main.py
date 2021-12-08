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

class Color(Enum):
    WHITE = 1
    BLACK = 2

class Piece:
    letter = "" # P for pawn, N for Knight, B for Bishop, R for Rook, Q for Queen, K for King

    def __init__(self, Color, Type):
        self.Color = Color
        self.Type = Type
        hasMoved = False

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

class Square:
    isEmpty = True

    def __init__(self, id, Color):
        self.id = id  # integers, 0 - 63
        self.Color = Color  # white, black
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
    def __init__(self):
        print("Initiating board...")
        # populate board with 64 squares
        for x in range(64):
            if isEven(x):
                self.squares.append(Square(x, "WHITE"))
            elif not isEven(x):
                self.squares.append(Square(x, "BLACK"))


    def move(self, sourcePiece, destinationSquare):
        print("Attempting to move piece " + str(sourcePiece) + " to " + str(destinationSquare))
        # validate the move


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

board = Board()
board.move("a1", "a2")


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
        contentsString = str(str(piece.Color)[0:2] + " " + piece.Type)
    print(str(square.id).rjust(2) + ":", end="")    # FIXME: replace id with coords
    print(str(contentsString).center(squareWidth, "-"), end=" ")

    # problem: id 8 is shorter than id 18


def getPlayerMove(Color):
    print(str(Color) + " to move: [src dest]")
    input("> ")


    # tryMove()

# def getStringOfLength(string, length):

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
            getPlayerMove("WHITE")
            whiteToMove = False
        else:
            getPlayerMove("BLACK")
            whiteToMove = True

print("test".center(10, "*"))
print("testing".center(10, "*"))

board = Board()
# board.squares[0].addPiece(Piece("White", "ROOK"))   # placing a white rook on a1, square 0, for testing purposes

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



# # pygame GUI
# pygame.init()
#
# white = (255,255,255)
# black = (0,0,0)
#
# red = (255,0,0)
# green = (0,255,0)
# blue = (0,0,255)
#
# gameDisplay = pygame.display.set_mode((800,600))
# gameDisplay.fill(black)
#
# pygame.draw.rect(gameDisplay, green, (400,400,50,25))   # where to draw, what color, top right X and Y, width, height
# pygame.draw.rect(gameDisplay, white, (500,500,50,25))
# pygame.draw.rect(gameDisplay, white, (0,50,100,100))
#
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
#
#     pygame.display.update()