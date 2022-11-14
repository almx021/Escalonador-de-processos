"""
Objetivo: Simular as estratégias de alocação de memória first-fit, best-fit e worst-fit.


Descrição: O programa deverá medir a utilização da memória (percentual de memória
utilizada) e o tempo médio de espera dos processos. O tempo de espera de cada processo é o
intervalo de tempo entre a criação e a conclusão do processo.


Entradas do Sistema:
Antes de iniciar a simulação, o usuário deverá configurar os seguintes parâmetros:
• Quantidade de processos que serão criados;
• Estratégia de alocação utilizada: first fit, best fit ou worst fit;
• Tamanho da memória real (MB);
• Tamanho da área de memória ocupada pelo sistema operacional (MB);
• [M1, M2] - Intervalo para gerar aleatoriamente a área ocupada por cada processo na
memória (MB);
• [tc1, tc2] - Intervalo para gerar aleatoriamente o tempo de criação de cada processo em
relação ao processo criado anteriormente (segundos). Portanto, o instante de criação
do processo é a soma do valor gerado aleatoriamente neste intervalo com o instante
em que foi criado o processo anterior;
• [td1, td2] - Intervalo para gerar aleatoriamente a duração de cada processo (segundos).
A duração representa quanto tempo o processo fica utilizando a memória a partir do
instante em que ele foi alocado.


Saídas:
A cada instante, o programa deverá mostrar na tela as seguintes informações:
• Mapa da memória, mostrando a área de memória ocupada por cada processo e as
áreas livres;
• Os processos que estão alocados na memória;
• Os processos que estão na fila aguardando a liberação de espaço de memória para
serem alocados;
• Os instantes de tempo em que cada processo foi criado, foi alocado na memória e
concluiu sua execução;
• Tempo de espera de cada processo (diferença entre o instante de conclusão e o
instante de criação);
• Tempo médio de espera dos processos que já concluíram (média do tempo de espera
de cada processo);
• Percentual de memória utilizada.

Funcionamento do programa:
Ao iniciar a execução, o programa deverá solicitar ao usuário a digitação de todos os
dados de entrada. Em seguida, deverá gerar aleatoriamente o instante de criação, a duração e
área de memória ocupada por cada processo.
Depois disto, o programa deverá iniciar a simulação alocando e liberando memória
para os processos de acordo com seus parâmetros. Vale ressaltar que não deverá ser feito
nenhum mecanismo de compactação, ou seja, um processo, ao ser criado, só deverá ser
alocado na memória caso exista um buraco na memória que o caiba. Caso contrário, o
processo deverá ficar na fila aguardando a liberação de um espaço de memória que o caiba.
"""

import random, queue
from time import sleep

from classes.process import Process
from classes.memory import Memory

