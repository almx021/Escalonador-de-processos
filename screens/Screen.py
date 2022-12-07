import tkinter as tk

from .Window import Window


class Screen(tk.Frame):
    def __init__(self, window: Window):
        super().__init__(window)