#!/usr/bin/env python
# widow class
import time
from tkinter import Tk, Canvas
from collections import namedtuple

Lines = namedtuple("Lines", "top right bottom left")
Walls = namedtuple("Walls", "top right bottom left",
                   defaults=[True, True, True, True]
                   )


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

        # Create named tuple of lines
        self.lines = Lines(left=Line(point_3, point_0, self.win),    # left wall   0 -- 1
                           top=Line(point_0, point_1, self.win),     # top wall    |    |
                           right=Line(point_1, point_2, self.win),   # right wall  3 -- 2
                           bottom=Line(point_2, point_3, self.win)   # bottom wall
                           )
        return
      
    def draw(self):
        for wall, line in zip(self.walls, self.lines):
            if wall is True:
                line.draw()
        c_line = Line(Point(self.center.x-5, self.center.y-5),
                      Point(self.center.x+5, self.center.y+5), self.win)
        c_line.draw("green")
        Line(Point(self.center.x-5, self.center.y+5),
             Point(self.center.x+5, self.center.y-5), self.win).draw("green")

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
        self._x = x1
        self._y = y1
        self._rows = num_rows
        self._colls = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = [[True for i in range(self._rows)] for j in range(self._colls)]
        self._create_cells()

    def _create_cells(self):
        for i in range(self._colls):
            for j in range(self._rows):
                b_c = Point(self._x+self._cell_size_x*i,
                            self._y+self._cell_size_y*j
                            )
                e_c = Point(self._x+self._cell_size_x*(i+1),
                            self._y+self._cell_size_y*(j+1)
                            )
                self._cells[i][j] = Cell(self._win, b_c, e_c)
                self._draw_cell(i, j)
                self._animate()
        return

    def _create_entrance_and_exit(self):
        self._cells[0][0].walls = (False, False, False, False)

    def _draw_cell(self, Coll, Row):
        self._cells[Coll][Row].draw()
        return

    def _animate(self):
        if self._win is not None:
            self._win.redraw()
            time.sleep(0.1)
    
               
if __name__ == "__main__":
    def main():
    
        win = Window(800, 600)
        line_1 = Line(Point(10, 10), Point(20, 100), win)
        line_2 = Line(Point(20, 20), Point(800 - 20, 600 - 20), win)
        win.draw_line(line_1, "black")
        win.draw_line(line_2, "red")
        cell1 = Cell(win, Point(15, 15), Point(45, 45))
        cell1.draw()
        cell2 = Cell(win, Point(50, 15), Point(80, 45), (True, False, True, False))
        cell2.draw()
        cell3 = Cell(win, Point(15, 150), Point(45, 195))
        cell3.draw()
        cell4 = Cell(win, Point(70, 95), Point(110, 135), (True, False, True, False))
        cell4.draw()
        
        cell4.draw_move(cell1)
        cell2.draw_move(cell3,True)

        a  = Maze(1, 1, 10, 15, 24, 24, win)
        win.wait_for_close()

   
    main()
