from functools import reduce
import pandas as pd

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

    def __init__(self, board, next_to_move=None, calc_vectors=True):
        
        self.board = board
        if next_to_move is None:
            # if next_to_move is None, infer the next player from the board, assuming that  goes first
            self.next_to_move = X if len(self.empty_cells()) % 2 == 1 else O
        else:
            self.next_to_move = next_to_move

        self.win_probs = {X: None, O: None}
        self.state_vectors = {}
        self.count_state_vectors = pd.DataFrame(index=[X, O], columns=[
            "unoccupied", 
            "occupied", 
            "attack", 
            "available", 
            "killed",
            "uu", 
            "ou", 
            "oo"
        ])

        self.horizontal_symmetry = self._has_horizontal_symmetry()
        self.vertical_symmetry = self._has_vertical_symmetry()

        if calc_vectors:
            self._calc_products()
            self.calc_state_vector(X)
            self.calc_state_vector(O)

            # NOTE should this be called?
            self.assign_probs()

    def _reflection_in_vertical(self, cell):
        """ Return the reflection of cell in the vertical line bisecting the board. """

        x, y = cell
        return BOARD_SIZE - x - 1, y

    def _reflection_in_horizontal(self, cell):
        """ Return the reflection of cell in the horizontal line bisecting the board. """

        x, y = cell
        return x, BOARD_SIZE - y - 1

    def _has_vertical_symmetry(self):
        """ Return True if the board is symmetrical about the vertical line bisecting it. """

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE // 2):
                opposite_x, opposite_y = self._reflection_in_vertical((x, y))
                if self.board[y][x] != self.board[opposite_y][opposite_x]:
                    return False

        return True

    def _has_horizontal_symmetry(self):
        """ Return True if the board is symmetrical about the horizontal line bisecting it. """

        for y in range(BOARD_SIZE // 2):
            for x in range(BOARD_SIZE):
                opposite_x, opposite_y = self._reflection_in_horizontal((x, y))
                if self.board[y][x] != self.board[opposite_y][opposite_x]:
                    return False

        return True

    def _other_corners(self, corner_cell):
        """ Take a corner cell and return a list of the other three corner cells. """

        return [
            self._reflection_in_horizontal(corner_cell),
            self._reflection_in_vertical(corner_cell),
            self._reflection_in_horizontal(self._reflection_in_vertical(corner_cell))
        ]

    def other_player(self, player):
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

        other_player = self.other_player(player)

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

        self.state_vectors[player] = {
            "unoccupied": unoccupied, 
            "occupied": occupied, 
            "attack": attack, 
            "available": available, 
            "killed": killed, 
            "uu": uu, 
            "ou": ou, 
            "oo": oo
        }
        self.count_state_vectors.loc[player] = [len(value) for value in self.state_vectors[player].values()]

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

        other_player = self.other_player(player)
        indices = [i for i in range(NUM_LINES)]

        return list(filter(lambda x: x is not None , map(lambda l, i: i if l % other_player != 0 else None, self.line_prods, indices)))

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

    def empty_cells(self):
        """ Return list of all empty cells on board. """

        return list(reduce(lambda x, y: x + y, [self.empty_cells_in_line(row) for row in range(BOARD_SIZE)], []))

    def line_poses_potential_threat(self, line, player):
        """ Return true if player poses potential threat on the line. """

        other_player = self.other_player(player)
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

    def possible_moves(self):
        """ Return all possible moves for the current player. """

        # TODO treat mirror states as one
        player = self.next_to_move
        other_player = self.other_player(player)

        player_count_state_vector = self.count_state_vectors.loc[player]
        other_player_count_state_vector = self.count_state_vectors.loc[other_player]

        player_attack_count = player_count_state_vector["attack"]

        # NOTE will symmetry analysis mess these up?
        if player_attack_count > 0:

            # return winning move if available
            return [attack[1] for attack in self.state_vectors[player]["attack"]]

        other_player_attack_count = other_player_count_state_vector["attack"]

        if other_player_attack_count > 0:

            # stop threats from opponent
            return [attack[1] for attack in self.state_vectors[other_player]["attack"]]

        # TODO refactor
        # Cells which can be ignored because of symmetry. Only one mirrored cell is considered.
        if self.horizontal_symmetry and self.vertical_symmetry:
            # if the board has both horizontal and vertical symmetry, then all corner cells are equivalent
            symmetry_ignore_cells = self._other_corners((0, 0))
        else:
            symmetry_ignore_cells = []

        possib_cells = []

        for cell in self.empty_cells():
            if cell not in symmetry_ignore_cells:
                if self.vertical_symmetry:
                    symmetry_ignore_cells.append(self._reflection_in_vertical(cell))
                if self.horizontal_symmetry:
                    symmetry_ignore_cells.append(self._reflection_in_horizontal(cell))

                possib_cells.append(cell)

        return possib_cells
                    

    def assign_probs(self):
        """
        Assign winning probabilities if a decision is certain, otherwise assign None.
        """

        player = self.next_to_move
        other_player = self.other_player(player)

        player_count_state_vector = self.count_state_vectors.loc[player]
        other_player_count_state_vector = self.count_state_vectors.loc[other_player]

        count_other_player_attacks = other_player_count_state_vector["attack"]

        count_oo = player_count_state_vector["oo"]
        # TODO Can this condition be improved? 
        if count_oo > 0 and \
           (count_other_player_attacks == 0 or \
              (count_other_player_attacks == 1 and \
                  self.state_vectors[other_player]["attack"][0][1] in [intersection[2] for intersection in self.state_vectors[player]["oo"]])):
              # player might be forced into playing a double threat, so that must be checked too

            # a player wins if he is about to play an o-o intersection
            self.win_probs[player] = 1.0
            self.win_probs[other_player] = 0.0
            return

        player_count_available = player_count_state_vector["available"]
        if player_count_available <= 2:
            # if a player has less than three available lines then he can't win
            self.win_probs[player] = 0.0

        other_player_count_available = other_player_count_state_vector["available"]
        if other_player_count_available <= 3:
            # if a player has less than 4 available lines and the opponent is about to play, then he can't win
            self.win_probs[other_player] = 0.0

    def game_over(self):
        """ Return True if the game is over, otherwise False. """

        x_win = X ** BOARD_SIZE
        o_win = O ** BOARD_SIZE

        for line_prod in self.line_prods:
            if line_prod == x_win or line_prod == o_win:
                # someone won
                return True

        if len(self.empty_cells()) == 0:
            # the board is full and no one won, a draw
            return True
        
        return False