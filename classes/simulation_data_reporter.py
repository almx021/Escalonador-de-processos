from typing import List, Tuple

from .shared.Observer import Observer

from .memory import Memory


class SimulationDataReporter(Observer):
    def __init__(self, memory: Memory):
        self.data: List[Tuple(str, float, float)] = list()
        self.memory = memory

        self._observers: List[Observer] = list()

    def update_data(self):
        self.data = [
            (
                'P' + str(process.id),
                process.get_inner_memory_address,
                process.memory_usage
            )
            for process in self.memory.current_processes
        ]

        self.data.append(('S.O', 0, self.memory.so_size))

        self._alert_all()
    
    def subscribe(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def _alert_all(self):
        for observer in self._observers:
            observer.alert()
