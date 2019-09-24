from state import State, RED, YELLOW, EMPTY
from state_operations import empty_state, move
from debug import print_board, line_status_str, print_count_vector, state_vector_dump, adjust_cell, print_future_state_table, print_double_threat_intersection_table

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
    state = move(move(move(move(empty_state(), 2), 0), 3), 0)
    # state = move(move(move(move(move(empty_state(), 3), 2), 4), 3), 4)

    print_board(state)
    print(state.is_sure_win())
    # print(state.line_potential_threat(55, RED))
    # print_future_state_table(state)
    # print(state.double_threats_intersections(YELLOW))
    # print_double_threat_intersection_table(state)