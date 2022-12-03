from tkinter import Tk

class Window(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1024x720")

        self.current_frame = None
        self.frames = {}
        self.data = {}
    
    def add_frame(self, frame, id):
        self.frames[id] = frame
        self.frames[id].place(relwidth=1, relheight=1)
        self.frames[id].render()
    
    def raise_frame(self, id):
        self.current_frame = self.frames[id]
        self.current_frame.tkraise()