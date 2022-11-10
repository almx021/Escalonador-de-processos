class Process:
    def __init__(self, init_time, duration, memory_usage) -> None:
        self.init_time = init_time
        self.duration = duration
        self.memory_usage = memory_usage
        self.allocation_time = None
        self.waiting_time = None
        self.status = 'Waiting'
    