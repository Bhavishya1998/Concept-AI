from state import State, RED, YELLOW, EMPTY, BOARD_WIDTH, BOARD_HEIGHT, EMPTY, UNAVAILABLE, SINGLE, DOUBLE, ATTACK

def print_board(state: State):
    """ Print the game board to console. """

    for r in range(BOARD_HEIGHT):
        print("|", end='')
        for c in range(BOARD_WIDTH):
            if state.board[r][c] == EMPTY:
                print(" |", end='')
            elif state.board[r][c] == RED:
                print("R|", end='')
            elif state.board[r][c] == YELLOW:
                print("Y|", end='')
        print()

    print()

def line_status_str(status):
    if status == EMPTY:
        return "EMPTY"
    elif status == UNAVAILABLE:
        return "UNAVAILABLE"
    elif status == SINGLE:
        return "SINGLE"
    elif status == DOUBLE:
        return "DOUBLE"
    elif status == ATTACK:
        return "ATTACK"