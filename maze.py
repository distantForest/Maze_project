#!/usr/bin/env python
# widow class
import time
import random
from tkinter import Tk, Canvas
from collections import namedtuple
from enum import Enum, IntEnum
from fractions import Fraction

Lines = namedtuple("Lines", "top right bottom left")
Walls = namedtuple("Walls", "top right bottom left",
                   defaults=[True, True, True, True]
                   )


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opp_dir(self):
         return Direction((self.value+2) % 4)

    def rotate(self, step):
        return Direction((self.value+step) % 4)

    def deltas(self):
        dd = [0, -1], [1, 0], [0, 1], [-1, 0]
        return dd[self.value]
   
    
class Window:
    def __init__(self, width_, height_):
        self.root_widget = Tk()
        self.root_widget.title("Maze")
        self.canva = Canvas(self.root_widget, height=height_, width=width_)
        self.canva.pack()
        self.running = False
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)
        return

    def redraw(self):
        self.root_widget.update_idletasks()
        self.root_widget.update()
      
    def draw_line(self, line, fill_color="black"):
        line.draw(fill_color)

    def wait_for_close(self):
        self.running = True
        while self.running is True:
            self.redraw()
        self.canva.destroy()
        self.root_widget.destroy()

    def close(self):
        self.running = False

       
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

       
class Line:
    def __init__(self, point_1p=Point(0, 0), point_2p=Point(0, 0), win=None):
        self.point_1 = Point(point_1p.x, point_1p.y)
        self.point_2 = Point(point_2p.x, point_2p.y)
        self._win = win

    def draw(self, fill_p="black"):
        if self._win is not None:
            self._win.canva.create_line(
                self.point_1.x,
                self.point_1.y,
                self.point_2.x,
                self.point_2.y,
                fill=fill_p, width=2
            )
            self._win.canva.pack()

     
