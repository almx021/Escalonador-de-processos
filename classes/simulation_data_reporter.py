from typing import List, Tuple
import numpy as np

from .shared.Observer import Observer

from .memory import Memory


class SimulationDataReporter(Observer):
    def __init__(self, memory: Memory):
        self.running_processes_data: np.array[Tuple] = np.array([])
        self.memory = memory

        self._observers: List[Observer] = list()

    def update_data(self):
        # self.running_processes_data = np.array(
        #     [
        #         (
        #             np.str0('P' + str(process.id)),
        #             np.int32(process.get_inner_memory_address),
        #             np.int32(process.memory_usage)
        #         )
        #         for process in self.memory.current_processes
        #     ]
        # )

        # print(self.running_processes_data)

        # self._alert_all()
        size = len(self.memory.current_processes)

        self.running_processes_data = np.array([
            np.zeros(size, dtype=np.chararray),
            np.zeros(size, dtype=np.int32),
            np.zeros(size, dtype=np.int32)
        ])

        for index, process in enumerate(self.memory.current_processes):
            self.running_processes_data[0][index] = np.str0(f"P{process.id}")
            self.running_processes_data[1][index] = np.int32(process.memory_usage)
            self.running_processes_data[2][index] = np.int32(process.get_inner_memory_address)

        self._alert_all()
    
    def subscribe(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def _alert_all(self):
        for observer in self._observers:
            observer.alert()
