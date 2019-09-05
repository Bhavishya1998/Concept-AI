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
