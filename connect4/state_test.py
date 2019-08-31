from state import State

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

if __name__ == "__main__":
    unittest.main()