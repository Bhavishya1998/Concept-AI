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

        self.assertEqual(s._r2l_diag_lines_of_cell((2, 2)), [46, 47])
        self.assertEqual(s._r2l_diag_lines_of_cell((0, 3)), [45])
        self.assertEqual(s._r2l_diag_lines_of_cell((4, 0)), [47])
        self.assertEqual(s._r2l_diag_lines_of_cell((5, 3)), [56])
        self.assertEqual(s._r2l_diag_lines_of_cell((3, 3)), [51, 52, 53])
        self.assertEqual(s._r2l_diag_lines_of_cell((0, 0)), [])
        self.assertEqual(s._r2l_diag_lines_of_cell((0, 2)), [])
        self.assertEqual(s._r2l_diag_lines_of_cell((5, 4)), [])
        self.assertEqual(s._r2l_diag_lines_of_cell((5, 6)), [])

if __name__ == "__main__":
    unittest.main()