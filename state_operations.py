from state import State, X, O, EMPTY
from copy import deepcopy

def next_state(state: State, move):
    """ Play 'move' on 'state' and return the next state. """

    x, y = move
    next_player = state.other_player(state.next_to_move)
    new_board = deepcopy(state.board)

    new_board[y][x] = state.next_to_move

    return State(new_board, next_to_move=next_player)
