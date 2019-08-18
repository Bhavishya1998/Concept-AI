from state import State, X, O, EMPTY, BOARD_SIZE
from copy import deepcopy
from n_dim_matrix import n_dim_matrix

def empty_state():
    """ Create a blank game state. """

    return State(n_dim_matrix((BOARD_SIZE, BOARD_SIZE), fill=EMPTY))

def next_state(state: State, move):
    """ Play 'move' on 'state' and return the next state. """

    # NOTE should a move be checked for validity?

    x, y = move
    next_player = state.other_player(state.next_to_move)
    new_board = deepcopy(state.board)

    new_board[y][x] = state.next_to_move

    return State(new_board, next_to_move=next_player)

