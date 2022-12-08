from tkinter import *

from typing import List
from numpy.typing import ArrayLike
import numpy as np

blue = "#035AA4"
red = "#EE3124"
white = "#CDCCCC"
yellow = "#BA8843"


class MemoryBar(Frame):
    def __init__(self, master, memory_size: int, so_memory_usage: int):
        super().__init__(master)
        self.memory_size = memory_size
        self.so_memory_usage = so_memory_usage

    def render(self):
        self.canvas = Canvas(self, background=white)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind(
            "<Configure>", lambda _: self._render_static_objects())

        self._render_static_objects()

    def _render_static_objects(self):
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
            fill=yellow,
            tags=("static")
        )
        self.canvas.create_text(
            rectangle_width / 2.0,
            rectangle_height / 2.0,
            text="S.O",
            fill="#FFFFFF",
            tags=("static"),
            anchor="center",
        )


class MemoryBarController:
    def __init__(self, memory_bar: MemoryBar):
        self.memory_bar = memory_bar

    def draw_processes(self, processes, free_areas):
        width = self.memory_bar.canvas.winfo_width()
        height = self.memory_bar.canvas.winfo_height()

        epsilon = height / self.memory_bar.memory_size

        # processes[0] -> Array with the processes PID's
        # processes[1] -> Array with the processes memory usage
        # processes[2] -> Array with the processes inner memory address

        for i in range(len(processes[0])):
            processes[0][i] = np.str0(
                f"{str(processes[0][i])} ({int(processes[1][i])} MU)")

        processes[1] = processes[1] * epsilon
        processes[2] = processes[2] * epsilon
        processes[1] = processes[2] + processes[1]

        rectangles_data = np.array([processes[2], processes[1]])
        processes_labels_data = np.array([
            processes[0],
            (processes[2] + processes[1]) / 2
        ])

        free_areas = np.transpose(free_areas)
        # free_areas [0] -> First position
        # free_areas [1] -> Last position

        free_areas_labels_text = np.array([
            f"Free ({int(free_areas[2][i])} MU)" for i in range(len(free_areas[0]))
        ])

        free_areas_labels_data = np.array([
            free_areas_labels_text,
            (free_areas[1] + free_areas[0]) * (epsilon / 2)
        ])

        colors = [blue, red]

        middle = width / 2
        _, number_of_processes = rectangles_data.shape

        self.memory_bar.canvas.delete("dynamic")
        for i in range(number_of_processes):
            self.memory_bar.canvas.create_rectangle(
                0, rectangles_data[0][i],
                width,
                rectangles_data[1][i],
                fill=colors[i % 2],
                tags=("dynamic")
            )

            self.memory_bar.canvas.create_text(
                middle, processes_labels_data[1][i],
                text=processes_labels_data[0][i],
                fill="#FFFFFF",
                tags=("dynamic"),
                anchor="center"
            )

        for i in range(len(free_areas_labels_data[0])):
            self.memory_bar.canvas.create_text(
                middle, free_areas_labels_data[1][i],
                text=free_areas_labels_data[0][i],
                fill="#FFFFFF",
                tags=("dynamic"),
                anchor="center"
            )

        self.memory_bar.canvas.update_idletasks()
