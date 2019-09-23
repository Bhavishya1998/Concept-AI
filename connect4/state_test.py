from state import State, RED, YELLOW, AVAILABLE, UNAVAILABLE, ATTACK, DOUBLE, SINGLE
from state_operations import empty_state, move

import unittest

class StateTest(unittest.TestCase):

    def test_row_lines_of_cell(self):
        
        s = State(None, None)

        self.assertEqual(s._row_lines_of_cell((0, 2)), [2, 1, 0])
        self.assertEqual(s._row_lines_of_cell((0, 3)), [3, 2, 1, 0])
        self.assertEqual(s._row_lines_of_cell((0, 6)), [3])
        self.assertEqual(s._row_lines_of_cell((3, 2)), [14, 13, 12])

    def test_col_lines_of_cell(self):
        
        s = State(None, None)

        self.assertEqual(s._col_lines_of_cell((2, 0)), [26, 25, 24])
        self.assertEqual(s._col_lines_of_cell((2, 2)), [32, 31, 30])
        self.assertEqual(s._col_lines_of_cell((5, 6)), [44])

    def test_r2l_diag_lines_of_cell(self):
        
        s = State(None, None)

        # right to left
        self.assertEqual(s._diag_lines_of_cell((2, 2), r2l=True), [46, 47])
        self.assertEqual(s._diag_lines_of_cell((0, 3), r2l=True), [45])
        self.assertEqual(s._diag_lines_of_cell((4, 0), r2l=True), [47])
        self.assertEqual(s._diag_lines_of_cell((5, 3), r2l=True), [56])
        self.assertEqual(s._diag_lines_of_cell((3, 3), r2l=True), [51, 52, 53])
        self.assertEqual(s._diag_lines_of_cell((0, 0), r2l=True), [])
        self.assertEqual(s._diag_lines_of_cell((0, 2), r2l=True), [])
        self.assertEqual(s._diag_lines_of_cell((5, 4), r2l=True), [])
        self.assertEqual(s._diag_lines_of_cell((5, 6), r2l=True), [])

        # left to right
        self.assertEqual(s._diag_lines_of_cell((1, 3), r2l=False), [58, 59])
        self.assertEqual(s._diag_lines_of_cell((0, 0), r2l=False), [63])
        self.assertEqual(s._diag_lines_of_cell((2, 2), r2l=False), [63, 64, 65])
        self.assertEqual(s._diag_lines_of_cell((4, 4), r2l=False), [64, 65])
        self.assertEqual(s._diag_lines_of_cell((2, 0), r2l=False), [68])
        self.assertEqual(s._diag_lines_of_cell((0, 6), r2l=False), [])
        self.assertEqual(s._diag_lines_of_cell((5, 2), r2l=False), [])

    def test_line_to_cells(self):
        
        s = State(None, None)

        # rows
        self.assertEqual(s.line_to_cells(0), [(0, 0), (0, 1), (0, 2), (0, 3)])
        self.assertEqual(s.line_to_cells(2), [(0, 2), (0, 3), (0, 4), (0, 5)])
        self.assertEqual(s.line_to_cells(23), [(5, 3), (5, 4), (5, 5), (5, 6)])

        # cols
        self.assertEqual(s.line_to_cells(24), [(0, 0), (1, 0), (2, 0), (3, 0)])
        self.assertEqual(s.line_to_cells(26), [(2, 0), (3, 0), (4, 0), (5, 0)])
        self.assertEqual(s.line_to_cells(44), [(2, 6), (3, 6), (4, 6), (5, 6)])

        # r2l diags
        self.assertEqual(s.line_to_cells(45), [(0, 3), (1, 2), (2, 1), (3, 0)])
        self.assertEqual(s.line_to_cells(47), [(1, 3), (2, 2), (3, 1), (4, 0)])
        self.assertEqual(s.line_to_cells(56), [(2, 6), (3, 5), (4, 4), (5, 3)])
        self.assertEqual(s.line_to_cells(50), [(2, 3), (3, 2), (4, 1), (5, 0)])

        # l2r diags
        self.assertEqual(s.line_to_cells(57), [(0, 3), (1, 4), (2, 5), (3, 6)])
        self.assertEqual(s.line_to_cells(60), [(0, 1), (1, 2), (2, 3), (3, 4)])
        self.assertEqual(s.line_to_cells(61), [(1, 2), (2, 3), (3, 4), (4, 5)])
        self.assertEqual(s.line_to_cells(68), [(2, 0), (3, 1), (4, 2), (5, 3)])

    def test_line_status(self):
        
        state = empty_state()
        state = move(move(move(state, 2), 3), 2)

        self.assertEqual(state.line_status(0, YELLOW), AVAILABLE)
        self.assertEqual(state.line_status(0, RED), AVAILABLE)
        self.assertEqual(state.line_status(31, YELLOW), SINGLE)
        self.assertEqual(state.line_status(32, YELLOW), DOUBLE)
        self.assertEqual(state.line_status(21, YELLOW), UNAVAILABLE)
        self.assertEqual(state.line_status(21, RED), UNAVAILABLE)
        self.assertEqual(state.line_status(23, RED), SINGLE)
        self.assertEqual(state.line_status(56, RED), SINGLE)
        self.assertEqual(state.line_status(56, YELLOW), UNAVAILABLE)
        self.assertEqual(state.line_status(55, YELLOW), SINGLE)
        self.assertEqual(state.line_status(68, RED), UNAVAILABLE)

    def test_line_future_state(self):
        
        # board used in case study 4 email thread
        state = move(move(move(move(move(move(move(move(move(move(move(move(move(empty_state(), 5), 3), 5), 3), 6), 6), 0), 6), 0), 5), 0), 0), 4)

        self.assertEqual(state.line_future_state(17), [(5, 1), (5, 2)])
        self.assertEqual(state.line_future_state(14), [(4, 2), (4, 4)])
        self.assertEqual(state.line_future_state(15), [(4, 4)])
        self.assertEqual(state.line_future_state(27), [])
        self.assertEqual(state.line_future_state(57), [(1, 3), (2, 4)])
        self.assertEqual(state.line_future_state(56), [])

    def test_line_intersection_cells(self):
        
        state = empty_state()

        self.assertEqual(state.line_intersection_cells(0, 1), [(0, 1), (0, 2), (0, 3)])
        self.assertEqual(state.line_intersection_cells(27, 1), [(0, 1)])
        self.assertEqual(state.line_intersection_cells(27, 2), [])
        self.assertEqual(state.line_intersection_cells(46, 58), [(1, 3)])

    def test_double_threats_intersections(self):
        pass
        # TODO add tests        

if __name__ == "__main__":
    unittest.main()