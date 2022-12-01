from .Screen import Screen
from .Window import Window

from tkinter import *

from typing import List, Tuple

from classes.shared.Observer import Observer
from classes.simulation_data_reporter import SimulationDataReporter

class SimulationPanel(Screen, Observer):
    def __init__(self, window: Window, simulation_data_reporter: SimulationDataReporter):
        super(Screen, self).__init__(window)

        self.simulation_data_reporter = simulation_data_reporter
        simulation_data_reporter.subscribe(self)

        self.render()

    def render(self):
        self.canvas = Canvas(self, background="#A0A0A0")
        print("Canvas instantiated")
        self.canvas.place(relx=0.05, relwidth=0.25, rely=0.1, relheight=0.8)

        self.start_button = Button(self, text="Start")
        self.start_button.place(relx=0.5, relwidth=0.45, rely=0.1, height=40)
    
    def alert(self):
        self.draw_processes(self.simulation_data_reporter.data)
    
    def draw_processes(self, processes: List[Tuple[str, float, float]]):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        display_data: list[tuple[str, float, float]] = []

        memory_size = self.simulation_data_reporter.memory.memory_size
        for pid, inner_memory_address, memory_usage in processes:
            m = (inner_memory_address / memory_size) * height
            n = (memory_usage / memory_size) * height
            pid = f"{pid}\n{memory_usage}"

            y0, y1 = m, m + n

            display_data.append((pid, y0, y1))

        self.canvas.delete('all')
        for pid, y0, y1 in display_data:
            self.canvas.create_rectangle(0, y0, width, y1, fill="#FFFFFF")
            self.canvas.create_text(width / 2, (y1 + y0) / 2, anchor="center", text=pid, fill="black")
