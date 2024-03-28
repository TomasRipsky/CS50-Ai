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
    # Count the number of X's and O's on the board
    num_X = sum(row.count(X) for row in board)
    num_O = sum(row.count(O) for row in board)
    
    # If the number of X's is less than the number of O's, it's X's turn
    if num_X <= num_O:
        return X
    # Otherwise, it's O's turn
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    # Iterate through each cell of the board
    for i in range(3):
        for j in range(3):
            # If the cell is empty, add it to the set of possible actions
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Make a deep copy of the original board
    new_board = copy.deepcopy(board)

    # Extract the row and column indices from the action
    i, j = action

    # Ensure that the action is valid
    if new_board[i][j] is not EMPTY:
        raise Exception("Invalid action")

    # Determine whose turn it is and update the board with the action
    current_player = player(board)
    new_board[i][j] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows for a winner
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]

    # Check columns for a winner
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]

    # Check diagonals for a winner
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    # If no winner found, return None
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is a winner
    if winner(board) is not None:
        return True

    # Check if the board is full
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    # If no winner and the board is full, the game is over
    return True


def utility(board):
    """
    Returns the utility of the current board.
    """
    # Check if X has won
    if winner(board) == X:
        return 1
    # Check if O has won
    elif winner(board) == O:
        return -1
    # If neither X nor O has won, the game ended in a tie
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board using alpha-beta pruning.
    """
    # Define the maximizing and minimizing players
    maximizing_player = X
    minimizing_player = O

    # Define the recursive helper function to perform minimax search with alpha-beta pruning
    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board)

        v = float("inf")
        for action in actions(board):
            v = min(v, max_value(result(board, action), alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v

    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board)

        v = float("-inf")
        for action in actions(board):
            v = max(v, min_value(result(board, action), alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v

    # Perform minimax search with alpha-beta pruning to find the optimal action
    optimal_action = None
    if player(board) == maximizing_player:
        v = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        for action in actions(board):
            min_result = min_value(result(board, action), alpha, beta)
            if min_result > v:
                v = min_result
                optimal_action = action
            alpha = max(alpha, v)
    else:
        v = float("inf")
        alpha = float("-inf")
        beta = float("inf")
        for action in actions(board):
            max_result = max_value(result(board, action), alpha, beta)
            if max_result < v:
                v = max_result
                optimal_action = action
            beta = min(beta, v)

    return optimal_action


# Without Alpha-Beta Pruning
"""
def minimax(board):
    
    #Returns the optimal action for the current player on the board.
    
    # Define the maximizing and minimizing players
    maximizing_player = X
    minimizing_player = O

    # Define the recursive helper function to perform minimax search
    def min_value(board):
        if terminal(board):
            return utility(board)

        v = float("inf")
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    def max_value(board):
        if terminal(board):
            return utility(board)

        v = float("-inf")
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    # Perform minimax search to find the optimal action
    optimal_action = None
    if player(board) == maximizing_player:
        v = float("-inf")
        for action in actions(board):
            min_result = min_value(result(board, action))
            if min_result > v:
                v = min_result
                optimal_action = action
    else:
        v = float("inf")
        for action in actions(board):
            max_result = max_value(result(board, action))
            if max_result < v:
                v = max_result
                optimal_action = action

    return optimal_action
"""