from identify_threats import State, X, O, EMPTY
import unittest

class ThreatDetectionTest(unittest.TestCase):
    
    def test_exisitng_threats(self):
        
        board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.existing_threats(X), [])
        self.assertEqual(state.existing_threats(O), [])

        board = [
            [X, O, O],
            [X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.existing_threats(X), [3])
        self.assertEqual(state.existing_threats(O), [])

        board = [
            [O, O, O],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.existing_threats(O), [])

        board = [
            [X, EMPTY, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.existing_threats(X), [])
        self.assertEqual(state.existing_threats(O), [])

        board = [
            [O, X, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.existing_threats(O), [6])

        board = [
            [O, EMPTY, X],
            [O, X, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.existing_threats(X), [7])
        self.assertEqual(state.existing_threats(O), [3])

        board = [
            [X, EMPTY, EMPTY],
            [O, X, EMPTY],
            [O, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.existing_threats(X), [6])

    def test_double_threat(self):
        
        board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.double_threats(X), [])
        self.assertEqual(state.double_threats(O), [])

        board = [
            [O, EMPTY, O],
            [X, EMPTY, X],
            [X, EMPTY, O]
        ]
        state = State(board)
        self.assertEqual(state.double_threats(X), [])
        self.assertEqual(state.double_threats(O), [0, 6])

    def test_available_lines(self):
        
        board = [
            [X, EMPTY, EMPTY],
            [O, EMPTY, O],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.available_lines(X), [0, 2, 4, 6, 7])
        self.assertEqual(state.available_lines(O), [1, 2, 4, 5, 7])

    def test_cells_in_line(self):
        
        board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.cells_in_line(1), [(0, 1), (1, 1), (2, 1)])
        self.assertEqual(state.cells_in_line(3), [(0, 0), (0, 1), (0, 2)])
        self.assertEqual(state.cells_in_line(6), [(0, 0), (1, 1), (2, 2)])
        self.assertEqual(state.cells_in_line(7), [(0, 2), (1, 1), (2, 0)])

    def test_potential_threats(self):
        
        board = [
            [X, O, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.potential_threats(X), [(3, [(0, 1), (0, 2)])])

        board = [
            [O, EMPTY, X],
            [X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.potential_threats(O), [(6, [(1, 1), (2, 2)])])

    def test_potential_double_threats(self):
        
        board = [
            [X, EMPTY, EMPTY],
            [O, O, EMPTY],
            [EMPTY, EMPTY, X]
        ]
        state = State(board)
        self.assertEqual(state.potential_double_threats(X), [(0, 5, (2, 0))])

        # NOTE triple threats count as a single double threat instead of three double threats. Is this okay?    
        board = [
            [X, X, EMPTY],
            [O, EMPTY, O],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.potential_double_threats(X), [(4, 6, (1, 1))])

        board = [
            [X, EMPTY, EMPTY],
            [O, X, EMPTY],
            [O, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.potential_double_threats(X), [(0, 4, (1, 0))])

    def test_state_vector(self):

        board = [
            [EMPTY, O, EMPTY],
            [EMPTY, X, EMPTY],
            [O, X, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.count_state_vector(X), [1, 2, 0, 3, 5, 0, 2, 0])
        self.assertEqual(state.count_state_vector(O), [1, 2, 0, 3, 5, 0, 1, 1])

        board = [
            [X, O, EMPTY],
            [EMPTY, X, EMPTY],
            [O, X, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.count_state_vector(X), [1, 2, 1, 3, 5, 0, 2, 0])
        self.assertEqual(state.count_state_vector(O), [1, 0, 0, 1, 7, 0, 0, 0])

        board = [
            [EMPTY, O, X],
            [EMPTY, X, EMPTY],
            [O, X, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.count_state_vector(X), [0, 3, 0, 3, 5, 0, 0, 2])
        self.assertEqual(state.count_state_vector(O), [0, 1, 0, 1, 7, 0, 0, 0])

        board = [
            [EMPTY, O, EMPTY],
            [X, X, O],
            [O, X, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.count_state_vector(X), [0, 1, 0, 1, 7, 0, 0, 0])
        self.assertEqual(state.count_state_vector(O), [0, 2, 0, 2, 6, 0, 0, 1])

if __name__ == "__main__":
    unittest.main()