from typing import List, Tuple
import numpy as np
from queue import Queue

from .shared.Observer import Observer

from .memory import Memory
from .process import Process

class SimulationDataReporter(Observer):
    def __init__(self, waiting_processes_queue: Queue, memory: Memory, finished_processes_list: List[Process]):
        self.memory = memory

        self.finished_processes_list = finished_processes_list
        self.waiting_processes_queue = waiting_processes_queue

        self.running_processes_data = np.array([
            np.array([], dtype=np.chararray),
            np.array([], dtype=np.int32),
            np.array([], dtype=np.int32),
            np.array([], dtype=np.int32),
            np.array([], dtype=np.int32)
        ])

        self.finished_processes_data = np.array([
            np.array([], dtype=np.chararray),
            np.array([], dtype=np.int32),
            np.array([], dtype=np.int32),
            np.array([], dtype=np.int32),
            np.array([], dtype=np.int32)
        ])

        self.waiting_processes_data = np.array([
            np.array([], dtype=np.chararray),
            np.array([], dtype=np.int32),
            np.array([], dtype=np.int32)
        ])

        self._observers: List[Observer] = []

    def trigger_process_created_event(self):
        self._refresh_waiting_processes()
        self._alert_event("process_created")

    def trigger_process_allocated_event(self):
        self._refresh_waiting_processes()
        self._refresh_running_processes()
        self._alert_event("process_allocated")

    def trigger_process_finished_event(self):
        self._refresh_running_processes()
        self._refresh_finished_processes()
        self._alert_event("process_finished")

    def recalculate_all(self):
        self._refresh_waiting_processes()
        self._refresh_running_processes()
        self._refresh_finished_processes()
        self._alert_event("all")
    
    def _refresh_waiting_processes(self):
        size = len(self.waiting_processes_queue.queue)

        self.waiting_processes_data = np.array([
            np.zeros(size, dtype=np.chararray),
            np.zeros(size, dtype=np.int32),
            np.zeros(size, dtype=np.int32)
        ])

        for index, process in enumerate(self.waiting_processes_queue.queue):
            self.waiting_processes_data[0][index] = np.str0(f"P{process.id}")
            self.waiting_processes_data[1][index] = np.int32(process.memory_usage)
            self.waiting_processes_data[2][index] = np.int32(process.init_time)

    def _refresh_running_processes(self):
        size = len(self.memory.current_processes)

        self.running_processes_data = np.array([
            np.zeros(size, dtype=np.chararray),
            np.zeros(size, dtype=np.int32),
            np.zeros(size, dtype=np.int32),
            np.zeros(size, dtype=np.int32),
            np.zeros(size, dtype=np.int32),
            np.zeros(size, dtype=np.int32),
        ])

        for index, process in enumerate(self.memory.current_processes):
            self.running_processes_data[0][index] = np.str0(f"P{process.id}")
            self.running_processes_data[1][index] = np.int32(process.memory_usage)
            self.running_processes_data[2][index] = np.int32(process.get_inner_memory_address)
            self.running_processes_data[3][index] = np.int32(process.init_time)
            self.running_processes_data[4][index] = np.int32(process.allocation_time)
            self.running_processes_data[5][index] = np.int32(process.duration)

    def _refresh_finished_processes(self):
        size = len(self.finished_processes_list)

        self.finished_processes_data = np.array([
            np.zeros(size, dtype=np.chararray),
            np.zeros(size, dtype=np.int32),
            np.zeros(size, dtype=np.int32),
            np.zeros(size, dtype=np.int32),
            np.zeros(size, dtype=np.int32),
            np.zeros(size, dtype=np.int32)
        ])

        for index, process in enumerate(self.finished_processes_list):
            self.finished_processes_data[0][index] = np.str0(f"P{process.id}")
            self.finished_processes_data[1][index] = np.int32(process.memory_usage)
            self.finished_processes_data[2][index] = np.int32(process.init_time)
            self.finished_processes_data[3][index] = np.int32(process.allocation_time)
            self.finished_processes_data[4][index] = np.int32(process.end_time)
        
        self.finished_processes_data[5] = self.finished_processes_data[4] - self.finished_processes_data[2]
    
    def get_free_areas(self):
        return np.array(self.memory.get_free_areas)

    @property
    def memory_usage(self):
        return self.memory.memory_usage
    
    @property
    def memory_size(self):
        return self.memory.memory_size
    
    def subscribe(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def _alert_event(self, event: str):
        for observer in self._observers:
            observer.alert(event)
