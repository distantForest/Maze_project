#!/usr/bin/env python
# widow class
from tkinter import Tk, Canvas
from collections import namedtuple


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
        line.draw(self.canva, fill_color)

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
    def __init__(self, point_1p=Point(0, 0), point_2p=Point(0, 0)):
        self.point_1 = Point(point_1p.x, point_1p.y)
        self.point_2 = Point(point_2p.x, point_2p.y)

    def draw(self, canva, fill_p="black"):
        canva.create_line(
            self.point_1.x,
            self.point_1.y,
            self.point_2.x,
            self.point_2.y,
            fill=fill_p, width=2
            )
        canva.pack()

     
class Cell:
    def __init__(self,
                 _win_p,
                 b_c=Point(0, 0), e_c=Point(0, 0),
                 walls_p=(True, True, True, True)
                 ):
        Walls = namedtuple("Walls", "top right bottom left",
                                    defaults=[True, True, True, True]
                           )
        self.win = _win_p
        self.walls = Walls(*walls_p)
        point_0 = b_c
        point_1 = Point(e_c.x, b_c.y)
        point_2 = e_c
        point_3 = Point(b_c.x, e_c.y)
        # Create named tuple of lines
        Lines = namedtuple("Lines", "top right bottom left")
        self.lines = Lines(left=Line(point_3, point_0),    # left wall
                           top=Line(point_0, point_1),     # top wall
                           right=Line(point_1, point_2),   # right wall
                           bottom=Line(point_2, point_3)   # bottom wall
                           )
      
    def draw(self):
        for wall, line in zip(self.walls, self.lines):
            if wall is True:
                line.draw(self.win.canva)
               

def main():
  
    win = Window(800, 600)
    line_1 = Line(Point(10, 10), Point(20, 100))
    line_2 = Line(Point(20, 20), Point(800 - 20, 600 - 20))
    win.draw_line(line_1, "black")
    win.draw_line(line_2, "red")
    cell1 = Cell(win, Point(15, 15), Point(45, 45))
    cell1.draw()
    cell2 = Cell(win, Point(50, 15), Point(80, 45), (True, False, True, False))
    cell2.draw()

    win.wait_for_close()

   
main()
