# TkTetris by Matthew Ponce de Leon

# Adapted from Tetris For Intro/Intermediate programmers tutorial by
# David Kosbie at https://www.cs.cmu.edu/~112n18/notes/notes-tetris/index.html

from tkinter import *
import copy, random

def initPieces(data):
    """
    Stores all types of Tetris pieces and their corresponding colors in data.

    data: struct
    """
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]]

    data.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, 
        zPiece]
    data.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", 
        "green", "orange"]

def init(data):
    """
    Initializes new Tetris game.

    data: struct
    """
    data.margin = 20 # specifies bottom margin left for displaying score
    data.cols, data.rows = 10, 14
    # Cell size based on canvas size nad num of cols
    data.cellSize = data.width / data.cols
    data.emptyColor = 'blue' # background color of grid
    data.board = [[data.emptyColor for col in range(data.cols)] 
        for row in range(data.rows)]
    initPieces(data) # stores diff types of pieces
    data.score = 0
    data.state = 'p'
    data.gameOver = False
    newFallingPiece(data) # generates first falling piece

def newFallingPiece(data):
    """
    Generates a new, random falling piece positioned at the top of the board.

    data: struct
    """
    index = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[index]
    data.fallingPieceColor = data.tetrisPieceColors[index]
    data.fallingPieceRow = 0
    # Sets starting col to middle index minus half of piece width to display
    # the piece in the middle
    data.fallingPieceCol = data.cols // 2 - len(data.fallingPiece[0]) // 2

def fallingPieceIsLegal(data):
    """
    Returns True if the falling piece is in a legal position on the Tetris 
    board, False otherwise.

    data: struct
    """
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            # Tests only for cells part of the falling piece
            if data.fallingPiece[row][col] == True:
                # Checks if row and col are within bounds of board
                if not (0 <= data.fallingPieceRow + row < data.rows and 
                        0 <= data.fallingPieceCol + col < data.cols):
                    return False
                # Checks if falling piece is not overlapping other pieces
                elif data.board[data.fallingPieceRow + row]\
                        [data.fallingPieceCol + col] != data.emptyColor:
                    return False
    return True

def moveFallingPiece(data, drow, dcol):
    """
    Attempts to move a falling Tetris piece in the given directions. Returns 
    True if the move is legal and completed successfully, False otherwise.

    data: struct
    drow: int
    dcol: int
    """
    # Try to move piece as specified by arrow keys
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    # Revert move if at edge of board or hitting other pieces
    if not fallingPieceIsLegal(data):
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True

def rotateFallingPiece(data):
    """
    Rotates given falling piece counterclockwise.

    data: struct
    """
    # Sets temp vars to store attributes of falling piece before rotation
    oldRow, oldCol = data.fallingPieceRow, data.fallingPieceCol
    oldPiece = data.fallingPiece
    oldNRows, oldNCols = len(oldPiece), len(oldPiece[0])
    # New piece swaps number of rows and cols from old piece
    newNRows, newNCols = oldNCols, oldNRows
    # Sets new location of falling piece
    newRow = oldRow + oldNRows // 2 - newNRows // 2
    newCol = oldCol + oldNCols // 2 - newNCols // 2
    newPiece = [[None for col in range(newNCols)] for row in range(newNRows)]
    # Maps boolean values to construct layout of new falling piece
    for row in range(oldNRows):
        for col in range(oldNCols):
            newPiece[oldNCols-1-col][row] = oldPiece[row][col]
    data.fallingPiece = newPiece
    data.fallingPieceRow, data.fallingPieceCol = newRow, newCol
    if not fallingPieceIsLegal(data):
        data.fallingPiece = oldPiece
        data.fallingPieceRow, data.fallingPieceCol = oldRow, oldCol

def removeFullRows(data):
    """
    Redraws board, removing rows that are full. Adds to score when a row is 
    removed.

    data: struct
    """
    newBoard = []
    # Adds old rows that are not full to new board
    for row in range(len(data.board)):
        if data.emptyColor in data.board[row]:
            newBoard.append(data.board[row])
    # Updates score based on full rows removed
    scoreToAdd = len(data.board) - len(newBoard)
    data.score += scoreToAdd
    # Updates board iff full rows were removed
    if scoreToAdd > 0:
        # Inserts empty rows atop old rows until board is original size
        while len(newBoard) < len(data.board):
            newBoard.insert(0, [data.emptyColor for col in range(data.cols)])
        # Replaces old board with new one
        data.board = newBoard