class Cell:
    def __init__(self,
                 _win_p=None,
                 b_c=Point(0, 0), e_c=Point(0, 0),
                 walls_p=Walls(True, True, True, True)
                 ):

        self.win = _win_p
        self.walls = Walls(*walls_p)
        point_0 = b_c
        point_1 = Point(e_c.x, b_c.y)
        point_2 = e_c
        point_3 = Point(b_c.x, e_c.y)
        side_x = e_c.x - b_c.x
        side_y = e_c.y - b_c.y
        self.center = Point(b_c.x + side_x // 2, b_c.y + side_y // 2)
        self.visited = False

        # Create named tuple of lines
        self.lines = Lines(left=Line(point_3, point_0, self.win),    # left wall   0 -- 1
                           top=Line(point_0, point_1, self.win),     # top wall    |    |
                           right=Line(point_1, point_2, self.win),   # right wall  3 -- 2
                           bottom=Line(point_2, point_3, self.win)   # bottom wall
                           )
        return
      
    def draw(self):
        for wall, line in zip(self.walls, self.lines):
            line.draw(fill_p="black" if wall is True else "gray")
            
        # mark cell center
        c_line_color = "green" if not self.visited else "yellow"
        c_line = Line(Point(self.center.x-5, self.center.y-5),
                      Point(self.center.x+5, self.center.y+5), self.win)
        c_line.draw(c_line_color)
        Line(Point(self.center.x-5, self.center.y+5),
             Point(self.center.x+5, self.center.y-5), self.win).draw(c_line_color)

    def draw_move(self, to_cell, undo=False):
        Line(self.center, to_cell.center, self.win).draw("grey" if undo else "red")


class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None
            ):
        random.seed(7)
        self._x = x1
        self._y = y1
        self._rows = num_rows
        self._colls = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = [[True for i in range(self._rows)] for j in range(self._colls)]
        self._create_cells()
        self._create_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
    def _create_cells(self):
        delta_x = self._cell_size_x + 3
        delta_y = self._cell_size_y + 3
        b_c_x = self._x
        e_c_x = b_c_x + self._cell_size_x
        for i in range(self._colls):
            b_c_y = self._y
            e_c_y = b_c_y + self._cell_size_y
            for j in range(self._rows):
                b_c = Point(b_c_x, b_c_y)
                e_c = Point(e_c_x, e_c_y)
                self._cells[i][j] = Cell(self._win, b_c, e_c)
                self._draw_cell(i, j)
                self._animate()
                b_c_y += delta_y
                e_c_y += delta_y
                
            b_c_x += delta_x
            e_c_x += delta_x
        return

    def _create_entrance_and_exit(self):
        r, c = self._rows-1, self._colls-1
        self._cells[0][0].walls = (False, True, True, False)
        self._draw_cell(0, 0)
        self._cells[c][r].walls = (True, False, False, True)
        self._draw_cell(c, r)

    def _break_walls_r(self, I_p, J_p):
        i, j = I_p, J_p
        the_cell = self._cells[i][j]
        
        while True:
            cells_to_visit = list()
            the_cell.visited = True
            # cells to visit
            if (j > 0) and not self._cells[i][j-1].visited:
                cells_to_visit.append((self._cells[i][j-1], Direction.UP, i, j-1))
            if (i > 0) and not self._cells[i-1][j].visited:
                cells_to_visit.append((self._cells[i-1][j], Direction.LEFT, i-1, j))
            if (j < (self._rows - 1)):
                if not self._cells[i][j+1].visited:
                    cells_to_visit.append((self._cells[i][j+1], Direction.DOWN, i, j+1))
            if (i < (self._colls - 1)):
                if not self._cells[i+1][j].visited:
                    cells_to_visit.append((self._cells[i+1][j], Direction.RIGHT, i+1, j))
                
            # check our pssibilities to move
            if len(cells_to_visit) == 0:
                # this is a dead end
                self._draw_cell(i, j)
                break
            
            # choose cell to move to
            cell_move_to, direction_move_to, i_r, j_r = random.choice(cells_to_visit)
            
            # knock down the wall in the current cell
            walls = list(the_cell.walls)
            walls[direction_move_to.value] = False
            the_cell.walls = Walls(*walls)
            the_cell.draw()
            
            # knock down the wall between in the target cell
            walls = list(cell_move_to.walls)
            walls[direction_move_to.opp_dir().value] = False
            cell_move_to.walls = Walls(*walls)
            cell_move_to.draw()
            self._animate()

            # dive into
            self._break_walls_r(i_r, j_r)
            continue
             
    def _draw_cell(self, Coll, Row):
        self._cells[Coll][Row].draw()
        return

    def _animate(self):
        if self._win is not None:
            self._win.redraw()
            time.sleep(0.05)

    def _reset_cells_visited(self):
        for c in self._cells:
            for x in c:
                x.visited = False
                x.draw()
                self._animate()

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, I_r, J_r):
        x, y = I_r, J_r
        colls, rows = self._colls, self._rows
        current_cell = self._cells[x][y]
        self._animate()
        current_cell.visited = True
        if (x == colls - 1) and (y == rows - 1):
            return True
        dx, dy = Fraction(colls, (x + 1)), Fraction(rows, (y + 1))
        
        # the magnet
        if dx >= dy:
            move_direction = Direction.RIGHT
            rotate = 1
        else:
            move_direction = Direction.DOWN
            rotate = -1

        for m in range(4):
            x_m = x + move_direction.deltas()[0]
            if x_m in range(colls):
                y_m = y + move_direction.deltas()[1]
                if y_m in range(rows):
                    move_to_cell = self._cells[x_m][y_m]
                    walls_exist = (current_cell.walls[move_direction]
                                   or move_to_cell.walls[move_direction.opp_dir()]
                                   or move_to_cell.visited
                                   )

                    if not walls_exist:
                        current_cell.draw_move(move_to_cell)
                        if self._solve_r(x_m, y_m):
                            return True
                        else:
                            current_cell.draw_move(move_to_cell, True)
            move_direction = move_direction.rotate(rotate)
            
        return False
    
               
if __name__ == "__main__":
    def main():
    
        win = Window(800, 600)
        a = Maze(100, 1, 10, 15, 24, 24, win)
        a.solve()
        
        win.wait_for_close()


    main()
    
