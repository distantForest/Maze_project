#!/usr/bin/env python
# widow class
from tkinter import Tk, Canvas


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
        print(self.point_1.x)
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
                  b_c = Point(0, 0), e_c = Point(0, 0),
                 walls_p = namedtuple("Walls", ['left', 'top', 'right', 'bottom'] ,defaults = "True, True, True, True"),
                 # has_left_wall_p = True,
                 # has_right_wall_p = True,
                 # has_top_wall_p = True,
                 # has_bottom_wall_p = True,
                 # _x1_p = 0, _x2_p = 0, _y1_p = 0, _y2_p = 0
                 ):
        self.walls = walls_p
        has_left_wall = has_left_wall_p
        has_right_wall = has_right_wall_p
        has_top_wall = has_top_wall_p
        has_bottom_wall = has_bottom_wall_p
        _x1_p, _x2_p, _y1_p, _y2 = _x1_p, _x2_p, _y1_p, _y2_p
    def draw(self,):
        begin_corner = b_c
        end_corner = e_c
        for wall in self.walls
        self.has_


class Point:
     def __init__(self, x=0, y=0):
         self.x = x

def main():
   
    win = Window(800, 600)
    line_1 = Line(Point(10, 10), Point(20, 100))
    line_2 = Line(Point(20, 20), Point(800 - 20, 600 - 20))
    win.draw_line(line_1, "black")
    win.draw_line(line_2, "red")

    win.wait_for_close()

    
main()
