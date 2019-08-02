from identify_threats import State, ROW, COL, DIAG, X, O, EMPTY
import unittest

class ThreatDetectionTest(unittest.TestCase):
    
    def test_find_threat(self):
        
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
        self.assertEqual(state.existing_threats(X), [(COL, 0)])
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
        self.assertEqual(state.existing_threats(O), [(DIAG, 0)])

        board = [
            [O, EMPTY, X],
            [O, X, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.existing_threats(X), [(DIAG, 1)])
        self.assertEqual(state.existing_threats(O), [(COL, 0)])

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
        self.assertEqual(state.double_threats(O), [(ROW, 0), (DIAG, 0)])

    def test_potential_threats(self):
        
        board = [
            [X, O, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.potential_threats(X), [((COL, 0), [(0, 1), (0, 2)])])

        board = [
            [O, EMPTY, X],
            [X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.potential_threats(O), [((DIAG, 0), [(1, 1), (2, 2)])])

    def test_potential_double_threats(self):
        
        board = [
            [X, EMPTY, EMPTY],
            [O, O, EMPTY],
            [EMPTY, EMPTY, X]
        ]
        state = State(board)
        self.assertEqual(state.potential_double_threats(X), [(2, 0)])

        board = [
            [X, X, EMPTY],
            [O, EMPTY, O],
            [EMPTY, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.potential_double_threats(X), [(1, 1)])

        board = [
            [X, EMPTY, EMPTY],
            [O, X, EMPTY],
            [O, EMPTY, EMPTY]
        ]
        state = State(board)
        self.assertEqual(state.potential_double_threats(X), [(1, 0)])

if __name__ == "__main__":
    unittest.main()