from state import State, other_player, RED, YELLOW, EMPTY, BOARD_HEIGHT, BOARD_WIDTH
from copy import deepcopy
from n_dim_matrix import n_dim_matrix

def move(state: State, column: int):
    """ Drop the next player's coin into 'column' and return the new game state object. """

    # find the highest occupied row in the column
    highest_occupied_row = state.col_highest_occupied_row(column)
    row = (BOARD_HEIGHT - 1) if highest_occupied_row is None else (highest_occupied_row - 1)

    # put into the row above the highest occupied row
    new_board = deepcopy(state.board)
    new_board[row][column] = state.next_to_move
    next_player = other_player(state.next_to_move)

    return State(new_board, next_player)

def empty_state():
    """ Return a game object with an empty board and red to move. """

    board = n_dim_matrix((BOARD_HEIGHT, BOARD_WIDTH), fill=EMPTY)
    return State(board, YELLOW)
