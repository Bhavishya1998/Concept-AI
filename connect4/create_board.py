from state import State
from debug import print_board
from state_operations import move, empty_state

if __name__ == "__main__":
    s = empty_state()
    state_str = "empty_state()"
    while True:
        print_board(s)
        print(state_str)
        col = int(input("Column "))
        s = move(s, col)
        state_str = f"move({state_str}, {col})"
        print()