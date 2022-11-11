class Memory:
    __instance = None
    
    def __new__(cls, *args, **kwargs):
        if Memory.__instance is None:
            return super().__new__(cls)
        else:
            return Memory.__instance
    
    def __init__(self, memory_size, so_size):
        if Memory.__instance is None:
            self.memory_size = memory_size
            self.memory_usage = so_size
            self.current_processes = list()

            Memory.__instance = self

    @property
    def free_space(self):
        return self.memory_size - self.memory_usage   
    
    def free(self, space):
        self.memory_usage -= space     