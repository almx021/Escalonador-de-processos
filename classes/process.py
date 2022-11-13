class Process:
    def __init__(self, id, init_time, duration, memory_usage) -> None:
        self.id = id
        self.init_time = init_time
        self.duration = duration
        self.memory_usage = memory_usage
        self.allocation_time = None
        self.waiting_time = None
        self.end_time = ...
        self.status = 'Waiting'
        self._inner_memory_address = ...
        self._upper_memory_address = ...
       
    @property 
    def get_inner_memory_address(self):
        return self._inner_memory_address
    
    @property
    def get_upper_memory_address(self):
        return self._upper_memory_address
     
    @get_inner_memory_address.setter   
    def set_inner_memory_address(self, x):
        self._inner_memory_address = x

    @get_upper_memory_address.setter
    def set_upper_memory_address(self, x):
        self._upper_memory_address = x        
        
    def get_used_area(self):
        return [self.get_inner_memory_address, self.get_upper_memory_address]
    
    def __str__(self):
        return (f'ID: {self.id},'
    f'        Tempo de criação: {self.init_time}\n')
#    f'Tempo de alocação: {self.allocation_time},\n' 
#    f'Tempo de duração: {self.duration},\n'
#    f'Tempo de espera: {self.waiting_time},\n'
#    f'Tempo de Finalização: {self.end_time},\n'
#    f'Uso de memória: {self.memory_usage},\n')
    