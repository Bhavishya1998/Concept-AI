from state import State, X, O, EMPTY, BOARD_SIZE
from state_operations import next_state

from debug import print_board

class Node:

    def __init__(self, state: State, flip_vertical=False, flip_horizontal=False):
        self.state = state
        self.children = {}
        self.flip_vertical = flip_vertical
        self.flip_horizontal = flip_horizontal
        self.value = None

    def generate_children(self):
        """ Generate all child nodes of this node (Forward Propagation). """

        possible_moves = self.state.possible_moves()

        for move in possible_moves:
            self.children[move] = Node(next_state(self.state, move))

    def assured_result(self):
        """ Return True if this state leads to an assured conclusion, otherwise False. """

        return (self.state.win_probs[X] == 0.0 or self.state.win_probs[X] == 1.0) and \
               (self.state.win_probs[O] == 0.0 or self.state.win_probs[O] == 1.0)

    def assured_value(self):
        """ Return node value in case of an assured result. """

        return self.state.win_probs

    def calculate_value(self):
        """ Calculate the value of this node using the values of all children nodes (Backward Propagation). """

        # TODO define value function
        return {
            X: sum(map(lambda n: n.value[X], self.children.values())) / len(self.children), 
            O: sum(map(lambda n: n.value[O], self.children.values())) / len(self.children)
        }

    def generate_subtree(self, depth=None):
        """
        Recursively generate the subtree below this node of the desired depth and return the result. 
        A depth of None generates the entire subtree.
        """

        if depth is None or depth > 0:
            if self.assured_result():
                self.value = self.assured_value()

            else:
                self.generate_children()

                for move in self.children:
                    self.children[move].generate_subtree((None if depth is None else depth-1))

                self.value = self.calculate_value()

            # DEBUG
            # if self.value[X] != 0.0 and self.value[O] != 0.0:
            # print_board(self.state)
            # print(self.value)
            # print()

            return self.value
        else:

            # TODO this makes depth unusable
            return None

    def select_next(self):
        """ Return the best possible move based on the defined selection algorithm. """

        player = self.state.next_to_move
        other_player = self.state.other_player(player)

        moves = list(self.children.keys())
        
        best_move = moves[0]
        for move in moves:
            if self.children[move].value[player] - self.children[move].value[other_player] > \
             self.children[best_move].value[player] - self.children[best_move].value[other_player]:
                best_move = move

        return best_move
