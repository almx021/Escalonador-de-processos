class Process:
    def __init__(self, id, init_time, duration, memory_usage) -> None:
        self.id = id
        self.init_time = init_time
        self.duration = duration
        self.memory_usage = memory_usage
        self.allocation_time = None
        self.waiting_time = None
        self.status = 'Waiting'
        
    def __str__(self):
        return "Process info: {self.init_time, self.duration, self.memory_usage}"
    