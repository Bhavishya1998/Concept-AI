RED = 2
YELLOW = 3
EMPTY = 1

BOARD_WIDTH = 7
BOARD_HEIGHT = 6

ROW_LINES_IN_ROW = 4
COL_LINES_IN_COL = 3

NUM_ROW_LINES = BOARD_HEIGHT * ROW_LINES_IN_ROW
NUM_COL_LINES = BOARD_WIDTH * COL_LINES_IN_COL
NUM_DIAG_LINES_ONE_SIDE = 12
NUM_TOTAL_LINES = NUM_ROW_LINES + NUM_COL_LINES + 2*NUM_DIAG_LINES_ONE_SIDE 

AVAILABLE = 1
UNAVAILABLE = 2
CURRENT_ATTACK = 3
FUTURE_ATTACK = 4
SINGLE = 5
DOUBLE = 6

WIN = 0
LOSS = 1
DRAW = 2
UNCERTAIN = 3

def other_player(player: int):
    """ Return the opposite player. """

    return RED if player == YELLOW else YELLOW

class State:
    
    def __init__(self, board, next_to_move):
        self.board = board
        self.next_to_move = next_to_move

        self.calc_state_vectors()

    def _cell_below(self, cell):
        """ Return the cell below 'cell', or None if 'cell' is in the bottom row. """

        r, c = cell
        return (r+1, c) if r < BOARD_HEIGHT - 1 else None

    def _col_num_empty_cells(self, column):
        """ Return the number of empty cells in 'column'. """

        num = 0
        for row in range(BOARD_HEIGHT):
            if self.board[row][column] == EMPTY:
                num += 1
            else:
                break

        return num

    def col_highest_occupied_row(self, column):
        """ Return the highest occupied row in a column, or None if the column is empty. """

        # TODO use col_num_empty_cells here

        walk = 0
        while walk < BOARD_HEIGHT and self.board[walk][column] == EMPTY:
            walk += 1

        return walk if walk < BOARD_HEIGHT else None

    def possible_moves(self):
        """ Return list of possible moves for the next player. """

        moves = []

        for c in range(BOARD_WIDTH):
            r = self.col_highest_occupied_row(c)
            if r is not None:
                moves.append((r, c))

        return moves

    def _is_col(self, line):
        """ Return True if line is along a column. """

        return line >= NUM_ROW_LINES and line < NUM_ROW_LINES + NUM_COL_LINES

    def _row_lines_of_cell(self, cell):
        """ Return list of all row lines that 'cell' belongs to. """

        r, c = cell
        row_line_starting_at_cell = 4*r + c

        row_lines = []

        for i in range(4):
            new_row_line = row_line_starting_at_cell - i
            if new_row_line >= ROW_LINES_IN_ROW*r and new_row_line < ROW_LINES_IN_ROW*(r+1):
                row_lines.append(new_row_line)

        return row_lines

    def _col_lines_of_cell(self, cell):
        """ Return list of all column lines that 'cell' belongs to. """

        # shifting all indices back by 24 to ease calculations

        r, c = cell
        col_line_starting_at_cell = 3*c + r

        col_lines = []
        for i in range(4):
            new_col_line = col_line_starting_at_cell - i
            if new_col_line >= COL_LINES_IN_COL*c and new_col_line < COL_LINES_IN_COL*(c+1):
                col_lines.append(24 + new_col_line)

        return col_lines

    def diagonal_of_cell(self, cell, r2l: bool):
        """ Return the diagonal of 'cell'. """

        r, c = cell

        if r2l:
            diagonal = r + c - 3
        else:
            top_cell_r, top_cell_c = r - min(r, c), c - min(r, c)
            diagonal = 3 - top_cell_c + top_cell_r

        return diagonal

    def _diagonal_top_row(self, diagonal):
        """ Return the top row of 'diagonal'. """

        return max(0, diagonal - 3)

    def _num_lines_in_diagonal(self, diagonal):
        """ Return the number of lines in 'diagonal'. """

        if diagonal in [0, 5]:
            return 1
        elif diagonal in [1, 4]:
            return 2
        elif diagonal in [2, 3]:
            return 3
        else:
            # should not be reached for legal diagonal
            return 0

    def _diagonal_start_end_lines(self, diagonal, r2l: bool):
        """ Return tuple of first and last line of diagonal. """

        if r2l:
            # right to left diagonal
            start_line = NUM_ROW_LINES + NUM_COL_LINES + ((diagonal+1)*diagonal//2 if diagonal <= 3 else 9 + 2*(diagonal-4))
            end_line = start_line + self._num_lines_in_diagonal(diagonal) - 1
        else:
            # left to right diagonal
            start_line = NUM_ROW_LINES + NUM_COL_LINES + NUM_DIAG_LINES_ONE_SIDE + ((diagonal+1)*diagonal//2 if diagonal <= 3 else 9 + 2*(diagonal-4))
            end_line = start_line + self._num_lines_in_diagonal(diagonal) - 1

        return start_line, end_line

    def _diag_lines_of_cell(self, cell, r2l: bool):
        """ Return either the right to left or left to right diagonal lines of cell. """

        r, c = cell

        diagonal = self.diagonal_of_cell(cell, r2l)

        if r2l:
            diagonal = r + c - 3
        else:
            top_cell_r, top_cell_c = r - min(r, c), c - min(r, c)
            diagonal = 3 - top_cell_c + top_cell_r

        if diagonal < 0 or diagonal > 5:
            # no diagonal lines pass through the cell
            return []
        
        start_line, end_line = self._diagonal_start_end_lines(diagonal, r2l)

        diag_lines = []

        top_row = self._diagonal_top_row(diagonal)

        for line in range(start_line, end_line+1):
            row_shift = line - start_line
            if top_row + row_shift <= r and r <= top_row + row_shift + 3:
                diag_lines.append(line)

        return diag_lines

    def lines_of_cell(self, cell):
        """ Return all lines passing through 'cell'. """

        return self._row_lines_of_cell(cell) + \
            self._col_lines_of_cell(cell) + \
            self._diag_lines_of_cell(cell, True) + \
            self._diag_lines_of_cell(cell, False)

    def _first_cell_of_row_line(self, line):
        """ Return first cell of row. """

        return line // ROW_LINES_IN_ROW, line % ROW_LINES_IN_ROW

    def _first_cell_of_col_line(self, line):
        """ Return first cell of column. """

        adjusted_line = line - NUM_ROW_LINES
        return adjusted_line % COL_LINES_IN_COL, adjusted_line // COL_LINES_IN_COL

    def diagonal_of_line(self, line):
        """ Return the diagonal that the line belongs to. """

        # TODO find a function for this, split into two for r2l and l2r if necessary
        if line in [45, 57]:
            return 0
        elif line in [46, 47, 58, 59]:
            return 1
        elif line in [48, 49, 50, 60, 61, 62]:
            return 2
        elif line in [51, 52, 53, 63, 64, 65]:
            return 3
        elif line in [54, 55, 66, 67]:
            return 4
        elif line in [56, 68]:
            return 5

    def _first_cell_of_r2l_diagonal_line(self, line):
        """ Return the first cell of right to left diagonal. """

        diagonal = self.diagonal_of_line(line)

        shift_r = 1
        shift_c = -1
        
        start_line, _ = self._diagonal_start_end_lines(diagonal, r2l=True)
        shift = line - start_line

        return max(0, diagonal - 3) + shift*shift_r, min(6, 3 + diagonal) + shift*shift_c

    def _first_cell_of_l2r_diagonal_line(self, line):
        """ Return the first cell of left to right diagonal. """

        diagonal = self.diagonal_of_line(line)

        shift_r = 1
        shift_c = 1

        start_line, _ = self._diagonal_start_end_lines(diagonal, r2l=False)
        shift = line - start_line


        return max(0, diagonal - 3) + shift*shift_r, max(0, 3 - diagonal) + shift*shift_c

    def line_to_cells(self, line):
        """ Return list of all cells of a line. """

        if line >= NUM_ROW_LINES + NUM_COL_LINES + NUM_DIAG_LINES_ONE_SIDE:
            # l2r diag
            first_cell_r, first_cell_c = self._first_cell_of_l2r_diagonal_line(line)
            shift_r = 1
            shift_c = 1
        elif line >= NUM_ROW_LINES + NUM_COL_LINES:
            # r2l diag
            first_cell_r, first_cell_c = self._first_cell_of_r2l_diagonal_line(line)
            shift_r = 1
            shift_c = -1
        elif line >= NUM_ROW_LINES:
            # col
            first_cell_r, first_cell_c = self._first_cell_of_col_line(line)
            shift_r = 1
            shift_c = 0
        else:
            # row
            first_cell_r, first_cell_c = self._first_cell_of_row_line(line)
            shift_r = 0
            shift_c = 1
            
        return [(first_cell_r + i*shift_r, first_cell_c + i*shift_c) for i in range(4)]

    def line_status(self, line, player):
        """ Return the status of 'line'. """

        other = other_player(player)

        if player == RED:
            attack = RED ** 3
            double = RED ** 2
            single = RED
        else:
            attack = YELLOW ** 3
            double = YELLOW ** 2
            single = YELLOW

        # calculate product of cells in line
        cells = self.line_to_cells(line)
        prod = 1
        for r, c in cells:
            prod *= self.board[r][c]

        if prod % other == 0:
            # other player has a coin on the line
            return UNAVAILABLE
        elif prod == attack:
            if self.line_future_state(line) == []:
                return CURRENT_ATTACK
            else:
                return FUTURE_ATTACK
        elif prod == double:
            return DOUBLE
        elif prod == single:
            return SINGLE
        else:
            return EMPTY

    def _empty_cells_in_line(self, line):
        """ Return list of empty cells in 'line'. """

        return [(r, c) for r, c in self.line_to_cells(line) if self.board[r][c] == EMPTY]

    def calc_state_vectors(self):
        """ Calculate and store state vectors for both players. """

        # TODO test this?
        self.state_vector = {RED: {}, YELLOW: {}}

        self.state_vector[RED]["available"] = []
        self.state_vector[YELLOW]["available"] = []
        self.state_vector[RED]["single"] = []
        self.state_vector[YELLOW]["single"] = []
        self.state_vector[RED]["double"] = []
        self.state_vector[YELLOW]["double"] = []
        self.state_vector[RED]["current_attack"] = []
        self.state_vector[YELLOW]["current_attack"] = []
        self.state_vector[RED]["future_attack"] = []
        self.state_vector[YELLOW]["future_attack"] = []
        self.state_vector[RED]["unavailable"] = []
        self.state_vector[YELLOW]["unavailable"] = []

        for line in range(NUM_TOTAL_LINES):

            # TODO change the status function to return for both lines to cut processing?
            status_red = self.line_status(line, RED)
            status_yellow = self.line_status(line, YELLOW)

            # TODO can this be optimized?
            if status_red == EMPTY:
                self.state_vector[RED]["available"].append(line)
                self.state_vector[YELLOW]["available"].append(line)
            else:
                if status_red == SINGLE:
                    self.state_vector[RED]["available"].append(line)
                    self.state_vector[RED]["single"].append(line)
                    self.state_vector[YELLOW]["unavailable"].append(line)
                elif status_red == DOUBLE:
                    self.state_vector[RED]["available"].append(line)
                    self.state_vector[RED]["double"].append(line)
                    self.state_vector[YELLOW]["unavailable"].append(line)
                elif status_red == CURRENT_ATTACK:
                    self.state_vector[RED]["available"].append(line)
                    self.state_vector[RED]["current_attack"].append((line, self._empty_cells_in_line(line)[0]))
                    self.state_vector[YELLOW]["unavailable"].append(line)
                elif status_red == FUTURE_ATTACK:
                    self.state_vector[RED]["available"].append(line)
                    self.state_vector[RED]["future_attack"].append((line, self._empty_cells_in_line(line)[0]))
                    self.state_vector[YELLOW]["unavailable"].append(line)
                elif status_yellow == SINGLE:
                    self.state_vector[RED]["unavailable"].append(line)
                    self.state_vector[YELLOW]["available"].append(line)
                    self.state_vector[YELLOW]["single"].append(line)
                elif status_yellow == DOUBLE:
                    self.state_vector[RED]["unavailable"].append(line)
                    self.state_vector[YELLOW]["available"].append(line)
                    self.state_vector[YELLOW]["double"].append(line)
                elif status_yellow == CURRENT_ATTACK:
                    self.state_vector[RED]["unavailable"].append(line)
                    self.state_vector[YELLOW]["available"].append(line)
                    self.state_vector[YELLOW]["current_attack"].append((line, self._empty_cells_in_line(line)[0]))
                elif status_yellow == FUTURE_ATTACK:
                    self.state_vector[RED]["unavailable"].append(line)
                    self.state_vector[YELLOW]["available"].append(line)
                    self.state_vector[YELLOW]["future_attack"].append((line, self._empty_cells_in_line(line)[0]))

    def line_future_state(self, line):
        """ Return the future state for a line. """

        # columns don't have a future state
        cells = [] if self._is_col(line) else self.line_to_cells(line)

        future_state = []

        for cell in cells:
            cell_below = self._cell_below(cell)
            if cell_below is not None and self.board[cell_below[0]][cell_below[1]] == EMPTY:
                future_state.append(cell_below)

        return future_state

    def future_state(self, player):
        """
        Return a dictionary with lines singly and doubly occupied by the player as keys and a tuple of their status and future state as values.
        """

        future_state = {}

        # NOTE would a single loop be more efficient? Probably won't be able to use list comprehensions then.

        for line in self.state_vector[player]["single"]:
            future_state[line] = (SINGLE, self.line_future_state(line))
        for line in self.state_vector[player]["double"]:
            future_state[line] = (DOUBLE, self.line_future_state(line))
        for line, _ in self.state_vector[player]["current_attack"]:
            future_state[line] = (CURRENT_ATTACK, self.line_future_state(line))
        for line, _ in self.state_vector[player]["future_attack"]:
            future_state[line] = (FUTURE_ATTACK, self.line_future_state(line))

        return future_state

    def line_intersection_cells(self, line1, line2):
        """ Return the list of cells common between two lines. """

        intersection_cells = []
        cells1 = self.line_to_cells(line1)
        cells2 = self.line_to_cells(line2)

        for cell in cells1:
            if cell in cells2:
                intersection_cells.append(cell)

        # lines don't intersect
        return intersection_cells

    def line_potential_threat(self, line, player):
        """
        Return list of coordinates of the cells that can be played by 'player' to attack this line.
        An empty list is returned if an attack is not possible or the line is already under attack.
        """

        # TODO if the future state of a ATTACK line is zeroed, that can also be counted as a threat, but it would attack a differnent line.
        # TODO perhaps define does_move_create_opponent_current_attack as a more general function for both players?
        if self.line_status(line, player) != DOUBLE or self.line_future_state(line) != []:
            return []

        cells = self.line_to_cells(line)
        
        potential_cells = []

        if self._is_col(line):
            # future state is not defined for columns, use different method here

            # column line can only be attacked by playing the second cell from the top
            potential_cells.append(cells[1])
        else:
            for cell in cells:
                r, c = cell
                if self.board[r][c] == EMPTY:
                    potential_cells.append(cell)

        return potential_cells

    def potential_double_threats(self, player):
        """
        Return list of tuples where the first two elements are the lines involved in a potential double threat 
        and the 3rd is the cell to play.
        """

        double_threats = []
        
        # lines which can potentially be attacked
        double_lines = [line for line in range(NUM_TOTAL_LINES) if self.line_status(line, player) == DOUBLE]

        for index1 in range(len(double_lines)):
            for index2 in range(index1+1, len(double_lines)):
                intersection_cells = self.line_intersection_cells(double_lines[index1], double_lines[index2])
                if len(intersection_cells) > 0:
                    # the lines intersect

                    line1_attack_cells = self.line_potential_threat(double_lines[index1], player)
                    line2_attack_cells = self.line_potential_threat(double_lines[index2], player)

                    if len(line1_attack_cells) > 0 and len(line2_attack_cells) > 0:
                        # both lines can be attacked

                        for intersection_cell in intersection_cells:
                            if intersection_cell in line1_attack_cells and intersection_cell in line2_attack_cells:
                                double_threats.append((double_lines[index1], double_lines[index2], intersection_cell))

        # no double threats can be played this turn
        return double_threats

    def does_move_create_opponent_current_attack(self, move, player):
        """ Check if a move turns an opponent future attack into a current attack for 'player'. """

        column = move
        highest_occupied_row = self.col_highest_occupied_row(column)    
        
        if highest_occupied_row in [0, 1]:
            # column is full or will be full

            return False

        cell_above = highest_occupied_row - 2, column

        for line in self.lines_of_cell(cell_above):
            if self.line_status(line, player) == FUTURE_ATTACK:
                return True

        return False

    def consecutive_double_threats(self):
        """ Return list of consecutive double threats that the next player can play. """
        # TODO improve docstring

        player = self.next_to_move
        other = other_player(player)
        consec_double_threats = []

        cells = self.possible_moves()

        # NOTE a move creates a future attack and a double attack, and the resulting block converts the future attack into a current attack?

        for cell in cells:
            # TODO get lines, find which will be attacked
            # TODO find the cell that blocks said attack
            # TODO see if the FS of the future attacked lines of the cell above are zeroed
            lines = self.lines_of_cell(cell)
            double_lines = [line for line in lines if self.line_status(line, player) == DOUBLE]

            for line in double_lines:
                line_empty_cells = self._empty_cells_in_line(line)
                cell_to_block = line_empty_cells[0] if line_empty_cells[0] == cell else line_empty_cells[1]
                cell_to_block_r, cell_to_block_c = cell_to_block
                
                # NOTE what if playing the block creates an attack for the opponent?
                # ^^^ probably can't. we are talking about zeroing an fs
                
                if cell_to_block_r == 0:
                    # there is no cell above the blocked cell
                    continue
                
                cell_above_blocked_cell = cell_to_block_r - 1, cell_to_block_c
                double_lines_above = [line_above for line_above in self.lines_of_cell(cell_above_blocked_cell) if self.line_status(line_above, player) == DOUBLE]
                # for line_above in double_lines_above:
                #     if self.line_fu

    def result(self):
        """
        Return the certain result for the game state for the current player, 
        or UNCERTAIN if a conclusion can't be forcasted.
        """

        # NOTE use the length of potential double threats here? It would probably be slower.

        player = self.next_to_move
        other = other_player(player)

        if len(self.state_vector[player]["current_attack"]) > 0:
            return WIN
            
        # TODO check if opponent has an attack (Should we check if opponent has two non intersecting attacks?)
        # it's a loss if the opponent has two non-interescting current attacks
        if len(self.state_vector[other]["current_attack"]) >= 2:
            empty_cell = self.state_vector[other]["current_attack"][0][1]
            for _, cell in self.state_vector[other]["current_attack"]:
                # check if at least one of the attacked lines have a different empty cell

                if cell != empty_cell:
                    return LOSS

        # TODO should we check if the intersection cell is playable?
        for index1 in range(len(self.state_vector[player]["double"])):
            for index2 in range(index1+1, len(self.state_vector[player]["double"])):
                intersection_cells = self.line_intersection_cells(self.state_vector[player]["double"][index1], self.state_vector[player]["double"][index2])
                if len(intersection_cells) > 0:
                    # the lines intersect

                    line1_attack_cells = self.line_potential_threat(self.state_vector[player]["double"][index1], player)
                    line2_attack_cells = self.line_potential_threat(self.state_vector[player]["double"][index2], player)

                    if len(line1_attack_cells) > 0 and len(line2_attack_cells) > 0:
                        # both lines can be attacked

                        for intersection_cell in intersection_cells:
                            if intersection_cell in line1_attack_cells and intersection_cell in line2_attack_cells and not self.does_move_create_opponent_current_attack(intersection_cell[1], other):
                                return WIN

        # no conlusion can be deduced
        return UNCERTAIN