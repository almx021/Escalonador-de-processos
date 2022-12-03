from tkinter import *

from typing import List
from numpy.typing import ArrayLike
import numpy as np

class MemoryBar(Frame):
    def __init__(self, master, memory_size: int, so_memory_usage: int):
        super().__init__(master)
        self.memory_size = memory_size
        self.so_memory_usage = so_memory_usage
        
    def render(self):
        self.canvas = Canvas(self, background="#A0A0A0")
        self.canvas.pack(fill="both", expand=True)

        self._draw_static_objects()

    def _draw_static_objects(self):
        self.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        rectangle_width = width
        rectangle_height = self.so_memory_usage * height / self.memory_size

        self.canvas.create_rectangle(
            0,
            0,
            rectangle_width,
            rectangle_height,
            fill="#FFFFFF",
            tags=("static")
        )
        self.canvas.create_text(
            rectangle_width / 2.0,
            rectangle_height / 2.0,
            text=f"S.O ({self.so_memory_usage}) um",
            tags=("static"),
            anchor="center"
        )

class MemoryBarController:
    def __init__(self, memory_bar: MemoryBar):
        self.memory_bar = memory_bar
    
    def draw_processes(self, processes):
        width = self.memory_bar.canvas.winfo_width()
        height = self.memory_bar.canvas.winfo_height()

        # for i, (pid, inner_memory_address, memory_usage) in enumerate(processes):
        #     pid = f"{pid} ({memory_usage} um)"
        #     m = ((inner_memory_address) / self.memory_bar.memory_size) * height
        #     n = ((memory_usage) / self.memory_bar.memory_size) * height

        #     y0, y1 = m, m + n

        # self.memory_bar.canvas.tk
        # self.memory_bar.canvas.delete("dynamic")
        # for pid, y0, y1 in display_data:
        #     self.memory_bar.canvas.create_rectangle(0, y0, width, y1, fill="#FFFFFF", tags=("dynamic"))
        #     self.memory_bar.canvas.create_text(width / 2, (y1 + y0) / 2, anchor="center", text=pid, fill="black", tags=("dynamic"))

        epsilon = height / self.memory_bar.memory_size

        processes[1] = processes[1] * epsilon
        processes[2] = processes[2] * epsilon
        processes[2] = processes[1] + processes[2]

        rectangles_data = np.array([processes[1], processes[2]])

        label_data = np.array([processes[0], (processes[1] + processes[2]) / 2])
        middle = width / 2

        _, number_of_processes = rectangles_data.shape


        self.memory_bar.canvas.delete("dynamic")
        for i in range(number_of_processes):
            self.memory_bar.canvas.create_rectangle(0, rectangles_data[0][i], width, rectangles_data[1][i], fill="#FFFFFF", tags=("dynamic"))
            self.memory_bar.canvas.create_text(middle, label_data[1][i], text=label_data[0][i], tags=("dynamic"), anchor="center")
