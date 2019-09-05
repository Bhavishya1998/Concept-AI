from state import State, other_player, RED, YELLOW, EMPTY, BOARD_HEIGHT, BOARD_WIDTH
from copy import deepcopy
from n_dim_matrix import n_dim_matrix

def move(state: State, column: int):
    """ Drop the next player's coin into the 'column' and return the new game state object. """

    # find the highest occupied slot in the column
    walk = 0
    while walk < BOARD_HEIGHT and state.board[walk][column] == EMPTY:
        walk += 1

    # put into the slot above the highest occupied slot
    slot = walk - 1
    new_board = deepcopy(state.board)
    new_board[slot][column] = state.next_to_move
    next_player = other_player(state.next_to_move)

    return State(new_board, next_player)

def empty_state():
    """ Return a game object with an empty board and red to move. """

    board = n_dim_matrix((BOARD_HEIGHT, BOARD_WIDTH), fill=EMPTY)
    return State(board, RED)
