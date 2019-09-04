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
# TODO correct this
# TODO refactor?

class State:
    
    def __init__(self, board, next_to_move):
        self.board = board
        self.next_to_move = next_to_move

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

    # TODO refactor next two functions
    def _first_cell_of_row_line(self, row):
        """ Return first cell of row. """

        return row // ROW_LINES_IN_ROW, row % ROW_LINES_IN_ROW

    def _first_cell_of_col_line(self, col):
        """ Return first cell of column. """

        adjusted_col = col - NUM_ROW_LINES
        return adjusted_col % COL_LINES_IN_COL, adjusted_col // COL_LINES_IN_COL

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