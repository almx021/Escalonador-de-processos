from .Screen import Screen
from .Window import Window

from tkinter import *

from typing import List, Tuple

from classes.shared.Observer import Observer
from classes.simulation_data_reporter import SimulationDataReporter

import numpy as np

from screens.components.memory_bar import MemoryBar, MemoryBarController
from screens.components.Table import Table

class SimulationPanel(Screen, Observer):
    def __init__(self, window: Window, simulation_data_reporter: SimulationDataReporter):
        super(Screen, self).__init__(window)

        self.simulation_data_reporter = simulation_data_reporter
        simulation_data_reporter.subscribe(self)

    def render(self):
        self.memory_bar = MemoryBar(
            self,
            self.simulation_data_reporter.memory.memory_size,
            self.simulation_data_reporter.memory.so_size
        )
        self.memory_bar.place(relx=0.05, relwidth=0.15, rely=0.05, relheight=0.8)
        self.memory_bar.render()

        self.memory_bar_controller = MemoryBarController(self.memory_bar)

        self.current_processes_table = Table(self, headers=["PID", "Usage", "Inner memory"], row_height=20)
        self.current_processes_table.place(relx=0.23, relwidth=0.35, rely=0.05, relheight=0.8)
        self.current_processes_table.render()

    def alert(self):
        self.current_processes_table.set(self.simulation_data_reporter.data.copy())
        self.memory_bar_controller.draw_processes(self.simulation_data_reporter.data.copy())