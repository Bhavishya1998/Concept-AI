from state import State, RED, YELLOW, EMPTY, BOARD_WIDTH, BOARD_HEIGHT, EMPTY, UNAVAILABLE, SINGLE, DOUBLE, CURRENT_ATTACK, FUTURE_ATTACK, NUM_ROW_LINES, NUM_COL_LINES, NUM_DIAG_LINES_ONE_SIDE
from tree import Node

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

def adjust_cell(cell):
    """ Adjust a cell to fit the format of the email thread. """

    r, c = cell
    return 6 - r, c + 1

def adjust_line(line, state=None):
    """
    Adjust a line to fit the format of the email thread.
    State must passed for diagonals.
    """

    if line < NUM_ROW_LINES:
        row, shift = divmod(line, 4)
        adjusted_row = 6 - row
        return ("0" * shift) + (str(adjusted_row) * 4) + ("0" * (3 - shift))
    elif line < NUM_ROW_LINES + NUM_COL_LINES:
        col, row = divmod(line - NUM_ROW_LINES, 3)
        adjusted_row, _ = adjust_cell((row, col))
        return ("0" * col) + str(adjusted_row - 3) + ("0" * (6 - col))
    elif line < NUM_ROW_LINES + NUM_COL_LINES + NUM_DIAG_LINES_ONE_SIDE:
        top_cell = state.line_to_cells(line)[0]
        _, top_cell_c = top_cell
        adjusted_cell_r, _ = adjust_cell(top_cell)
        return ("0" * (top_cell_c - 3)) + (''.join([str(i) for i in range(adjusted_cell_r - 3, adjusted_cell_r + 1)])) + ("0" * (6 - top_cell_c))
    else:
        top_cell = state.line_to_cells(line)[0]
        _, top_cell_c = top_cell
        adjusted_cell_r, _ = adjust_cell(top_cell)
        return ("0" * top_cell_c) + (''.join([str(i) for i in range(adjusted_cell_r, adjusted_cell_r - 4, -1)])) + ("0" * (3 - top_cell_c))

def line_status_str(status):
    if status == EMPTY:
        return "EMPTY"
    elif status == UNAVAILABLE:
        return "UNAVAILABLE"
    elif status == SINGLE:
        return "SINGLE"
    elif status == DOUBLE:
        return "DOUBLE"
    elif status == CURRENT_ATTACK:
        return "CURRENT ATTACK"
    elif status == FUTURE_ATTACK:
        return "FUTURE ATTACK"

def state_vector_dump(state: State):
    state.calc_state_vectors()
    print("RED")
    print("Single : ", state.state_vector[RED]["single"])
    print("Double : ", state.state_vector[RED]["double"])
    print("Attack : ", state.state_vector[RED]["attack"])
    print("Unavailable : ", state.state_vector[RED]["unavailable"])
    print("\nYELLOW")
    print("Single : ", state.state_vector[YELLOW]["single"])
    print("Double : ", state.state_vector[YELLOW]["double"])
    print("Attack : ", state.state_vector[YELLOW]["attack"])
    print("Unavailable : ", state.state_vector[YELLOW]["unavailable"])

# NOTE haven't implemented count vector in state yet 
def print_count_vector(state: State):
    state.calc_state_vectors()
    print("RED")
    for k, v in state.state_vector[RED].items():
        print(k, " : ", len(v))
    print("\nYELLOW")
    for k, v in state.state_vector[YELLOW].items():
        print(k, " : ", len(v))

def print_future_state_table(state: State):
    """ Print out a table of future states for both players """

    red_fs = state.future_state(RED)
    yellow_fs = state.future_state(YELLOW)

    print("RED")
    for line, val in red_fs.items():
        status, fs = val
        print(f"line {adjust_line(line, state)} | {line_status_str(status)} | future state {[adjust_cell(cell) for cell in fs]}")

    print("\nYELLOW")
    for line, val in yellow_fs.items():
        status, fs = val
        print(f"line {adjust_line(line, state)} | {line_status_str(status)} | future state {[adjust_cell(cell) for cell in fs]}")

def print_double_threat_table(state: State):
    red_pdt = state.potential_double_threats(RED)
    yellow_pdt = state.potential_double_threats(YELLOW)

    print("RED")
    for line1, line2, cell in red_pdt:
        print(f"{adjust_line(line1)} | {adjust_line(line2)} | {adjust_cell(cell)}")

    print("\nYELLOW")
    for line1, line2, cell in yellow_pdt:
        print(f"{adjust_line(line1)} | {adjust_line(line2)} | {adjust_cell(cell)}")

def print_tree(node: Node):
    print_board(node.state)
    for child in node.children:
        print_tree(child)

    # print("--------------------------------------------------")