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
def set_aspect(content_frame, pad_frame, aspect_ratio):
    # a function which places a frame within a containing frame, and
    # then forces the inner frame to keep a specific aspect ratio

    def enforce_aspect_ratio(event):
        # when the pad window resizes, fit the content into it,
        # either by fixing the width or the height and then
        # adjusting the height or width based on the aspect ratio.

        # start by using the width as the controlling dimension
        desired_width = event.width
        desired_height = int(event.width / aspect_ratio)

        # if the window is too tall to fit, use the height as
        # the controlling dimension
        if desired_height > event.height:
            desired_height = event.height
            desired_width = int(event.height * aspect_ratio)
        desired_height=desired_height//10*10
        desired_width=desired_width//10*10
        # place the window, giving it an explicit size
        content_frame.place(in_=pad_frame, x=0, y=0, 
            width=desired_width, height=desired_height)

    pad_frame.bind("<Configure>", enforce_aspect_ratio)
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
        self.bind("<Configure>", self.on_resize)
    def make_piece(self, color):
        if color==None:
            return
        self.color=color
        self.piece=self.create_circle(self.winfo_width()/2,self.winfo_width()/2,self.winfo_width()*13/30, fill=color)
    def clear(self):
        self.delete(self.piece)
        self.color=None
    def on_resize(self,event):
        self.delete("all")
        self.create_line(0,self.winfo_width()/2, self.winfo_height(),self.winfo_width()/2)
        self.create_line(self.winfo_height()/2, 0,self.winfo_height()/2,self.winfo_width())
        self.make_piece(self.color)

class goGrid(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        squares={}
        for i in range(10):
            for x in range(10):
                squares[(i,x)]=goSquare((i,x), self)
                squares[(i,x)].grid(row=i, column=x, sticky=N+S+E+W)
                #squares[(i,x)].make_piece("white")
        for i in range(10):
            Grid.rowconfigure(self, i, weight=1)
            Grid.columnconfigure(self, i, weight=1)
        self.master=master
    def get_click(self, event):
        #event.widget.clear()
        self.master.get_click(event)

class goFrame(Frame):
    def __init__(self):
        self.master=Tk()
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        Frame.__init__(self, self.master)
        self.grid(row=0, column=0, sticky="nsew")
        self.goGrid=goGrid(self)
        set_aspect(self.goGrid, self, 1.0)
        self.master.geometry('300x300')
        self.turn=0 #white is 0 black is 1
        self.strSquares={}
        for i in range(10):
            for x in range(10):
                self.strSquares[(i,x)]=""
        self.event=None
        self.errorVar=StringVar()
        self.errorMessage = Label(self.master, textvariable=self.errorVar)
        self.errorMessage.grid()
        self.liberties=[]
        self.master.mainloop()
    def get_click(self, event):
        self.event=event
        print(event.widget.position)
        if self.strSquares[self.event.widget.position]!="":
            return
        if self.validate_move(event.widget.position):
            self.remove_pieces()

    def validate_move(self, position):
        for i in self.find_liberties(position):
            if self.strSquares[i]=="":
                self.make_move(position)
                self.errorVar.set("")
                self.liberties=[]
                return
            self.errorVar.set("Can't make move: move is suicidal!")
        
    def find_liberties(self, position):
        self.original_liberties=self.liberties
        r,c=position
        for (i,x) in [(0,1), (1,0), (0,-1), (-1,0)]:
            try:
                self.strSquares[(r+i,c+x)]
                if not((r+i,c+x) in self.liberties):
                    self.liberties.append((r+i,c+x))
            except KeyError:
                pass

        for i in self.liberties:
            a=self.strSquares[i]
            if a==self.turn and not(a in self.original_liberties): 
                print(self.liberties)
                if self.original_liberties==self.liberties:
                    return self.liberties
                else:
                    self.liberties+=self.find_liberties(i)
        return self.liberties
    def make_move(self, position):
        self.strSquares[position]=self.turn
        self.event.widget.make_piece(["white", "black"][self.turn])
        self.turn=1-self.turn
        
goFrame()