class Scheduler:
   
    def __init__(self) -> None:
        memory_size = int(input("Tamanho da memória: "))
        so_size = int(input("Uso de memória do SO: "))
        self.allocation_method = int(input("Método de alocação de processos (1 para FF, 2 para BF, 3 para WF): "))
        self.number_of_processes = int(input("Quantidade de processos: "))
        self.range_of_creation = list(map(int, input("limite inferior e superior de tempo para criação dos processos, separados por espaço: ").split()))
        self.range_of_duration = list(map(int, input("limite inferior e superior de duração dos processos, separados por espaço: ").split()))
        self.range_of_space = list(map(int, input("limite inferior e superior de uso de memória dos processos, separados por espaço: ").split()))
        
        self.memory = Memory(memory_size, so_size)
        self.processes = dict()
        self.finished_processes = list()
        self.list_of_init_times = list()
        self.waiting_room = queue.Queue(self.number_of_processes)
        
        self.counter = 0
        
    def main_loop(self):
        for _ in range(self.number_of_processes):
            self.list_of_init_times.append(random.randint(self.range_of_creation[0], self.range_of_creation[1]))
            if _ > 0:
                self.list_of_init_times[_] +=  self.list_of_init_times[_- 1]
        
        while (not self.list_of_init_times == [] 
               or not all(
                   process.status == 'Finished' for process in self.processes.values()
                   )):
            sleep(0.1)
            self.counter += 1
            print('\nCONTADOR DE TEMPO:', self.counter) 

            if self.list_of_init_times != []:
                print('Próximos tempos de criação de processos:', self.list_of_init_times, '\n')

            self.update_schedule()
                       
            self.generate_report()
    
    def _create_process(self, init_time):
        id = len(self.processes)
        duration = random.randint(self.range_of_duration[0], self.range_of_duration[1])
        size = random.randint(self.range_of_space[0], self.range_of_space[1])
            
        p = Process(id, init_time, duration, size)
        self.processes[id] = p
        self.list_of_init_times.pop(self.list_of_init_times.index(self.counter))
        self.waiting_room.put(p)
        return p

    def _allocate_process(self, process:Process, cluster):
        process.allocation_time = self.counter
        process.waiting_time = self.counter + process.duration
        process.status = "Running"
        process.set_inner_memory_address = cluster[0]
        process.set_upper_memory_address = cluster[0] + process.memory_usage - 1

        self.memory.current_processes.append(process)
        self.memory.memory_usage += process.memory_usage
        
    def _desallocate_process(self, process:Process):
        process.end_time = self.counter
        process.status = "Finished"
        
        self.memory.memory_usage -= process.memory_usage
        
        self.finished_processes.append(
            self.memory.current_processes.pop(
                self.memory.current_processes.index(process)))

    def _fit_process(self):
        if self.allocation_method == 1:
            return self._first_fit()
        
        while not self.waiting_room.empty() and not self.memory.get_free_space < 1:
            free_clusters = []
            free_areas = self.memory.get_free_areas
            
            for cluster in free_areas:
                if cluster[2] >= self.waiting_room.queue[0].memory_usage:
                    free_clusters.append(cluster)
                
            if len(free_clusters) == 0:
                return
        
            if self.allocation_method == 2:
                cluster = sorted(free_clusters, key=lambda c:c[2])[0]                 
            elif self.allocation_method == 3:
                cluster = sorted(free_clusters, key=lambda c:c[2])[-1]
                
            del free_clusters
            self._allocate_process(self.waiting_room.get(), cluster)

    def _first_fit(self):
        i = 0
            
        while not self.waiting_room.empty() and not self.memory.get_free_space < 0:  
            free_areas = self.memory.get_free_areas
            
            for cluster in free_areas:
                print(f'FREE AREAS: {free_areas}')
                if cluster[2] >= self.waiting_room.queue[0].memory_usage:
#                    talvez seja útil no futuro:
#                    print(i)
#                    print(f'[[[{free_areas}]]]')
#                    print(f'---------------{cluster, self.waiting_room.queue[0].memory_usage}-----------')
#                    print(f'----{self.memory.get_unavailable_areas}----')
                    self._allocate_process(self.waiting_room.get(), cluster)
                    i = 0
                    break
                else:
                    i += 1
                
            if i == len(free_areas):
                return

    def update_schedule(self):
        _flag = False
        for process in self.processes.values():
            if (process.status == 'Running' and 
                self.counter - process.duration == process.allocation_time):
                _flag = True
                self._desallocate_process(process)

        while self.counter in self.list_of_init_times:
            _flag = True
            process = self._create_process(self.counter)
        
        if _flag:
            self._fit_process()

        assert len(self.memory.current_processes) == len(self.memory.get_unavailable_areas) - 1


    def generate_report(self):
        print(f"""-------------------------------------------------------------------------
Estado da memória:
        Total - {self.memory.memory_size}
        Usada - {self.memory.memory_usage}
        Livre - {self.memory.get_free_space}
        Porcentagem de uso - {round((self.memory.memory_usage / self.memory.memory_size)*100, 2)}%
        Áreas ocupadas - {self.memory.get_unavailable_areas}
        Áreas livres - {self.memory.get_free_areas}
    --------------------------------------
Processos alocados:""")
        for i in self.memory.current_processes:
            print(f'        {i}')

        print("""    --------------------------------------
Processos na fila:""")
        for i in self.waiting_room.queue:
            print(f'        {i}')
            
        print("""    --------------------------------------
Processos finalizados:""")
                
        for i in sorted(self.finished_processes, key=lambda p:p.id):
            print(f'        ID: {i.id},\n'
            f'        Tempo de criação: {i.init_time},'
            f'        Tempo de alocação: {i.allocation_time},'
            f'        Tempo de conclusão: {i.end_time},'
            f'        Tempo de espera: {i.waiting_time}')
        print("""-------------------------------------------------------------------------""")


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.main_loop()
    
    del scheduler