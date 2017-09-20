'''
Author : Kevin Wu
This program plays the game go
It has a goSquare class, a goGrid class, and a goFrame class.
The goSquare is an individual square from the goGame which has an attribute
for its position and color. It has methods for drawing a circle and removing one.

The goGrid contains all of the goSquares and also handles making moves and the UI

The goFrame handles all of the logic and end of game stuff.

'''
from tkinter import *
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle
class goSquare(Canvas):
    def __init__(self, position, master):
        self.master=master
        (self.row, self.col)=position
        self.position=position
        Canvas.__init__(self, master, width=30, height=30, highlightthickness=0)
        self.create_line(0, 15, 30, 15)
        self.create_line(15,0,15,30)
        self.color=None
        self.bind("<Button-1>", master.get_click)
    def make_piece(self, color):
        self.color=color
        self.piece=self.create_circle(15,15,13, fill=color)
    def clear(self):
        self.delete(self.piece)

class goGrid(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        squares={}
        for i in range(10):
            for x in range(10):
                squares[(i,x)]=goSquare((i,x), self)
                squares[(i,x)].grid(row=i, column=x, sticky=N+S+E+W)
                squares[(i,x)].make_piece("white")
        for i in range(10):
            Grid.rowconfigure(self, i, weight=1)
            Grid.columnconfigure(self, i, weight=1)
    def get_click(self, event):
        event.widget.clear()

bob=Tk()
goGrid(bob).grid(sticky=N+S+E+W, row=0, column=0)
Grid.rowconfigure(bob, 0, weight=1)
Grid.columnconfigure(bob, 0, weight=1)
bob.mainloop()
