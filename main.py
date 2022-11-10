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
        self.intilization_times = list()
        self.last_initialization_time = 0
        self.waiting_room = queue.Queue(self.number_of_processes)
        
    def main(self):
        for _ in range(self.number_of_processes):
            self.intilization_times.append(random.randint(self.range_of_creation[0], self.range_of_creation[1]))
            if _ > 0:
                self.initilization_times[_] +=  self.initilization_times[_- 1]
                
        counter = 0
        print(self.intilization_times)
        
        while True:
           sleep(1)
           counter += 1
           
           print(counter)
           
           if counter in self.list_of_init_times:
               print('oi')
               self._create_process(counter)
               self.list_of_init_times.pop(counter)
               self._schedule_process(self, self.processes[len(self.processes) - 1])
               
               print(processes) 
    
    def _create_process(self, init_time):
        
        for id in range(self.number_of_processes):
            duration = random.randint(self.range_of_duration[0], self.range_of_duration[1])
            size = random.randint(self.range_of_space[0], self.range_of_space[1])
            
            init_time += self.last_initialization_time
            self.processes[id] = Process(init_time, duration, size)

            self.last_initialization_time = last_time
            

    def _schedule_process(self, element):
        if not self.waiting_room.empty:
            self.waiting_room.put(element)
        else:
            if self.memory.free_space > element.memory_usage:
                self.memory.current_processes.append(element)
                self.memory.free_space -= element.memory_usage
                
        
    def _pop_from_queue(self):
        self.waiting_room.get()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.main()
    
    del scheduler