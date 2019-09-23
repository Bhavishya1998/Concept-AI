from state import State, RED, YELLOW, EMPTY
from state_operations import empty_state, move
from debug import print_board, line_status_str, print_count_vector, state_vector_dump, adjust_cell, print_future_state_table

if __name__ == "__main__":
    # s = empty_state()

    # s2 = move(move(move(move(move(s, 1), 1), 6), 0), 5)
    # print_board(s2)

    # R = RED
    # Y = YELLOW
    # _ = EMPTY
    # board = [
    #     [_, _, _, _, _, _, _],
    #     [_, _, _, _, _, _, _],
    #     [R, _, _, _, _, _, _],
    #     [Y, _, _, _, _, R, R],
    #     [Y, _, _, R, R, Y, R],
    #     [Y, _, _, R, Y, Y, Y],
    # ]
    # state = State(board, next_to_move=YELLOW)
    state = move(move(move(move(move(move(move(empty_state(), 0), 6), 2), 6), 3), 6), 4)

    print_board(state)
    # print_future_state_table(state)
    print(state.double_threats_intersections(YELLOW))