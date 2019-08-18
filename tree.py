from state import State, X, O, EMPTY, BOARD_SIZE
from state_operations import next_state

class Node:

    def __init__(self, state: State):
        self.state = state
        self.children = {}
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

        # TODO define value function
        return False

    def calculate_value(self, children_values: dict):
        """ Calculate the value of this node using the values of all children nodes (Backward Propagation). """

        # TODO define value function
        return False

    def generate_subtree(self):
        """ Recursively generate the subtree below this node and return the result. """

        if self.assured_result():
            self.value = self.assured_value()

        else:
            self.generate_children()

            # NOTE should children_values be saved?
            children_values = {}
            for move in self.children:
                children_values[move] = self.children[move].generate_subtree()

            self.value = self.calculate_value(children_values)

        return self.value
