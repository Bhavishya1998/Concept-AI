from state import State, X, O, EMPTY

def print_board(s: State, flip_vertical=False, flip_horizontal=False):
    for y in range(3):
        print("|", end='')
        cell_y = 2 - y if flip_horizontal else y
        for x in range(3):
            cell_x = 2 - x if flip_vertical else x
            if s.board[cell_y][cell_x] == X:
                print("X", end="|")
            if s.board[cell_y][cell_x] == O:
                print("O", end="|")
            if s.board[cell_y][cell_x] == EMPTY:
                print(" ", end="|")
        print()

    print()