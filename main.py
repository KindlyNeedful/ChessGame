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
    letter = ""  # P for pawn, N for Knight, B for Bishop, R for Rook, Q for Queen, K for King

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
    x = 0
    y = 0

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
            # if isEven(x):
            #     print("Creating square " + str(x) + ", White")
            #     self.squares.append(Square(x, "White"))
            # elif not isEven(x):
            #     print("Creating square " + str(x) + ", Black")
            #     self.squares.append(Square(x, "Black"))
            if isEven (x // 8):
                if isEven(x):
                    color = "Black"
                elif not isEven(x):
                    color = "White"
            elif not isEven (x // 8):
                if isEven(x):
                    color = "White"
                elif not isEven(x):
                    color = "Black"

            print("Creating square " + str(x) + ", color " + str(color))
            self.squares.append(Square(x, color))


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

whiteAtBottom = True  # which way to orient the board.


def printBoard():
    print("")
    if whiteAtBottom:
        for x in range(8, 0, -1):
            printRow(x)
    elif not whiteAtBottom:
        for x in range(1, 9):
            printRow(x)
    print("")


def printRow(rowNum):
    for x in range(8):
        printSquare(board.squares[x + 8 * (rowNum - 1)])
    print("\n")


squareWidth = 12


def printSquare(square):
    # print(square.id, end=" ")

    if square.isEmpty:
        contentsString = ""
    else:
        piece = square.getContents()
        contentsString = str(str(piece.getColor())[0:2] + " " + piece.Type)
    print(str(square.id).rjust(2) + ":", end="")  # FIXME: replace id with coords
    print(str(contentsString).center(squareWidth, "-"), end=" ")

    # problem: id 8 is shorter than id 18


def playerOffersDraw(color):
    print("Player " + color + " is offering a draw.")
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
        print(color + " has resigned!")
        # display victory screen
        startGame()
    else:
        try:
            src = playerInput.split(",")[0]
            dest = playerInput.split(",")[1]

            print("Trying move: " + str(src) + "," + str(dest))
            if validateMove(src, dest, color):
                move(src, dest)
            else:
                getPlayerMove(color)
        except ValueError:
            print("Invalid input.")
            getPlayerMove(color)

    # else:     # FIXME - rework input validation
    #     print("Invalid input.")
    #     getPlayerMove(color)


# src, dest square ids #FIXME - changing this to pass the squares in directly.
# ONLY returns true/false whether a move is valid, does not actually move anything
def validateMove(src, dest, playerColor):
    # if the player is black, modifier = -1. If white, modifier = 1.
    blackModifier = 1
    if playerColor == "Black":
        blackModifier = -1

    # print("validateMove(" + str(src.id) + ", " + str(dest.id) + ", " + str(playerColor) + ")...")
    # src = board.getSquare(src)
    # dest = board.getSquare(dest)
    # ERROR: it's parsing input src,dest as strings.    # implemented board.getSquares() - good.

    # list all the conditions in which this is an invalid move.
    # unless all conditions are met, return False.

    # if there is no piece in the src square
    if (src.isEmpty):
        print("Invalid move: src is empty.")
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
    if piece.Type == "ROOK":

        # move must be within the same rank
        if src.id // 8 == dest.id // 8:
            if pathIsClear(src, dest):
                return True
            else:
                return False
        # or within the same file
        elif src.id % 8 == dest.id % 8:
            if pathIsClear(src, dest):
                return True
            else:
                return False


         # move must not skip over any pieces
        else:
            return False

    # knight rules
    validMoveDiffs = [17, 10, 6, 15]
    if piece.Type == "KNIGHT":
        if dest.id - src.id in validMoveDiffs:
            return True

    # bishop rules
    if piece.Type == "BISHOP":
        # if moveIsDiagonal(src, dest):
        #     print("bishop: move is diagonal.")
        #     return True
        # print("src.x/squareSize: " + str(src.x/squareSize) +", src.y/squareSize: " + str(src.y/squareSize))
        # print("dest.x/squareSize: " + str(dest.x/squareSize) + ", dest.y/squareSize: " + str(dest.y/squareSize))
        # print("src.x - dest.x: " + str(src.x - dest.x))
        # print("src.y - dest.y: " + str(src.y - dest.y))

        if abs(src.x - dest.x) == abs(src.y - dest.y):
            print("move valid.")
            if pathIsClear(src, dest):
                return True


    # queen rules

    # king rules

    return False
    return True

def moveIsDiagonal(src, dest):
    print("Checking whether move is diagonal: " + str(src.id) + ", " + str(dest.id))
    if (src.id - dest.id) % 9 == 0 or (src.id - dest.id) % 7 == 0:
        return True
    else:
        return False

def pathIsClear(src, dest):
    # returns True if a proposed move does not skip over any pieces
    print("pathIsClear(): checking whether move skips any pieces: " + str(src.id) + ", " + str(dest.id) + "\n\t", end="")
    piecesInPath = 0

    # horizontal moves
    if src.id // 8 == dest.id // 8:
        print("Horizontal move detected.")
        for x in range(src.id + 1, dest.id):
            # print(str(x), end=", ")
            square = board.getSquare(str(x))

            if square.isEmpty:
                print("Square " + str(x) + " is empty.")
            if not square.isEmpty:
                print("Square " + str(x) + " is not empty.")
                piecesInPath += 1

    # vertical moves
    if src.id % 8 == dest.id % 8:
        print("Vertical move detected.")
        # for every number between src and dest whose %8 is the same.

        modifier = 1
        if src.id > dest.id:
            modifier = -1
        for x in range(src.id + 8 * modifier, dest.id, 8 * modifier):
            print(str(x))
            square = board.getSquare(str(x))

            if square.isEmpty:
                print("Square " + str(x) + " is empty.")
            if not square.isEmpty:
                print("Square " + str(x) + " is not empty.")
                piecesInPath += 1

    # diagonal moves
    if abs(src.x - dest.x) == abs(src.y - dest.y):
        print("Diagonal move detected.")


        # positive sloped lines
        if dest.x > src.x and dest.y < src.y or dest.x < src.x and dest.y > src.y:
            print("positive slope detected")
            slopeIsPositive = True

        # negative sloped lines
        if dest.x > src.x and dest.y > src.y or dest.x < src.x and dest.y < src.y:
            print("negative slope detected")
            slopeIsPositive = False

        if slopeIsPositive:
            diff = 9
        elif not slopeIsPositive:
            diff = 7

        if dest.id > src.id:
            for x in range(src.id + diff, dest.id, diff):
                print(str(x))
                if not board.getSquare(str(x)).isEmpty:
                    piecesInPath += 1
        elif dest.id < src.id:
            for x in range(src.id - diff, dest.id, -diff):
                print(str(x))
                if not board.getSquare(str(x)).isEmpty:
                    piecesInPath += 1

    print("Pieces in path: " + str(piecesInPath))
    if piecesInPath == 0:
        return True
    else:
        return False

def move(src, dest):
    # takes src and dest squares. Only runs after the move has been validated.
    # src = board.getSquare(src)
    # dest = board.getSquare(dest)
    print("Moving piece from " + str(src.id) + " to " + str(dest.id))
    # print(src)
    # print(dest)

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
    playerVictory = None  # will be set to WHITE or BLACK upon victory
    while playerVictory == None and stalemate == False:
        printBoard()
        if whiteToMove:
            getPlayerMove("White")
            whiteToMove = False
        else:
            getPlayerMove("Black")
            whiteToMove = True


# print("test".center(10, "*"))
# print("testing".center(10, "*"))


def startGame():
    # board = Board()
    # FIXME - may need to clear contents from previous game
    populateBoard()
    gameLoop()


# pygame GUI
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
# custom colors
backgroundColor = (60, 70, 90)
squareColorLight = (235, 235, 208)
squareColorDark = (118, 148, 85)
lightTextColor = (245, 245, 245)
borderColor = (40, 40, 40)

# defines height/width of the squares
squareSize = 75

# define gameDisplay window size
# gameDisplay = pygame.display.set_mode((800,600))
gameDisplay = pygame.display.set_mode((12 * squareSize, 10 * squareSize))

gameDisplay.fill(backgroundColor)
# pygame.draw.rect(gameDisplay, green, (400,400,50,25))   # where to draw, what color, top left X and Y, width, height
# pygame.draw.rect(gameDisplay, white, (500,500,50,25))


# pygame.draw.rect(gameDisplay, squareColorLight, (0,0,squareSize,squareSize))

# for x in range(0,8):
#     pygame.draw.rect(gameDisplay, squareColorLight, (squareSize * x, squareSize * x, squareSize, squareSize))


# draw chessboard
def drawBoard():
    for x in range(0, 8):

        for y in range(0, 8):
            if isEven(x + y):
                color = squareColorLight
            else:
                color = squareColorDark

            pygame.draw.rect(gameDisplay, color, (squareSize * y, squareSize * x, squareSize, squareSize))
drawBoard()

fontSize = 24
font = pygame.font.SysFont(None, fontSize)
def drawLabels():
    # draw square labels

    #img = font.render('a', True, lightTextColor)

    characterString = "abcdefgh"
    labelOffsetX = squareSize / 2
    for x in range(8):
        gameDisplay.blit(font.render(characterString[x], True, lightTextColor),
                         (labelOffsetX + squareSize * x, squareSize * 8.1))

    numberString = "12345678"
    for x in range(8):
        gameDisplay.blit(font.render(numberString[7 - x], True, lightTextColor),
                         (squareSize * 8.1, labelOffsetX + squareSize * x))

    gameDisplay.blit(font.render("White to move", True, lightTextColor),
                     (squareSize * 9, squareSize / 2))

drawLabels()

def updateLabels():
    if whiteToMove:
        text = "White to move"
    elif not whiteToMove:
        text = "Black to move"

    pygame.draw.rect(gameDisplay, backgroundColor, (squareSize * 9, squareSize / 2, squareSize * 2, squareSize))
    gameDisplay.blit(font.render(text, True, lightTextColor),
                     (squareSize * 9, squareSize / 2))

# # render testing images
# whitePawnImg = pygame.image.load('whitePawn.png')
# whitePawnImg = pygame.transform.scale(whitePawnImg, (squareSize, squareSize))
# # gameDisplay.blit(whitePawnImg, (0, 0))
#
# gameDisplay.blit(whitePawnImg, (4 * squareSize, 6 * squareSize))

# main game loop
board = Board()
populateBoard()
# move("a1", "a2", "")
# startGame()

# render initial pieces
# print(str(board.getSquare("0").g))
# print("square 0 contents: " + str(board.getSquare("0").getContents().getType()) + " " + str(
#     board.getSquare("0").getContents().getColor()))

def giveSquaresCoords():
# assign x and y coord values to each squares. Square 0, a1, starts in the bottom left.
    for square in board.squares:
        # print("id: " + str(square.id), end="\t")
        square.x = (square.id % 8) * squareSize
        square.y = (7 * squareSize) - ((square.id // 8) * squareSize)  # FIXME

        # print("x: " + str(square.x), end="\t")
        # print("y: " + str(square.y))
giveSquaresCoords()


def getPieceImg(pieceColor, pieceType):
    if pieceColor == None or pieceType == None:
        return None
    elif pieceColor == "White":
        if pieceType == "ROOK":
            return pygame.transform.scale(pygame.image.load('whiteRook.png'), (squareSize, squareSize))
        elif pieceType == "KNIGHT":
            return pygame.transform.scale(pygame.image.load('whiteKnight.png'), (squareSize, squareSize))
        elif pieceType == "BISHOP":
            return pygame.transform.scale(pygame.image.load('whiteBishop.png'), (squareSize, squareSize))
        elif pieceType == "QUEEN":
            return pygame.transform.scale(pygame.image.load('whiteQueen.png'), (squareSize, squareSize))
        elif pieceType == "KING":
            return pygame.transform.scale(pygame.image.load('whiteKing.png'), (squareSize, squareSize))
        elif pieceType == "PAWN":
            return pygame.transform.scale(pygame.image.load('whitePawn.png'), (squareSize, squareSize))
    elif pieceColor == "Black":
        if pieceType == "ROOK":
            return pygame.transform.scale(pygame.image.load('blackRook.png'), (squareSize, squareSize))
        elif pieceType == "KNIGHT":
            return pygame.transform.scale(pygame.image.load('blackKnight.png'), (squareSize, squareSize))
        elif pieceType == "BISHOP":
            return pygame.transform.scale(pygame.image.load('blackBishop.png'), (squareSize, squareSize))
        elif pieceType == "QUEEN":
            return pygame.transform.scale(pygame.image.load('blackQueen.png'), (squareSize, squareSize))
        elif pieceType == "KING":
            return pygame.transform.scale(pygame.image.load('blackKing.png'), (squareSize, squareSize))
        elif pieceType == "PAWN":
            return pygame.transform.scale(pygame.image.load('blackPawn.png'), (squareSize, squareSize))


def renderPieces():
    # print("Rendering pieces...")
    for square in board.squares:
        # print("Rendering square id " + str(square.id), end='\t')

        if square.isEmpty:
            # pieceImg = pygame.transform.scale(pygame.image.load('noPiece.png'), (squareSize, squareSize))
            # gameDisplay.blit(pieceImg, (square.x, square.y))
            #
            # continue
            # print("Square " + str(square.id) + " is empty. Color should be " + str(square.color))
            # if isEven(square.id):
            #     color = squareColorDark
            # else:
            #     color = squareColorLight
            if square.color == 'Black':
                color = squareColorDark
            else:
                color = squareColorLight

            #pygame.draw.rect(gameDisplay, color, (squareSize * y, squareSize * x, squareSize, squareSize))
            pygame.draw.rect(gameDisplay, color, (square.x, square.y, squareSize, squareSize))
        else:
            pieceImg = getPieceImg(square.getContents().getColor(), square.getContents().getType())
            # print("pieceImg: " + str(pieceImg))
            # print("coords: " + str(square.x) + ", " + str(square.y))
            gameDisplay.blit(pieceImg, (square.x, square.y))


renderPieces()


def getSquare(xCoord, yCoord):
    # this function returns the square containing the provided x and y coords.
    for square in board.squares:
        if xCoord >= square.x and xCoord < square.x + squareSize:
            if yCoord >= square.y and yCoord < square.y + squareSize:
                return square
    else:
        return None

# starting coords for the chessboard
xOrigin = 0
yOrigin = 0


def clickIsOnBoard(coords):
    xCoord = coords[0]
    yCoord = coords[1]
    if xCoord >= xOrigin and xCoord <= xOrigin + 8 * squareSize:
        if yCoord >= yOrigin and yCoord <= yOrigin + 8 * squareSize:
            return True
    else:
        return False


whiteToMove = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # FIXME: need ability to read current player move
        # src = None
        # dest = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if clickIsOnBoard(pos):
                src = getSquare(pos[0], pos[1])

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if clickIsOnBoard(pos):
                dest = getSquare(pos[0], pos[1])

                if whiteToMove:
                    if validateMove(src, dest, 'White'):
                        move(src, dest)
                        whiteToMove = False

                else:
                    if validateMove(src, dest, 'Black'):
                        move(src, dest)
                        whiteToMove = True
            drawBoard()
            renderPieces()
            pygame.display.flip()
            updateLabels()

    pygame.display.update()
