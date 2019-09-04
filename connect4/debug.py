from state import State, RED, YELLOW, EMPTY, BOARD_WIDTH, BOARD_HEIGHT

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

