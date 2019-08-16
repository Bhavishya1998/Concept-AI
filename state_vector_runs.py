from identify_threats import State, X, O, EMPTY

def print_state(s: State):
    for y in range(3):
        print("|", end='')
        for x in range(3):
            if s.board[y][x] == X:
                print("X", end="|")
            if s.board[y][x] == O:
                print("O", end="|")
            if s.board[y][x] == EMPTY:
                print(" ", end="|")
        print()

    print("X: " + str(s.state_vectors[X]))
    print("O: " + str(s.state_vectors[O]))
    print()

if __name__ == "__main__":

    board = [
        [EMPTY, O, X],
        [EMPTY, X, EMPTY],
        [O, X, EMPTY]
    ]
    s = State(board)
    print_state(s)
    
    board = [
        [EMPTY, O, EMPTY],
        [X, X, O],
        [O, X, EMPTY]
    ]
    s = State(board)
    print_state(s)

    board = [
        [X, O, EMPTY],
        [EMPTY, X, EMPTY],
        [O, X, EMPTY]
    ]
    s = State(board)
    print_state(s)