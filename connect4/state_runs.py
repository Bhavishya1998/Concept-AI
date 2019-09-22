from state import State, RED, YELLOW
from state_operations import empty_state, move
from debug import print_board, line_status_str, print_count_vector, state_vector_dump, adjust_cell, print_future_state_table

if __name__ == "__main__":
    # s = empty_state()

    # s2 = move(move(move(move(move(s, 1), 1), 6), 0), 5)
    # print_board(s2)

    state = move(move(move(move(move(move(move(move(move(move(move(move(move(empty_state(), 5), 3), 5), 3), 6), 6), 0), 6), 0), 5), 0), 0), 4)

    print_board(state)
    # print(state.line_future_state(8))
    print_future_state_table(state)