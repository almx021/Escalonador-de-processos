from tkinter import Tk

class Window(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")

        self.current_frame = None
        self.frames = {}
        self.data = {}
    
    def add_frame(self, frame, id):
        self.frames[id] = frame
    
    def raise_frame(self, id):
        if self.current_frame is not None:
            self.current_frame.place_forget()
            self.current_frame = None
        
        self.current_frame = self.frames[id]
        self.current_frame.place(relwidth=1, relheight=1)