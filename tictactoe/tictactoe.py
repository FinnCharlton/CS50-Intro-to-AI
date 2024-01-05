"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #Create count variables
    xCount = 0
    oCount = 0

    #Loop through lists and add up counts
    for row in board:
        for cell in row:
            if cell == X:
                xCount += 1
            elif cell == O:
                oCount +=1
    
    #Return correct player
    if xCount == oCount:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #Initialise set
    actions = set()

    #Loop through board, return all empty cells
    for rowIndex, row in enumerate(board):
        for colIndex, cell in enumerate(row):
            if cell == EMPTY:
                actions.add((rowIndex,colIndex))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #Parse action
    i = action[0]
    j = action[1]

    #Copy the original board
    copyBoard = copy.deepcopy(board)

    #Find player to move
    turn = player(copyBoard)
    
    #Check if action is legal
    if copyBoard[i][j] != EMPTY:
        raise Exception("Illegal move has been considered")
    
    #Apply action to board copy and return
    copyBoard[i][j] = turn
    return copyBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Initialse variable
    winner = str(None)

    #Check for rows winners
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][0] == board[row][2]:
            if board[row][0] != EMPTY:
                winner = board[row][0]
    
    #Check for rows winners
    for col in range(3):
        if board[0][col] == board[1][col] and board[0][col] == board[2][col]:
            if board[0][col] != EMPTY:
                winner = board[0][col]

    #Check for diagonal winners
    if board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        winner = board[0][0]
    if board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        winner = board[0][2]


    return winner

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #Return True if a player has won
    if str(winner(board)) != str(None):
        return True

    #Return False if any cell is empty, else return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #Find winner
    terminalWinner = winner(board)

    #Map utility
    if terminalWinner == X:
        return 1
    elif terminalWinner == O:
        return -1
    else:
        return 0

def maxScore(board):

    #Set v to maximally negative
    v = -10000

    #If board is terminal, it is just worth its utility
    if terminal(board):
        return utility(board)
    
    for actionMax in actions(board):
        v = max(v,minScore(result(board,actionMax)))
    return v
    
def minScore(board):

    #Set v to maximally positive
    v = 10000

    #If board is terminal, it is just worth its utility
    if terminal(board):
        return utility(board)
    
    for actionMin in actions(board):
        v = min(v,maxScore(result(board,actionMin)))
    return v
    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    actionScoreList = []

    #If player is X, return list of actions that maximise score
    if player(board) == X:
        for action in actions(board):
            score = minScore(result(board,action))
            actionScoreList.append([action,score])

        #Return an action with max score
        maxItem = [(0,0),-10000]
        for item in actionScoreList:
            if item[1] > maxItem[1]:
                maxItem = item
        return maxItem[0]
    
    #If player is O, return list of actions that minimise score
    if player(board) == O:
        for action in actions(board):
            score = maxScore(result(board,action))
            actionScoreList.append([action,score])

        #Return an action with mix score
        minItem = [(0,0),10000]
        for item in actionScoreList:
            if item[1] < minItem[1]:
                minItem = item
        return minItem[0]
        
            
