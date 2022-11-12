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
            self.memory_usage = self.so_size = so_size
            self.current_processes = list()

            Memory.__instance = self

    @property
    def get_free_space(self):
        return self.memory_size - self.memory_usage
    
    @property
    def get_free_areas(self):
        areas = self.get_unavailable_areas
        
        if len(areas) == 1:
            return [(areas[0][1] + 1, self.memory_size - 1, self.memory_size - areas[0][1] - 1)]
        else:
            _free_areas = []
            
            for i in range(1, len(areas)):
                if areas.values()[i][0] > areas.values()[i-1][1] + 1:
                    _free_areas.append(
                        (areas.values()[i-1][1] + 1, # first free position in this cluster
                         areas.values()[i][0] - 1, # last free position in this cluster
                         areas.values()[i][0] - areas.values()[i-1][1] + 1) # free space in this cluster
                        )
                    
            _free_areas.append(
                areas[len(areas) - 1][1] + 1,
                self.memory_size - 1,
                self.memory_size - areas[len(areas) - 1][1] - 1
                )
            
            return _free_areas
    
    @property
    def get_unavailable_areas(self):
        if hasattr(self, '_unavailable_area'):
            _unavailable_areas
            
        _unavailable_areas = {0: (0, self.so_size - 1)}
        
        for process in self.current_processes:
            _unavailable_areas[process.id + 1] = (process.get_inner_memory_address,
                                                  process.get_upper_memory_address)
            
        return _unavailable_areas
    
    def free(self, space):
        self.memory_usage -= space     