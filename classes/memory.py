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
            self.so_size = so_size
            self.memory_usage = so_size
            self.current_processes = list()

            Memory.__instance = self

    @property
    def get_free_space(self):
        return self.memory_size - self.memory_usage
    
    @property
    def get_free_areas(self):
        _areas = self.get_unavailable_areas
        if len(_areas) == 1:
            return [(_areas[0][1] + 1, self.memory_size - 1, self.memory_size - _areas[0][1] - 1)]
        else:
            _free_areas = []
            
            for i in range(1, len(_areas)):
                if _areas[i][0] > _areas[i-1][1] + 1:
                    _free_areas.append(
                        (_areas[i-1][1] + 1, # first free position in this cluster
                         _areas[i][0] - 1, # last free position in this cluster
                         _areas[i][0] - _areas[i-1][1] # free space in this cluster
                        ))
                    
            _free_areas.append(
                (_areas[len(_areas) - 1][1] + 1,
                self.memory_size - 1,
                self.memory_size - _areas[len(_areas) - 1][1] - 1
                ))
            
            return _free_areas
    
    @property
    def get_unavailable_areas(self):
        if hasattr(self, '_unavailable_areas'):
            self._unavailable_areas
            
        self._unavailable_areas = [[0, self.so_size - 1]]
        
        self.current_processes = sorted(
            self.current_processes,
            key=lambda p: p.get_inner_memory_address)
        
        for process in self.current_processes:
            self._unavailable_areas.append([process.get_inner_memory_address,
                                                  process.get_upper_memory_address])
            
        return self._unavailable_areas
        