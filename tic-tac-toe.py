import math
import copy

# Constants for representing the players, empty cells on the board
X = "X"
O = "O"
EMPTY = None

# Returns the player who is next to move
def player(board):
    if board == [] or board == [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]] or len([item for sublist in board for item in sublist]) % 2 == 0:
        return X
    return O

# Returns a set of all possible actions (i, j) available on the board
def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions

# Returns the board that results from making move (i, j) on the board
def result(board, action):
    if action not in actions(board):
        raise Exception("Invalid action")
    
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

# Returns the winner of the game, if there is one
def winner(board):
    for player in [X, O]:
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
                return player
        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return player
    return None

# Returns True if the game is over, False otherwise
def terminal(board):
    return winner(board) is not None or all(board[i][j] != EMPTY for i in range(3) for j in range(3))

# Returns the utility of the current board
def utility(board):
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0

# Returns the optimal move for the current player using the Minimax algorithm
def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)
    if current_player == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]

# Returns the maximum utility value and corresponding move for X
def max_value(board):
    if terminal(board):
        return utility(board), None

    v = -math.inf
    move = None
    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > v:
            v = min_val
            move = action
            if v == 1:
                break
    return v, move

# Returns the minimum utility value and corresponding move for O
def min_value(board):
    if terminal(board):
        return utility(board), None

    v = math.inf
    move = None
    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v = max_val
            move = action
            if v == -1:
                break
    return v, move