def placeFallingPiece(data):
    """
    Places falling piece in the board at its current indices.

    data: struct
    """
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col]:
                data.board[data.fallingPieceRow + row]\
                    [data.fallingPieceCol + col] = data.fallingPieceColor
    removeFullRows(data)

def mousePressed(event, data):
    """
    Executed on mouseclick.

    event: dict
    data: struct
    """
    pass

def keyPressed(event, data):
    """
    Executed upon keypress.

    event: dict
    data: struct
    """
    if not data.gameOver:
        # Specifies change in row and col of falling piece upon keypress
        drow, dcol = 0, 0
        if event.keysym == 'Right': dcol = 1
        elif event.keysym == 'Left': dcol = -1
        elif event.keysym == 'Down': drow = 1
        # Rotates falling piece CCW if up arrow key is pressed
        elif event.keysym == 'Up': rotateFallingPiece(data)
        # Rotates falling piece CW if right shift is pressed
        elif event.keysym == 'Shift_R':
            # should be in helper func but not enough time to
            # write test cases for it:
            rotateFallingPiece(data)
            rotateFallingPiece(data)
            rotateFallingPiece(data)
        # Moves falling piece to bottom upon hitting enter
        elif event.keysym == 'Return':
            while moveFallingPiece(data, 1, 0): pass
        # Moves falling piece in given direction
        moveFallingPiece(data, drow, dcol)
    # Game restarted if r key is pressed
    if event.keysym == 'r': init(data)

def timerFired(data):
    """
    Executed when the given time interval in data has elapsed.

    data: struct
    """
    if not data.gameOver:
        testMove = moveFallingPiece(data, 1, 0)
        # If the next move of the falling piece is illegal, 
        if testMove == False:
            # it stays in place and a new piece is generated.
            placeFallingPiece(data)
            newFallingPiece(data)
            # If new falling piece is illegal, the board is filled to the top.
            if not fallingPieceIsLegal(data):
                data.gameOver = True

def drawCell(canvas, data, row, col, color):
    """
    Draws a cell of the size given in data at the specified row and col.

    canvas: tkinter canvas obj
    data: struct
    row: pos int
    col: pos int
    color: str
    """
    x0, y0 = col * data.cellSize, row * data.cellSize
    x1, y1 = (col+1) * data.cellSize, (row+1) * data.cellSize
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=5)

def drawBoard(canvas, data):
    """
    Draws a Tetris grid according to the size and color specified in data.

    canvas: tkinter canvas obj
    data: struct
    """
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])

def drawFallingPiece(canvas, data):
    """
    Starting at the given indices in data, draws the given falling piece 
    according to the specifications in data.tetrisPieces.

    canvas: tkinter canvas obj
    data: struct
    """
    # Iterates through 2D list representing falling piece and draws cells 
    # as specified
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                drawCell(canvas, data, data.fallingPieceRow + row,
                    data.fallingPieceCol + col, data.fallingPieceColor)

def drawScore(canvas, data):
    """
    Displays the current score at the bottom of the window.

    canvas: tkinter canvas obj
    data: struct
    """
    canvas.create_text(data.width / 2, (data.rows + 0.5) * data.cellSize, 
        text='Score: %s' %data.score, font='Verdana 24', fill='black')

def drawGameOverPopup(canvas, data):
    """
    Displays an overlay notifiying the user that the game is over.

    canvas: tkinter canvas obj
    data: struct
    """
    canvas.create_rectangle(0, 200, 400, 400, fill='white')
    canvas.create_text(data.width / 2, data.height / 2, 
        text='Game Over!', font='Verdana 48')

def redrawAll(canvas, data):
    """
    Draws on window canvas when the time interval has elapsed.

    canvas: tkinter canvas obj
    data: struct
    """
    drawBoard(canvas, data)
    drawScore(canvas, data)
    if not data.gameOver:
        drawFallingPiece(canvas, data)
    else: drawGameOverPopup(canvas, data)

def run(width=300, height=300):
    """
    Displays graphical user interface for the Tetris game.
    """
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 750 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

if __name__ == '__main__':
    run(400, 600)
