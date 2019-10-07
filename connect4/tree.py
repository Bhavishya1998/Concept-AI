from state import State
from state_operations import move

class Node:

    def __init__(self, state: State):
        self.state = state
        self.children = []

    def create_children(self):
        """ Create list of all children of this node. """

        moves = self.state.possible_moves()

        self.children = [Node(move(self.state, c)) for _, c in moves]

    def create_subtree(self, level):
        
        if level <= 0:
            return

        self.create_children()

        for child in self.children:
            child.create_subtree(level-1)