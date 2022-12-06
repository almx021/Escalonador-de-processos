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
        self.memory_bar.place(relx=0.05, relwidth=0.10, rely=0.05, relheight=0.8)
        self.memory_bar.render()

        self.memory_bar_controller = MemoryBarController(self.memory_bar)

        self.waiting_processes_table = Table(self, headers=["PID", "Usage", "Created"], header_height=40)
        self.waiting_processes_table.place(relx=0.17, relwidth=0.3, rely=0.05, relheight=0.8)
        self.waiting_processes_table.render()

        self.current_processes_table = Table(self, headers=["PID", "Usage", "Created", "Allocated"], header_height=40)
        self.current_processes_table.place(relx=0.48, relwidth=0.47, rely=0.05, relheight=0.38)
        self.current_processes_table.render()

        self.finished_processes_table = Table(self, headers=["PID", "Usage", "Created", "Allocated", "Finished", "T.E"], header_height=40)
        self.finished_processes_table.place(relx=0.48, relwidth=0.47, rely=0.47, relheight=0.38)
        self.finished_processes_table.render()

        self.usage_label = Label(self, text="Current memory usage is 0%")
        self.usage_label.place(relx=0.05, rely=0.9, anchor="sw")

        self.average_te_label = Label(self, text="Average awaiting time is unknown")
        self.average_te_label.place(relx=0.95, rely=0.9, anchor="se")

    def alert(self, event: str):
        if event == "process_created":
            waiting_processes_data = self.simulation_data_reporter.waiting_processes_data
            self.waiting_processes_table.set(np.array([
                waiting_processes_data[0].copy(),
                waiting_processes_data[1].copy(),
                waiting_processes_data[2].copy()
            ]))

        if event == "process_allocated":
            running_processes_data = self.simulation_data_reporter.running_processes_data

            self.current_processes_table.set(np.array([
                running_processes_data[0].copy(),
                running_processes_data[1].copy(),
                running_processes_data[3].copy(),
                running_processes_data[4].copy()
            ]))
            self.memory_bar_controller.draw_processes(np.array([
                running_processes_data[0].copy(),
                running_processes_data[1].copy(),
                running_processes_data[2].copy()
            ]))

            memory_usage = self.simulation_data_reporter.memory_usage / self.simulation_data_reporter.memory_size * 100
            self.usage_label.config(text="Current memory usage is {:3.2f}%".format(memory_usage))

        elif event == "process_finished":
            finished_processes_data = self.simulation_data_reporter.finished_processes_data.copy()

            # finished_processes_data = np.array([np.flip(array) for array in finished_processes_data])
            finished_processes_data = np.flip(finished_processes_data, axis=1)

            self.finished_processes_table.set(np.array(finished_processes_data))
            self.average_te_label.config(text="Average awaiting time is {:3.2f}".format(np.average(finished_processes_data[5].astype(np.float32))))
            