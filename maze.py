#!/usr/bin/env python
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width_, height_):
        self.root_widget = Tk()
        self.root_widget.title("Maze")
        self.canva = Canvas(self.root_widget, height = height_, width = width_)
        self.canva.pack()
        self.running = False
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)
        return

    def redraw(self):
        self.root_widget.update_idletasks()
        self.root_widget.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()
        self.canva.destroy()
        self.root_widget.destroy()

    def close(self):
        self.running = False

def main():
    win = Window(800, 600)
    win.wait_for_close()

main()

