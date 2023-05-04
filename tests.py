import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
            )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
            )
        visited = True
        for i in range(num_cols):
            for j in range(num_rows):
                visited = visited and m1._cells[i][j].visited
                if not visited:
                    break
        self.assertEqual(
            False,
            visited,
            "There are some cells visited"
            )

        
if __name__ == "__main__":
    unittest.main()
            
