from state import State, X, O, EMPTY
from state_operations import next_state

import unittest

class StateOperationsTest(unittest.TestCase):
    
    def test_next_state(self):
        
        board = [
            [X, O, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board, next_to_move=X)
        move = (1, 1)
        next_board = [
            [X, O, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        new_state = next_state(state, move)
        self.assertEqual(new_state.board, next_board)
        self.assertEqual(new_state.next_to_move, O)

if __name__ == "__main__":
    unittest.main()