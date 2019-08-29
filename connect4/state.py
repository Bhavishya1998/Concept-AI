RED = 2
YELLOW = 3
EMPTY = 1

BOARD_WIDTH = 7
BOARD_HEIGHT = 6

ROW_LINES_IN_ROW = 4
COL_LINES_IN_COL = 3

NUM_ROW_LINES = BOARD_HEIGHT * ROW_LINES_IN_ROW
NUM_COL_LINES = BOARD_WIDTH * COL_LINES_IN_COL
NUM_DIAGS_ONE_SIDE = 12
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

    def lines_of_cell(self, cell):
        pass