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
ATTACK = 3
SINGLE = 4
DOUBLE = 5

def other_player(player: int):
    """ Return the opposite player. """

    return RED if player == YELLOW else YELLOW

class State:
    
    def __init__(self, board, next_to_move):
        self.board = board
        self.next_to_move = next_to_move

    def _cell_below(self, cell):
        """ Return the cell below 'cell', or None if 'cell' is in the bottom row. """

        r, c = cell
        return (r+1, c) if r < BOARD_HEIGHT - 1 else None

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
            return ATTACK
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
        self.state_vector[RED]["attack"] = []
        self.state_vector[YELLOW]["attack"] = []
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
                elif status_red == ATTACK:
                    self.state_vector[RED]["available"].append(line)
                    self.state_vector[RED]["attack"].append((line, self._empty_cells_in_line(line)[0]))
                    self.state_vector[YELLOW]["unavailable"].append(line)
                elif status_yellow == SINGLE:
                    self.state_vector[RED]["unavailable"].append(line)
                    self.state_vector[YELLOW]["available"].append(line)
                    self.state_vector[YELLOW]["single"].append(line)
                elif status_yellow == DOUBLE:
                    self.state_vector[RED]["unavailable"].append(line)
                    self.state_vector[YELLOW]["available"].append(line)
                    self.state_vector[YELLOW]["double"].append(line)
                elif status_yellow == ATTACK:
                    self.state_vector[RED]["unavailable"].append(line)
                    self.state_vector[YELLOW]["available"].append(line)
                    self.state_vector[YELLOW]["attack"].append((line, self._empty_cells_in_line(line)[0]))

    def line_future_state(self, line):
        """ Return the future-state for a line. """

        # columns don't have a future state
        cells = [] if line >= NUM_ROW_LINES and line < NUM_ROW_LINES + NUM_COL_LINES else self.line_to_cells(line)

        future_state = []

        for cell in cells:
            cell_below = self._cell_below(cell)
            if cell_below is not None and self.board[cell_below[0]][cell_below[1]] == EMPTY:
                future_state.append(cell_below)

        return future_state