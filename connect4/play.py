from state import State
from debug import print_board
from state_operations import move, empty_state

if __name__ == "__main__":
    s = empty_state()
    while True:
        print_board(s)
        col = int(input("Column "))
        s = move(s, col)
        print()