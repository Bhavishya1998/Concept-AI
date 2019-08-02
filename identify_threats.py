from n_dim_matrix import n_dim_matrix

X = 2
O = 3
EMPTY = 1

BOARD_SIZE = 3

# will be used to identify where a threat or double threat is
ROW = 0
COL = 1
DIAG = 2

class State:

    def __init__(self, board):
        self.board = board

        # NOTE call calc_products?
        self._calc_products()

    def _calc_products(self):
        """ Calculate the products across all lines. """

        self.row_prods = [1, 1, 1]
        self.col_prods = [1, 1, 1]
        self.diag_prods = [1, 1]

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                self.row_prods[y] *= self.board[y][x]
                self.col_prods[x] *= self.board[y][x]

                # check if cell is in leading diagonal
                if x == y:
                    self.diag_prods[0] *= self.board[y][x]

                # check if cell is in non-leading diagonal
                if x + y == BOARD_SIZE - 1:
                    self.diag_prods[1] *= self.board[y][x]

    def existing_threats(self, player):
        """
        Return list of all existing threats by player.
        """

        other_player = X if player == O else O

        if player == X:
            threat = X ** 2
        else:
            threat = O ** 2

        existing_threats = []

        for i in range(BOARD_SIZE):
            if self.row_prods[i] == threat and self.row_prods[i] % other_player != 0:
                existing_threats.append((ROW, i))
            if self.col_prods[i] == threat and self.col_prods[i] % other_player != 0:
                existing_threats.append((COL, i))

        for i in range(2):
            if self.diag_prods[i] == threat and self.diag_prods[i] % other_player != 0:
                existing_threats.append((DIAG, i))

        return existing_threats

    def double_threats(self, player):
        """
        Return the output of existing_threats if multiple threats exist. Else return None.
        """

        existing_threats = self.existing_threats(player)
        if len(existing_threats) > 1:
            return existing_threats
        else:
            return []
            
    def cells_in_line(self, line):
        """ Return list of all cells in line. """

        type, index = line

        cells = []

        if type == ROW:
            for i in range(BOARD_SIZE):
                cells.append((i, index))
        elif type == COL:
            for i in range(BOARD_SIZE):
                cells.append((index, i))
        else:
            for i in range(BOARD_SIZE):
                cells.append((i, i + 2*index*(1-i)))

        return cells

    def lines_available_to_player(self, player):
        """ Return list of all lines available to a player. """

        other_player = X if player == O else O

        available_lines = []

        for i in range(BOARD_SIZE):
            if self.row_prods[i] % other_player != 0:
                available_lines.append((ROW, i))
            if self.col_prods[i] % other_player != 0:
                available_lines.append((COL, i))

        for i in range(2):
            if self.diag_prods[i] % other_player != 0:
                available_lines.append((DIAG, i))

        return available_lines

    def empty_cells_in_line(self, line):
        """ Return list containing all empty cells in a line. """

        return list(filter(lambda c: self.board[c[1]][c[0]] == EMPTY, self.cells_in_line(line)))

    def line_intersection_cell(self, line1, line2):
        """
        Return the x, y coordinates of the points of intersection of two lines.
        Return None if the lines don't intersect.
        """

        line1_cells = self.cells_in_line(line1)
        line2_cells = self.cells_in_line(line2)

        intersection_set = set(line1_cells).intersection(set(line2_cells))

        if len(intersection_set) == 0: 
            # lines don't intersect
            return None
        else:
            return intersection_set.pop()

    def line_poses_potential_threat(self, line, player):
        """ Return true if player poses potential threat on the line. """

        type, index = line

        return (type == ROW and self.row_prods[index] // player == 1) \
        or (type == COL and self.col_prods[index] // player == 1) \
        or (type == DIAG and self.diag_prods[index] // player == 1)

    def potential_threats(self, player):
        """ Return list of all potential moves by player that would pose a threat. """

        available_lines = self.lines_available_to_player(player)
        
        # NOTE Just return the list of cells? Would have to eliminate duplicates then.
        return list(map(lambda l: (l, self.empty_cells_in_line(l)), 
                   filter(lambda l: self.line_poses_potential_threat(l, player), available_lines)))

    def potential_double_threats(self, player):
        """ Return list of all potential moves by player that would pose a double threat. """
        
        threatening_lines = self.potential_threats(player)

        potential_double_threats = []

        for i in range(len(threatening_lines)):
            for j in range(i+1, len(threatening_lines)):
                line1 = threatening_lines[i][0]
                line2 = threatening_lines[j][0]
                intersection_cell = self.line_intersection_cell(line1, line2)
                if intersection_cell is not None:
                    x, y = intersection_cell
                    if self.board[y][x] == EMPTY:
                        potential_double_threats.append(intersection_cell)

        return potential_double_threats

def empty_state():
    """ Create a blank game state. """

    return State(n_dim_matrix((BOARD_SIZE, BOARD_SIZE), fill=EMPTY))