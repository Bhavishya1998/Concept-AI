from n_dim_matrix import n_dim_matrix

X = 2
O = 3
EMPTY = 1

BOARD_SIZE = 3
NUM_LINES = 2*BOARD_SIZE + 2

# will be used to identify where a threat or double threat is
ROW = 0
COL = 1
DIAG = 2

MUTUALLY_KILLED = 0
UNOCCUPIED = 5

class State:

    def __init__(self, board, calc_vectors=True):
        self.board = board

        self.intersections = {
            X: {"uu": [], "ou": [], "oo": []}, 
            O: {"uu": [], "ou": [], "oo": []}
        }

        # TODO refactor
        self.state_vectors = {}

        if calc_vectors:
            self._calc_products()
            self.calc_state_vector(X)
            self.calc_state_vector(O)

    def _other_player(self, player):
        """ Take a player and returns the other player(opponent). """

        return O if player == X else X 

    def cell_row_col(self, cell):
        """ Return a tuple (row, col) where row is the index of the row of the cell and col is the index of its column. """

        x, y = cell
        row = y
        col = x + BOARD_SIZE

        return (row, col)

    def cell_diags(self, cell):
        """ Return list of indices of all diagonals the cell belongs to. """

        x, y = cell
        diags = []
        if x == y:
            diags.append(2*BOARD_SIZE)
        if x + y == BOARD_SIZE - 1:
            diags.append(2*BOARD_SIZE + 1)

        return diags
    
    def _calc_products(self):
        """ Calculate the products across all lines. """

        self.line_prods = [1] * NUM_LINES

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                row, col = self.cell_row_col((x, y))
                self.line_prods[row] *= self.board[y][x]
                self.line_prods[col] *= self.board[y][x]

                for diag in self.cell_diags((x, y)):
                    self.line_prods[diag] *= self.board[y][x]

    def _occupancy(self, line):
        """
        Classify line as:
            - Singly occupied: X/O
            - Unoccupied: UNOCCUPIED
            - killed: KILLED
        """

        if self.line_prods[line] == 1:
            return UNOCCUPIED
        elif self.line_prods[line] % X == 0 and self.line_prods[line] % O == 0:
            return MUTUALLY_KILLED
        elif self.line_prods[line] % X == 0:
            return X
        else:
            return O

    # TODO do we need this?
    def classify_lines(self):
        """
        Classify all lines as:
            - Unoccupied -> 1
            - Singly Occupied -> X/O
            - Threat -> X^2/O^2
            - Mutually killed -> 0
        """

        return list(map(lambda l: 0 if l % X == 0 and l % O == 0 else l, self.line_prods))

    def calc_state_vector(self, player):
        """ Calculate and store the state vector for a player. """

        other_player = self._other_player(player)

        unoccupied = []
        occupied = []
        attack = []
        available = []
        killed = []

        # TODO refactor
        uu = []
        ou = []
        oo = []

        for line in range(NUM_LINES):
            occupancy = self._occupancy(line)
            
            if occupancy == player:
                occupied.append(line)
            elif occupancy == other_player or occupancy == MUTUALLY_KILLED:
                killed.append(line)
            elif occupancy == UNOCCUPIED:
                unoccupied.append(line)
            
            if self.line_prods[line] == player ** 2:

                # store (line, attacked cell) tuples
                attack.append((line, self.empty_cells_in_line(line)[0]))

        available = occupied + unoccupied

        for line1 in range(NUM_LINES):
            occupancy_line1 = self._occupancy(line1)
            
            for line2 in range(line1 + 1, NUM_LINES):
                occupancy_line2 = self._occupancy(line2)

                intersection_cell = self.line_intersection_cell(line1, line2)

                # if the lines intersect
                if intersection_cell is not None:
                    if occupancy_line1 * occupancy_line2 == UNOCCUPIED * UNOCCUPIED:
                        uu.append((line1, line2, intersection_cell))
                    elif occupancy_line1 * occupancy_line2 == player * UNOCCUPIED:
                        ou.append((line1, line2, intersection_cell))
                    elif occupancy_line1 * occupancy_line2 == player * player and \
                        self.board[intersection_cell[1]][intersection_cell[0]] == EMPTY:
                        
                        oo.append((line1, line2, intersection_cell))

        self.state_vectors[player] = [unoccupied, occupied, attack, available, killed, uu, ou, oo]

    def count_state_vector(self, player):
        """ Return a vector with the lengths of all state vector lists of the input player. """

        return list(map(len, self.state_vectors[player]))

    def line_type(self, line):
        """ Return the line type (row, column or diagonal) from the index of the line. """

        if line < BOARD_SIZE:
            return ROW
        elif line < 2*BOARD_SIZE:
            return COL
        else:
            return DIAG

    def existing_threats(self, player):
        """
        Return list of line indices where the player poses a threat.
        """

        threat = X ** 2 if player == X else O ** 2
        indices = [i for i in range(NUM_LINES)]
        return list(filter(lambda x: x is not None, map(lambda l, i: i if l == threat else None, self.line_prods, indices)))

    def double_threats(self, player):
        """
        Return the output of existing_threats if multiple threats exist. Else return an empty list.
        """

        existing_threats = self.existing_threats(player)
        return existing_threats if len(existing_threats) > 1 else []
            
    def cells_in_line(self, line):
        """ Return list of all cells in line. """

        type = self.line_type(line)

        if type == ROW:
            return [(i, line) for i in range(BOARD_SIZE)]
        elif type == COL:
            return [(line - BOARD_SIZE, i) for i in range(BOARD_SIZE)]
        else:
            return [(i, i + 2*(line - 2*BOARD_SIZE)*(1-i)) for i in range(BOARD_SIZE)]

    def available_lines(self, player):
        """ Return list of all lines available to a player. """

        other_player = self._other_player(player)
        indices = [i for i in range(NUM_LINES)]

        return list(filter(lambda x: x is not None ,map(lambda l, i: i if l % other_player != 0 else None, self.line_prods, indices)))

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
        
        return None if len(intersection_set) == 0 else intersection_set.pop()

    def line_poses_potential_threat(self, line, player):
        """ Return true if player poses potential threat on the line. """

        other_player = self._other_player(player)
        return self.line_prods[line] % other_player != 0 and self.line_prods[line] // player == 1

    def potential_threats(self, player):
        """ Return list of all potential moves by player that would pose a threat. """

        available_lines = self.available_lines(player)
        
        # NOTE Just return the list of cells? Would have to eliminate duplicates then.
        return list(map(lambda l: (l, self.empty_cells_in_line(l)), filter(lambda l: self.line_poses_potential_threat(l, player), available_lines)))

    def potential_double_threats(self, player):
        """ Return list of all potential moves by player that would pose a double threat. """
        
        potential_threats = self.potential_threats(player)

        potential_double_threats = []

        for i in range(len(potential_threats)):
            for j in range(i+1, len(potential_threats)):
                line1 = potential_threats[i][0]
                line2 = potential_threats[j][0]
                
                intersection_cell = self.line_intersection_cell(line1, line2)
                if intersection_cell is not None:
                    x, y = intersection_cell
                    if self.board[y][x] == EMPTY:
                        potential_double_threats.append((line1, line2, intersection_cell))

        return potential_double_threats

def empty_state():
    """ Create a blank game state. """

    return State(n_dim_matrix((BOARD_SIZE, BOARD_SIZE), fill=EMPTY))