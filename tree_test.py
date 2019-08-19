from state import State, X, O, EMPTY
from tree import Node

import unittest

class TreeTest(unittest.TestCase):

    def test_tree_generation_and_calculate_value(self):
        
        board = [
            [O, O, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, X, EMPTY]
        ]
        state = State(board, next_to_move=X)
        node = Node(state)
        node.generate_subtree()
        self.assertAlmostEqual(node.value[X], 0.0, 2)
        self.assertAlmostEqual(node.value[O], 0.0, 2)

        board = [
            [EMPTY, O, EMPTY],
            [O, X, EMPTY],
            [EMPTY, X, EMPTY]
        ]
        state = State(board, next_to_move=X)
        node = Node(state)
        node.generate_subtree()
        self.assertAlmostEqual(node.value[X], 1.0, 2)
        self.assertAlmostEqual(node.value[O], 0.0, 2)

        board = [
            [EMPTY, O, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, X, EMPTY]
        ]
        state = State(board, next_to_move=O)
        node = Node(state)
        node.generate_subtree()
        self.assertAlmostEqual(node.value[X], 0.33, 2)
        self.assertAlmostEqual(node.value[O], 0.0, 2)

        board = [
            [EMPTY, EMPTY, X],
            [EMPTY, X, EMPTY],
            [O, O, EMPTY]
        ]
        state = State(board, next_to_move=X)
        node = Node(state)
        node.generate_subtree()
        self.assertAlmostEqual(node.value[X], 1.0, 2)
        self.assertAlmostEqual(node.value[O], 0.0, 2)

        board = [
            [O, EMPTY, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, EMPTY, X]
        ]
        state = State(board, next_to_move=O)
        node = Node(state)
        node.generate_subtree()
        self.assertAlmostEqual(node.value[X], 0.67, 2)
        self.assertAlmostEqual(node.value[O], 0.0, 2)



if __name__ == "__main__":
    unittest.main()